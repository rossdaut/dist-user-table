import argparse
import json
import sys
import threading
from flask import Flask, request

from .server import Server

parser = argparse.ArgumentParser(
    prog = 'peer.app',
    description = 'Launch a chord peer and an http server'
)

parser.add_argument('-a', '--address', type=str, help='Chord address')
parser.add_argument('-p', '--chord-port', type=int, help='Chord port')
parser.add_argument('-P', '--http-port', type=int, help='HTTP port')
parser.add_argument('-J', '--join-address', type=str, help='Join address')
parser.add_argument('-j', '--join-port', type=int, help='Join port')

args = parser.parse_args()

chord_address = args.address or 'localhost'
chord_port = args.chord_port or 50051
http_port = args.http_port or 5000
join_addr = args.join_address
join_port = args.join_port


app = Flask(__name__)

server = Server(chord_address, chord_port, join_addr, join_port)
t = threading.Thread(target=server.serve)
t.start()

@app.route('/status/<int:user_id>', methods=['GET'])
def get_user_status(user_id):
    status = server.get_user_status(user_id)

    if status is None:
        return json.dumps({ "error": "User not found" }), 404

    return json.dumps({ "status": server.get_user_status(user_id) })

@app.route('/status/<int:user_id>', methods=['POST'])
def set_user_status(user_id):
    status = request.json['status']

    if server.set_user_status(user_id, status):
        return json.dumps({ "success": True }), 200


if __name__ == "__main__":
    app.run(port=http_port)