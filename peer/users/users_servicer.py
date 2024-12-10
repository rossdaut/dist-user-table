from stubs import users_pb2, users_pb2_grpc

from .utils import hash_id


class UsersServicer(users_pb2_grpc.UsersServicer):
    def __init__(self):
        self.users = {}

    def GetUserStatus(self, request, context):
        user_id = request.user_id
        user_status = self.users[user_id] if user_id in self.users else None

        return users_pb2.OptionalUserStatus(exists=user_status != None , status=user_status)

    def SetUserStatus(self, request, context):
        user_id = request.user_id
        status = request.status

        self.users[user_id] = status

        return users_pb2.SetStatusResponse(success=True)

    def write_users(self, filepath, id):
        with open(filepath, 'w') as f:
            f.write(f"ID: {id}\n")

            for user_id, status in self.users.items():
                f.write(f"id: {user_id}\thash: {hash_id(user_id)}\tstatus: {status}\n")
