import grpc
from google.protobuf.empty_pb2 import Empty

from stubs import users_pb2, users_pb2_grpc

def remote_get_user_status(target, user_id):
    with grpc.insecure_channel(f"{target.ip}:{target.port}") as channel:
        stub = users_pb2_grpc.UsersStub(channel)

        optional_status_grpc = stub.GetUserStatus(users_pb2.UserId(user_id=user_id))

        if not optional_status_grpc.exists:
            return None
        return users_pb2.Status.Name(optional_status_grpc.status)

def remote_set_user_status(target, user_id, status):
    with grpc.insecure_channel(f"{target.ip}:{target.port}") as channel:
        stub = users_pb2_grpc.UsersStub(channel)

        response = stub.SetUserStatus(users_pb2.SetStatusRequest(user_id=user_id, status=status))
        return response.success

def remote_transfer_users(address, users):
    with grpc.insecure_channel(f"{address.ip}:{address.port}") as channel:
        stub = users_pb2_grpc.UsersStub(channel)

        response = stub.TransferUsers(users_pb2.UsersMap(users=users))
        return response.success

def remote_request_backup(address):
    with grpc.insecure_channel(f"{address.ip}:{address.port}") as channel:
        stub = users_pb2_grpc.UsersStub(channel)
        response = stub.RequestBackup(Empty())

        return response.users