import math
import hashlib

from constants import M

def generate_id(address):
    hexdigest = hashlib.sha1(str(address).encode()).hexdigest()
    return int(hexdigest, 16) % (2 ** M)

def in_mod_range(value, start, end, lclosed=False, rclosed=False):
    if start < end:
        return start < value < end or (lclosed and value == start) or (rclosed and value == end)
    else:
        return start < value or value < end or (lclosed and value == start) or (rclosed and value == end)

def id_to_bytes(id):
    return id.to_bytes(length=math.ceil(M/8))

def id_from_bytes(id):
    return int.from_bytes(id)