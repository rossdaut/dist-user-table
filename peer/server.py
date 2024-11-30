from concurrent import futures
import grpc

from stubs import chord_pb2, chord_pb2_grpc
from constants import M
from .chord_servicer import ChordServicer

class Server:
    def __init__(self, ip, port, join_port=None):
        self.port = port
        self.join_port = join_port
        self.node = ChordServicer('localhost', port)

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        chord_pb2_grpc.add_ChordServicer_to_server(self.node, server)
        server.add_insecure_port(f"[::]:{self.port}")
        server.start()

        if self.join_port:
            self.node.join(chord_pb2.Node(ip='localhost', port=self.join_port))

        next = 0
        self.node.write_finger()
        while True:
            input()
            self.node.stabilize()
            self.node.fix_fingers(next)
            next = (next + 1) % M
            self.node.write_finger()