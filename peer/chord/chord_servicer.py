from stubs import chord_pb2, chord_pb2_grpc
from constants import M
from .remote import remote_find_successor, remote_notify, remote_predecessor
from .utils import generate_id, id_from_bytes, in_mod_range
from .node import Node

class ChordServicer(chord_pb2_grpc.ChordServicer):
    def __init__(self, ip, port, storage_servicer):
        self.id = generate_id(ip, port)
        self.node = Node(id=self.id, ip=ip, port=port)
        self.predecessor = None
        self.finger = [None] * M
        self.finger[0] = self.node
        self.storage_servicer = storage_servicer

    @property
    def successor(self):
        return self.finger[0]

    @successor.setter
    def successor(self, node):
        self.finger[0] = node

    ### STUB METHODS ###

    def FindSuccessor(self, request, context):
        id = id_from_bytes(request.id)
        node = self.find_successor(id)

        return node.as_grpc()

    def Predecessor(self, request, context):
        predecessor_grpc = self.predecessor.as_grpc() if self.predecessor != None else None
        return chord_pb2.OptionalNode(exists=self.predecessor != None, node=predecessor_grpc)

    def Notify(self, grpc_node, context):
        id = id_from_bytes(grpc_node.id)
        if self.predecessor == None or in_mod_range(id, self.predecessor.id, self.id):
            self.predecessor = Node.of(grpc_node)

            keys_range = range(self.id+1, self.predecessor.id)
            self.storage_servicer.transfer_data(self.predecessor, keys_range)

        return chord_pb2.Empty()


    ### PRIVATE ###

    def find_successor(self, id):
        if self.id == self.successor.id:
            return self.node

        if in_mod_range(id, self.id, self.successor.id+1):
            return self.successor
        
        n = self.closest_preceding_node(id)

        return remote_find_successor(n, id)

    def closest_preceding_node(self, id):
        for i in range(M-1, 0, -1):
            if self.finger[i] == None:
                continue

            node = self.finger[i]
            if in_mod_range(node.id, self.id, id):
                return node

        return self.node

    def join(self, ring_node):
        self.predecessor = None
        self.successor = remote_find_successor(ring_node, self.id)


    ### Periodic Methods ###
 
    def stabilize(self):
        new_successor = remote_predecessor(self.successor)
        
        if new_successor != None:
            if in_mod_range(new_successor.id, self.id, self.successor.id):
                self.successor = new_successor

        remote_notify(self.successor, self.node)

    def fix_fingers(self, next):
        id = (self.id + 2 ** (next)) % (2 ** M)
        self.finger[next] = self.find_successor(id)

    def write_finger(self, filepath):
        with open(filepath, "w") as f:
            f.write(f"ID: {self.id}\n")

            if self.predecessor != None:
                f.write(f"PRED: {self.predecessor.id}\n")

            for i, node in enumerate(self.finger):
                if node == None:
                    continue
                i_str = str(i).rjust(3)
                f.write(f"{i_str}: {node.id}\n")
