from concurrent import futures
from datetime import datetime
import grpc
import time

from stubs import chord_pb2, chord_pb2_grpc, users_pb2_grpc
from constants import M
from .chord.chord_servicer import ChordServicer
from .users.users_servicer import UsersServicer
from .users.remote import remote_get_user_status, remote_set_user_status
from .users.utils import hash_id

class Server:
    def __init__(self, ip, port, join_port=None):
        self.port = port
        self.join_port = join_port
        self.users_servicer = UsersServicer()
        self.chord_servicer = ChordServicer('localhost', port, self.users_servicer)

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        chord_pb2_grpc.add_ChordServicer_to_server(self.chord_servicer, server)
        users_pb2_grpc.add_UsersServicer_to_server(self.users_servicer, server)
        server.add_insecure_port(f"[::]:{self.port}")
        server.start()

        if self.join_port:
            self.chord_servicer.join(chord_pb2.Node(ip='localhost', port=self.join_port))

        next = 0
        log = open(f"output/log_{self.port}.txt", "w")

        self.write_status()
        while True:
            self.stabilize(log)
            self.fix_fingers(next, log)
            self.check_predecessor(log)
            self.write_status()
            next = (next + 1) % M

            log.flush()
            time.sleep(1)

    def get_user_status(self, user_id):
        successor = self.chord_servicer.find_successor(hash_id(user_id))

        return remote_get_user_status(successor, user_id)

    def set_user_status(self, user_id, status):
        successor = self.chord_servicer.find_successor(hash_id(user_id))

        return remote_set_user_status(successor, user_id, status)


    # Periodic methods

    def stabilize(self, log):
        log.write(f"[{datetime.now()}] Stabilizing...\n")
        self.chord_servicer.stabilize()

    def fix_fingers(self, next, log):
        log.write(f"[{datetime.now()}] Fixing fingers...\n")
        self.chord_servicer.fix_fingers(next)

    def check_predecessor(self, log):
        log.write(f"[{datetime.now()}] Checking predecessor...\n")
        self.chord_servicer.check_predecessor()

    

    def write_status(self):
        self.chord_servicer.write_finger(f"output/finger_{self.port}.txt")
        self.users_servicer.write_users(f"output/users_{self.port}.txt", self.chord_servicer.id)
