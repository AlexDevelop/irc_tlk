import socket


class IrcClient(object):
    client = None
    connect_response = None

    def set_client(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # defines the socket

    def check_client(self):
        if self.client is None:
            self.set_client()

        return self

    def get_client(self):
        return self.client