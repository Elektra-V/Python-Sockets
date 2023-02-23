import socket

class Server:
    def __init__(self, port, host=socket.gethostname()):
        self.port = port
        self.host = host


    def __str__(self):
        return "Hello I am server"
    
    
    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            print(f"Connected by {addr}")

            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                print(f"from connected user: {data}")
                data = input(" -> ")
                conn.send(data.encode())

            conn.close()


def main():
    server = Server(8080)
    print(server)
    server.listen()
   

if __name__ == "__main__":
    main()