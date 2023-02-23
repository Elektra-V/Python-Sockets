import socket
from server import Server
from client import Client

def main():

    user_input = int(input("Choose an option\n 1.Listen\n 2.Connect\n Enter: ").strip())

    if user_input == 1:
        server = Server(8080)
        print(server)
        server.listen()
    
    if user_input == 2:
        client = Client(socket.gethostname(), 8080)
        print(client)
        client.connect()


if __name__ == "__main__":
    main()