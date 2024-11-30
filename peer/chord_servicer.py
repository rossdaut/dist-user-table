from stubs import chord_pb2, chord_pb2_grpc
from constants import M
from .utils import *

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

    def Notify(self, node, context):
        id = generate_id(node.ip, node.port)
        if self.predecessor == None or in_mod_range(id, self.predecessor_id, self.id):
            self.predecessor = node

        return chord_pb2.Empty()


    ### PRIVATE ###

    def find_successor(self, id):
        if in_mod_range(id, self.id, self.successor_id+1):
            return self.successor
        
        n = self.closest_preceding_node(id)

        return remote_find_successor(n, id)

    def closest_preceding_node(self, id):
        for i in range(M-1, 0, -1):
            if self.finger[i] == None:
                continue

            node_id = generate_id(self.finger[i].ip, self.finger[i].port)
            if in_mod_range(node_id, self.id, id):
                return self.finger[i]

        return self.node

    def join(self, ring_node):
        self.predecessor = None
        self.successor = remote_find_successor(ring_node, self.id)


    ### Periodic Methods ###
 
    def stabilize(self):
        optional_successor = remote_predecessor(self.successor)
        new_successor = optional_successor.node
        
        if optional_successor.exists:
            id = generate_id(new_successor.ip, new_successor.port)

            if in_mod_range(id, self.id, self.successor_id):
                self.successor = new_successor

        remote_notify(self.successor, self.node)

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