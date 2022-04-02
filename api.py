import grpc

import api_pb2
import api_pb2_grpc


class TrojanServer(object):
    def __init__(self, server, port) -> None:
        self.server = server
        self.port = port
        self.stub = self.createStub()

    def createStub(self):
        channel = grpc.insecure_channel(self.server + ':' + str(self.port))
        stub = api_pb2_grpc.TrojanServerServiceStub(channel)
        return stub

    def listUsers(self):
        users = self.stub.ListUsers(api_pb2.ListUsersRequest())
        users = [user.status for user in users]
        return users

    def addUsers(self, users):
        reqs = []
        for user in users:
            if hasattr(user.user, 'password'):
                print(f'Adding user({user.user.password})')
            elif hasattr(user.user, 'hash'):
                print(f'Adding user({user.user.hash})')
            else:
                print(f'Adding user({user.user.password} - {user.user.hash})')
            reqs.append(api_pb2.SetUsersRequest(status=user,
                        operation=api_pb2.SetUsersRequest.Operation.Add))
        res = self.stub.SetUsers(iter(reqs))
        for i in res:
            print(i)

    def deleteUsers(self, users):
        reqs = []
        for user in users:
            if hasattr(user.user, 'password'):
                print(f'Deleting user({user.user.password})')
            elif hasattr(user.user, 'hash'):
                print(f'Deleting user({user.user.hash})')
            else:
                print(
                    f'Deleting user({user.user.password} - {user.user.hash})')
            reqs.append(api_pb2.SetUsersRequest(status=user,
                        operation=api_pb2.SetUsersRequest.Operation.Delete))
        res = self.stub.SetUsers(iter(reqs))
        for i in res:
            print(i)


def generateUser(password, hash='', upload_speed_limit=39321600, download_speed_limit=39321600, ip_limit=4):
    user = api_pb2.UserStatus(
        user=api_pb2.User(
            password=password,
            hash=hash
        ),
        traffic_total=api_pb2.Traffic(upload_traffic=0, download_traffic=0),
        speed_current=api_pb2.Speed(upload_speed=0, download_speed=0),
        speed_limit=api_pb2.Speed(
            upload_speed=upload_speed_limit, download_speed=download_speed_limit),
        ip_current=0,
        ip_limit=ip_limit,
    )
    return user
