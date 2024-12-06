import json
import threading
from flask import Flask, request

from .server import Server


app = Flask(__name__)

server = Server('localhost', 50051)
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
    app.run()