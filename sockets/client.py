import socket

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    
    def __str__(self):
        return f"Hello I am client"


    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            message = input(" -> ")

            while message.lower().strip() != "quit":
                s.send(message.encode())
                data = s.recv(1024).decode()
                print(f"Received from server: {data}")
                message = input(" -> ")
            
            s.close()


def main():
    client = Client(socket.gethostname(), 8080)
    print(client)
    client.connect()


if __name__ == "__main__":
    main()