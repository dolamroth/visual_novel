import socket
import json

from django.conf import settings


class VndbStats:
    def __init__(self):
        self.sock = None
        self.status = 'Not connection'
        self.connected = False

    def login(self):
        HOST, PORT = settings.VNDB_API_HOST, settings.VNDB_API_PORT
        eot = u"\u0004"

        vndblogin = dict()

        vndblogin["protocol"] = settings.VNDB_API_PROTOCOL
        vndblogin["client"] = settings.VNDB_API_CLIENT
        vndblogin["clientver"] = settings.VNDB_API_CLIENTVER
        vndblogin["username"] = settings.VNDB_API_USERNAME
        vndblogin["password"] = settings.VNDB_API_PASSWORD

        bindata = ("login " + json.dumps(vndblogin))

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.sock.sendall(bytes(bindata + eot, "utf-8"))
            # Read the response "Ok" in order to clear pipe for next call
            received = str(self.sock.recv(1024), "utf-8")
            self.status = 'Connected'
            self.connected = True
        except:
            self.sock = None
            self.status = 'Connection was failed'
            self.connected = False

    def logout(self):
        if self.sock is None:
            return
        self.sock.close()
        self.status = 'not connection (logout)'
        self.connected = False

    def update_vn(self, vndb_id):
        if self.sock is None:
            self.status = 'Connection was failed'
            self.connected = False
            return
        eot = u"\u0004"
        bindata = 'get vn stats (id = {})'.format(vndb_id)
        self.sock.sendall(bytes(bindata + eot, "utf-8"))
        received = str(self.sock.recv(1024), "utf-8")
        # The answer is always in format "results %json_object%" + terminate symbol u"\u0004"
        vn_obj = json.loads(received[8:-1])
        rating = int(float(vn_obj['items'][0]['rating']) * 100.0)
        popularity = int(float(vn_obj['items'][0]['popularity']) * 100.0)
        vote_count = int(vn_obj['items'][0]['votecount'])
        return rating, popularity, vote_count
