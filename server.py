import socket


class LoadBalancer:
    def __init__(self, nodes):
        self.nodes = nodes
        self.current_node = 0

    def get_next_node(self):
        node = self.nodes[self.current_node]
        self.current_node = (self.current_node + 1) % len(self.nodes)
        return node


class Listener:
    def __init__(self, ip, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind(('', port))
        self.listener.listen(0)
        self.connection, address = self.listener.accept()

    def reliable_send(self, data: bytes) -> None:
        """
        Функция отправки данных в сокет
        данные ожидаются сразу типа bytes
        """
        CHUNK_SIZE = 0xffff
        for chunk_start in range(0, len(data), CHUNK_SIZE):
            chunk_end = chunk_start + CHUNK_SIZE
            chunk = data[chunk_start:chunk_end]
            self.connection.send(len(chunk).to_bytes(2, "big"))
            self.connection.send(chunk)
            self.connection.send(b"x00x00")

    def readexactly(self, bytes_count: int) -> bytes:
        """
        Функция приёма определённого количества байт
        """
        received_bytes = b''
        while len(received_bytes) < bytes_count:
            part = self.connection.recv(bytes_count - len(received_bytes))
            if not part:
                raise IOError("Соединение потеряно")
            received_bytes += part
        return received_bytes

    def reliable_receive(self) -> bytes:
        """
        Функция приёма данных
        возвращает тип bytes
        """
        received_bytes = b''
        while True:
            part_len = int.from_bytes(self.readexactly(2), "big")
            if part_len == 0:
                return received_bytes
            received_bytes += self.readexactly(part_len)

    def run(self):
        storage_name = input("Write storage name: ")
        self.reliable_send(storage_name.encode())
        command = input("Write command: ")
        load_balancer = LoadBalancer(['node1', 'node2', 'node3'])
        while command.lower().strip() != 'exit':
            node = load_balancer.get_next_node()
            self.connection.send(node.encode())
            self.reliable_send(command.encode())
            result = self.reliable_receive().decode()
            if not result:
                break
            print('Received from client: ' + result)
            command = input("Write command: ")


my_listener = Listener(socket.gethostname(), 5000)
my_listener.run()
