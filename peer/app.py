import json
import sys
import threading
from flask import Flask, request

from .server import Server

chord_port = 50051
http_port = 5000
join_port = None

if len(sys.argv) > 1:
    chord_port = int(sys.argv[1])

if len(sys.argv) > 2:
    http_port = int(sys.argv[2])

if len(sys.argv) > 3:
    join_port = int(sys.argv[3])


app = Flask(__name__)

server = Server('localhost', chord_port, join_port)
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