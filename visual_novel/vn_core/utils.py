import socket
import json

from django.conf import settings

__version__ = '0.1'


class VndbStats(object):
    def __init__(self):
        self.sock = None
        self.protocol = settings.VNDB_API_PROTOCOL
        self.client = settings.VNDB_API_CLIENT
        self.clientver = settings.VNDB_API_CLIENTVER
        self.username = settings.VNDB_API_USERNAME
        self.password = settings.VNDB_API_PASSWORD
        self.eot = u"\u0004"

    class VndbError(Exception):
        message = ''

        def __str__(self):
            return self.message

    class VndbAuthError(VndbError):
        message = 'Подключение не выполнено'

    class VndbTypeError(VndbError):
        message = 'Передано значение неверного типа'

    def __assert(self, param, type):
        try:
            assert type(param), type
        except AssertionError:
            raise self.VndbTypeError()

    def login(self):
        HOST, PORT = settings.VNDB_API_HOST, settings.VNDB_API_PORT

        vndblogin = dict()

        vndblogin["protocol"] = self.protocol
        vndblogin["client"] = self.client
        vndblogin["clientver"] = self.clientver
        vndblogin["username"] = self.username
        vndblogin["password"] = self.password

        bindata = ("login " + json.dumps(vndblogin))

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.sock.sendall(bytes(bindata + self.eot, "utf-8"))
            # Read the response "Ok" in order to clear pipe for next call
            received = str(self.sock.recv(1024), "utf-8")
        except:
            self.sock = None
            raise self.VndbAuthError()

    def logout(self):
        try:
            self.sock.close()
        except:
            pass

    def update_vn(self, vndb_id):
        self.__assert(vndb_id, int)
        if self.sock is None:
            raise self.VndbAuthError()
        bindata = 'get vn stats (id = {})'.format(vndb_id)
        self.sock.sendall(bytes(bindata + self.eot, "utf-8"))
        received = str(self.sock.recv(1024), "utf-8")

        # The answer is always in format "results %json_object%" + terminate symbol u"\u0004"
        vn_obj = json.loads(received[8:-1])
        rating = round(float(vn_obj['items'][0]['rating']) * 100.0)
        popularity = round(float(vn_obj['items'][0]['popularity']) * 100.0)
        vote_count = round(vn_obj['items'][0]['votecount'])
        return rating, popularity, vote_count

