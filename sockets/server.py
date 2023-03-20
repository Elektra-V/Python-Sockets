import socket
import threading

class MultiClientServer:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_list = []
        self.client_sockets = []
        self.lock = threading.Lock()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        # server's own IP address and Port number
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            #server connects to specific client socket having some IP address
            client_socket, client_address = self.server_socket.accept()
            print(f"New client connected from {client_address[0]}:{client_address[1]}")
            # blocking the sockets list for adding new sockets to it by one thread at a time
            self.lock.acquire()
            self.client_sockets.append(client_socket)
            self.lock.release()

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            # blocking the clients list for adding new client address to it by one thread at a time avoiding race condition
            self.lock.acquire()
            self.client_list.append(client_address[0])
            self.lock.release()

            client_thread.start()

            print(self.client_list)

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                data = client_socket.recv(1024)

                if data:
                    message = f"Received message from {client_address[0]}:{client_address[1]}: {data.decode('utf-8').strip()}"
                    print(message)

                    # iterate over list of sockets from clients and brodcast message to all clients
                    for socket in self.client_sockets:
                        if socket != client_socket:
                            socket.send(message.encode('utf-8'))

                else:
                    print(f"Client {client_address[0]}:{client_address[1]} disconnected")

                    # blocking the clients list for removing client address from it if user gets disconnected abruptly
                    self.lock.acquire()
                    self.client_list.remove(client_address[0])
                    self.client_sockets.remove(client_socket)
                    self.lock.release()

                    client_socket.close()
                    return
                
            except:
                print(f"Error occurred while receiving message from {client_address[0]}:{client_address[1]}")

                # blocking the clients list for removing client address from it if there is error while receiving message
                self.lock.acquire()
                self.client_list.remove(client_address[0])
                self.lock.release()

                client_socket.close()
                return


if __name__ == '__main__':
    server = MultiClientServer('localhost', 5000)
    server.start_server()