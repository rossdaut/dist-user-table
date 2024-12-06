import grpc

from stubs import users_pb2, users_pb2_grpc

def remote_get_user_status(target, user_id):
    with grpc.insecure_channel(f"{target.ip}:{target.port}") as channel:
        stub = users_pb2_grpc.UsersStub(channel)

        optional_status_grpc = stub.GetUserStatus(users_pb2.UserId(user_id=user_id))

        if not optional_status_grpc.exists:
            return None
        return optional_status_grpc.status

def remote_set_user_status(target, user_id, status):
    with grpc.insecure_channel(f"{target.ip}:{target.port}") as channel:
        stub = users_pb2_grpc.UsersStub(channel)

        response = stub.SetUserStatus(users_pb2.SetStatusRequest(user_id=user_id, status=status))
        return response.success