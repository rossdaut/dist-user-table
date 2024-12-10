import hashlib

from constants import M


def hash_id(id):
    hexdigest = hashlib.sha1(str(id).encode()).hexdigest()
    return int(hexdigest, 16) % (2 ** M)