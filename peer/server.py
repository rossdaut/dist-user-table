from concurrent import futures
import grpc

from stubs import chord_pb2, chord_pb2_grpc, users_pb2_grpc
from constants import M
from .chord.chord_servicer import ChordServicer
from .users.users_servicer import UsersServicer
from .users.remote import remote_get_user_status, remote_set_user_status

class Server:
    def __init__(self, ip, port, join_port=None):
        self.port = port
        self.join_port = join_port
        self.chord_servicer = ChordServicer('localhost', port)
        self.users_servicer = UsersServicer()

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        chord_pb2_grpc.add_ChordServicer_to_server(self.chord_servicer, server)
        users_pb2_grpc.add_UsersServicer_to_server(self.users_servicer, server)
        server.add_insecure_port(f"[::]:{self.port}")
        server.start()

        if self.join_port:
            self.chord_servicer.join(chord_pb2.Node(ip='localhost', port=self.join_port))

        next = 0
        self.chord_servicer.write_finger()
        while True:
            print("Stabilizing...")
            self.chord_servicer.stabilize()
            print("Fixing fingers...")
            self.chord_servicer.fix_fingers(next)
            next = (next + 1) % M
            self.chord_servicer.write_finger()

    def get_user_status(self, user_id):
        successor = self.chord_servicer.find_successor(user_id)

        return remote_get_user_status(successor, user_id)

    def set_user_status(self, user_id, status):
        successor = self.chord_servicer.find_successor(user_id)

        return remote_set_user_status(successor, user_id, status)