import math
import grpc
import hashlib

from constants import M
from stubs import chord_pb2, chord_pb2_grpc

def remote_find_successor(target, id):
    with grpc.insecure_channel(f"{target.ip}:{target.port}") as channel:
        stub = chord_pb2_grpc.ChordStub(channel)
        return stub.FindSuccessor(chord_pb2.SuccessorRequest(id=id_to_bytes(id)))

def remote_notify(target, node):
    with grpc.insecure_channel(f"{target.ip}:{target.port}") as channel:
        stub = chord_pb2_grpc.ChordStub(channel)
        stub.Notify(node)

def remote_predecessor(target):
    with grpc.insecure_channel(f"{target.ip}:{target.port}") as channel:
        stub = chord_pb2_grpc.ChordStub(channel)
        return stub.Predecessor(chord_pb2.Empty())

def generate_id(ip, port):
    node_str = f"{ip}:{port}"
    hexdigest = hashlib.sha1(node_str.encode()).hexdigest()
    return int(hexdigest, 16) % (2 ** M)

def in_mod_range(value, start, end, lclosed=False, rclosed=False):
    if start < end:
        return start < value < end or (lclosed and value == start) or (rclosed and value == end)
    else:
        return start < value or value < end or (lclosed and value == start) or (rclosed and value == end)

def id_to_bytes(id):
    return id.to_bytes(length=math.ceil(M/8))