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
    if (value < 0) or (start < 0) or (end < 0):
        raise ValueError("Value, start, and end must be positive")
    if (value >= 2**M) or (start >= 2**M) or (end >= 2**M):
        raise ValueError("Value, start, and end must be less than 2^M")

    # Normalize
    value = (value - start) % M
    end   = (end - start)   % M
    start = 0

    # Check
    left_check  = start <= value if lclosed else start < value
    right_check = value <= end   if rclosed else value < end

    return left_check and right_check

def id_to_bytes(id):
    return id.to_bytes(length=math.ceil(M/8))