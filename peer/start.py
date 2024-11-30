import sys

from .server import Server

port = 50051
join_port = None

if len(sys.argv) >= 2:
    port = int(sys.argv[1])

if len(sys.argv) == 3:
    join_port = int(sys.argv[2])

server = Server('localhost', port, join_port)
server.serve()
