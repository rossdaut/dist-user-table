from stubs import chord_pb2
from .utils import id_from_bytes, id_to_bytes

class Node:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port

    @classmethod
    def of(cls, grpc_node):
        return cls(id_from_bytes(grpc_node.id), grpc_node.ip, grpc_node.port)

    def as_grpc(self):
        return chord_pb2.Node(id=id_to_bytes(self.id), ip=self.ip, port=self.port)
