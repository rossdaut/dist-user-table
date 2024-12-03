from stubs import users_pb2, users_pb2_grpc


class UsersServicer(users_pb2_grpc.UsersServicer):
    def __init__(self):
        self.users = {}

    def GetUserStatus(self, request, context):
        user_id = request.user_id
        user_status = self.users[user_id].status if user_id in self.users else None

        return users_pb2_grpc.OptionalUserStatus(exists=user_status != None , status=user_status)

    def SetUserStatus(self, request, context):
        user_id = request.id
        status = request.status

        self.users[user_id] = status

        return users_pb2.SetStatusResponse(success=True)