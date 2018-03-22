import socket
import json

from django.conf import settings


def vndb_socket_login():
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
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(bytes(bindata + eot, "utf-8"))
        # Read the response "Ok" in order to clear pipe for next call
        received = str(sock.recv(1024), "utf-8")
        return sock
    except:
        return None


def vndb_socket_logout(sock):
    if sock is None:
        return
    sock.close()


def vndb_socket_update_vn(sock, vndb_id):
    if sock is None:
        return
    eot = u"\u0004"
    bindata = 'get vn stats (id = {})'.format(vndb_id)
    sock.sendall(bytes(bindata + eot, "utf-8"))
    received = str(sock.recv(1024), "utf-8")
    # The answer is always in format "results %json_object%" + terminate symbol u"\u0004"
    vn_obj = json.loads(received[8:-1])
    rating = int(float(vn_obj['items'][0]['rating']) * 100.0)
    popularity = int(float(vn_obj['items'][0]['popularity']) * 100.0)
    vote_count = int(vn_obj['items'][0]['votecount'])
    return rating, popularity, vote_count
