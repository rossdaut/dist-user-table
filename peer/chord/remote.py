import grpc

from stubs import chord_pb2, chord_pb2_grpc
from .utils import id_to_bytes
from .node import Node


def remote_find_successor(target, id):
    with grpc.insecure_channel(f"{target.ip}:{target.port}") as channel:
        stub = chord_pb2_grpc.ChordStub(channel)
        successor_grpc = stub.FindSuccessor(chord_pb2.SuccessorRequest(id=id_to_bytes(id)))

        return Node.of(successor_grpc)

def remote_notify(target, node):
    with grpc.insecure_channel(f"{target.ip}:{target.port}") as channel:
        stub = chord_pb2_grpc.ChordStub(channel)
        stub.Notify(node.as_grpc())

def remote_predecessor(target):
    with grpc.insecure_channel(f"{target.ip}:{target.port}") as channel:
        stub = chord_pb2_grpc.ChordStub(channel)
        optional_predecessor_grpc = stub.Predecessor(chord_pb2.Empty())

        return Node.of(optional_predecessor_grpc.node) if optional_predecessor_grpc.exists else None

def remote_check(target, repeat=3):
    with grpc.insecure_channel(f"{target.ip}:{target.port}") as channel:
        stub = chord_pb2_grpc.ChordStub(channel)

        for i in range(repeat):
            try:
                stub.Check(chord_pb2.Empty())
                return True
            except: continue
        
        return False

def remote_successors(target):
    with grpc.insecure_channel(f"{target.ip}:{target.port}") as channel:
        stub = chord_pb2_grpc.ChordStub(channel)
        nodes_list = stub.Successors(chord_pb2.Empty())

        return [Node.of(grpc_node) for grpc_node in nodes_list.nodes]