import socket
from typing import List

from commands import Commands
from storagemain import Storage


class Client:
    def __init__(self, nodes: List[str], ip: str, port: int):
        self.nodes = nodes
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data: bytes) -> None:
        count_nodes = len(self.nodes)
        for i, chunk in enumerate([data[_:_ + 0xffff] for _ in range(0, len(data), 0xffff)]):
            node_index = i % count_nodes
            node = self.nodes[node_index]
            ip, port = node.split(':')
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect((ip, int(port)))
            connection.send(len(chunk).to_bytes(2, 'big'))
            connection.send(chunk)
            connection.send(b'x00x00')
            connection.close()

    def readexactly(self, bytes_count: int) -> bytes:
        b = b''
        while len(b) < bytes_count:
            part = self.connection.recv(bytes_count - len(b))
            if part:
                b += part
                continue
            raise IOError("Соединение потеряно")
        return b

    def reliable_receive(self) -> bytes:
        b = b''
        while True:
            part_len = int.from_bytes(self.readexactly(2), "big")
            if part_len == 0:
                return b
            b += self.readexactly(part_len)

    def run(self):
        print("Connected to server")
        storage_name = self.reliable_receive().decode()
        storage = Storage(storage_name)
        storage.load()
        print("Storage name " + str(storage_name))
        while True:
            command: str = self.reliable_receive().decode()
            if command:
                commands = Commands()
                result = commands.execute_command(storage, command)
                print(result)
                self.reliable_send(result.encode())
                continue
            break


if __name__ == '__main__':
    nodes = [
        '192.0.2.1:5000',
        '192.0.2.2:5000',
        '192.0.2.3:5000'
    ]
    my_client = Client(nodes, socket.gethostname(), 5000)
    my_client.run()