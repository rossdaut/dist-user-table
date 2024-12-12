from peer.chord.utils import in_mod_range
from stubs import users_pb2, users_pb2_grpc

from .remote import remote_request_backup, remote_transfer_users
from .utils import hash_id


class UsersServicer(users_pb2_grpc.UsersServicer):
    def __init__(self):
        self.users = {}
        self.backup = {}

    def GetUserStatus(self, request, context):
        user_id = request.user_id
        user_status = self.users[user_id] if user_id in self.users else None

        return users_pb2.OptionalUserStatus(exists=user_status != None , status=user_status)

    def SetUserStatus(self, request, context):
        user_id = request.user_id
        status = request.status

        self.users[user_id] = status
        
        return users_pb2.Response(success=True)

    def TransferUsers(self, request, context):
        self.add_all(request.users)

        return users_pb2.Response(success=True)

    def RequestBackup(self, request, context):
        return users_pb2.UsersMap(users=self.users)

    def transfer_data(self, address, keys_range):
        filtered_users = {}

        for user_id in list(self.users):
            if in_mod_range(hash_id(user_id), keys_range.start, keys_range.stop, rclosed=True):
                status = self.users.pop(user_id)
                filtered_users[user_id] = status

        remote_transfer_users(address, filtered_users)

    def request_backup(self, address):
        try:
            self.backup = remote_request_backup(address)
        except: pass

    def save_backup(self):
        self.users.update(self.backup)
        self.backup = {}

    def add_all(self, data):
        for user_id, status in data.items():
            self.users[user_id] = status

    def write_users(self, filepath, id):
        with open(filepath, 'w') as f:
            f.write(f"ID: {id}\n")
            f.write("ID\tHASH\tSTATUS\n\n")

            keys_sorted_by_hash = sorted(self.users.keys(), key=lambda id: hash_id(id))
            for user_id in keys_sorted_by_hash:
                write_user(f, self.users, user_id)
            f.write("\nBACKUP\n")

            backup_sorted_by_hash = sorted(self.backup.keys(), key=lambda id: hash_id(id))
            for user_id in backup_sorted_by_hash:
                write_user(f, self.backup, user_id)
        
def write_user(f, dict, user_id):
    f.write("{id:s}\t{hash:s}\t{status:s}\n".format(
        id = str(user_id).rjust(2),
        hash = str(hash_id(user_id)).rjust(4),
        status = users_pb2.Status.Name(dict[user_id])
    ))
