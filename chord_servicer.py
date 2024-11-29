from dataclasses import dataclass
import math

import grpc
from chord import chord_pb2, chord_pb2_grpc
import hashlib
from constants import M

class ChordServicer(chord_pb2_grpc.ChordServicer):
    def __init__(self, ip, port):
        self.id = generate_id(ip, port)
        self.node = chord_pb2.Node(ip=ip, port=port)
        self.predecessor = None
        self.finger = [None] * M
        self.finger[0] = self.node

    @property
    def successor(self):
        return self.finger[0]

    @property
    def successor_id(self):
        return generate_id(self.successor.ip, self.successor.port)

    @property
    def predecessor_id(self):
        if self.predecessor == None:
            return None

        return generate_id(self.predecessor.ip, self.predecessor.port)

    @successor.setter
    def successor(self, node):
        self.finger[0] = node

    ### STUB METHODS ###
    def FindSuccessor(self, request, context):
        id = int.from_bytes(request.id)
        return self.find_successor(id)

    def Predecessor(self, request, context):
        return chord_pb2.OptionalNode(exists=self.predecessor != None, node=self.predecessor)


    ### PRIVATE ###
    def find_successor(self, id):
        if in_mod_range(id, self.id+1, self.successor_id):
            return self.successor
        
        n = self.closest_preceding_node(id)

        return remote_find_successor(n, id)

    def closest_preceding_node(self, id):
        for i in range(M-1, 0, -1):
            if self.finger[i] == None:
                continue

            node_id = generate_id(self.finger[i].ip, self.finger[i].port)
            if in_mod_range(node_id, self.id+1, id-1):
                return self.finger[i]

        return self.node

    def join(self, ring_node):
        self.predecessor = None
        self.successor = remote_find_successor(ring_node, self.id)
 
    def stabilize(self):
        optional_successor = remote_predecessor(self.successor)
        new_successor = optional_successor.node
        
        if optional_successor.exists:
            id = generate_id(new_successor.ip, new_successor.port)

            if in_mod_range(id, self.id + 1, self.successor_id-1):
                self.successor = new_successor

        remote_notify(self.successor, self.node)

    def Notify(self, node, context):
        id = generate_id(node.ip, node.port)
        if self.predecessor == None or in_mod_range(id, self.predecessor_id+1, self.id-1):
            self.predecessor = node

        return chord_pb2.Empty()

    def fix_fingers(self, next):
        id = (self.id + 2 ** (next)) % (2 ** M)
        self.finger[next] = self.find_successor(id) 

    def write_finger(self):
        with open(f"finger-{self.node.port}.txt", "w") as f:
            f.write(f"ID: {self.id}\n")
            if self.predecessor != None:
                f.write(f"PRED: {self.predecessor_id}\n")
            for i, node in enumerate(self.finger):
                if node == None:
                    continue

                i_str = str(i).rjust(3)
                f.write(f"{i_str}: {generate_id(node.ip, node.port)}\n")

def remote_find_successor(node, id):
    with grpc.insecure_channel(f"{node.ip}:{node.port}") as channel:
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

def in_mod_range(value, start, end):
    if start <= end:
        return start <= value <= end
    else:
        return value >= start or value <= end

def id_to_bytes(id):
    return id.to_bytes(length=math.ceil(M/8))