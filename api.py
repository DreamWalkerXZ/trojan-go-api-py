import grpc

import api_pb2
import api_pb2_grpc

from rich.console import Console

console = Console()


class TrojanServer(object):
    def __init__(self, server, port) -> None:
        self.server = server
        self.port = port
        self.stub = self.generate_stub()

    def generate_stub(self):
        channel = grpc.insecure_channel(self.server + ':' + str(self.port))
        stub = api_pb2_grpc.TrojanServerServiceStub(channel)
        return stub

    def list_users(self):
        users = self.stub.ListUsers(api_pb2.ListUsersRequest())
        users = [user.status for user in users]
        return users

    def add_users(self, users):
        reqs = []
        for user in users:
            reqs.append(api_pb2.SetUsersRequest(status=user,
                        operation=api_pb2.SetUsersRequest.Operation.Add))
        res = self.stub.SetUsers(iter(reqs))
        for i in res:
            console.log(i)

    def delete_users(self, users):
        reqs = []
        for user in users:
            reqs.append(api_pb2.SetUsersRequest(status=user,
                        operation=api_pb2.SetUsersRequest.Operation.Delete))
        res = self.stub.SetUsers(iter(reqs))
        for i in res:
            console.log(i)

    def modify_users(self, users):
        reqs = []
        for user in users:
            reqs.append(api_pb2.SetUsersRequest(status=user,
                        operation=api_pb2.SetUsersRequest.Operation.Modify))
        res = self.stub.SetUsers(iter(reqs))
        for i in res:
            console.log(i)


def generate_user(password, hash='', upload_traffic=0, download_traffic=0, upload_speed_limit=39321600, download_speed_limit=39321600, upload_speed_current=0, download_speed_current=0, ip_limit=4):
    user = api_pb2.UserStatus(
        user=api_pb2.User(
            password=password,
            hash=hash
        ),
        traffic_total=api_pb2.Traffic(
            upload_traffic=upload_traffic, download_traffic=download_traffic),
        speed_current=api_pb2.Speed(
            upload_speed=upload_speed_current, download_speed=download_speed_current),
        speed_limit=api_pb2.Speed(
            upload_speed=upload_speed_limit, download_speed=download_speed_limit),
        ip_current=0,
        ip_limit=ip_limit,
    )
    return user
