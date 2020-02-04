import itertools
import json
import socket


class JSONClient(object):

    def __init__(self, addr):
        self.socket = socket.create_connection(addr)
        self.id_counter = itertools.count()

    def __del__(self):
        self.socket.close()

    def call(self, name, *params):
        request = dict(id=next(self.id_counter),
                       params=list(params),
                       method=name)
        self.socket.sendall(json.dumps(request).encode())

        # This must loop if resp is bigger than 4K
        response = self.socket.recv(4096)
        response = json.loads(response.decode())

        if response.get('id') != request.get('id'):
            raise Exception("expected id=%s, received id=%s: %s"
                            % (request.get('id'), response.get('id'),
                               response.get('error')))

        if response.get('error') is not None:
            raise Exception(response.get('error'))

        return response.get('result')
