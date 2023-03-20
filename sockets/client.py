import socket 

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        # client is connected to the server 
        print(f"Connected to server {self.host}:{self.port}")
        self.start_receiving()
    
    def start_receiving(self):
        while True:
            message = input("Enter message: ")
            self.send_message(message)

            try:
                data = self.client_socket.recv(1024)

                if data:
                    message = data.decode('utf-8').strip()
                    print(message)
                    
                    # if client inputs quit it should close the connection
                    if message == "quit":
                        print("Disconnecting from server")
                        self.client_socket.close()
                        return
                    
                else:
                    print(f"Disconnected from server")
                    self.client_socket.close()
                    return
            
            except:
                print("Error occured while receiving mesaage from server")
                self.client_socket.close()
                return
    
    def send_message(self,message):
        try:
            self.client_socket.send(message.encode('utf-8'))
        except:
            print("Error occured while sending message to server")


if __name__ == '__main__':
    client = Client('localhost', 5000)
    client.connect()