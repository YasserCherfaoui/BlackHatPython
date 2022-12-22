import socket
import argparse
import sys
import textwrap
import threading

class MatrixChat:
    def __init__(self, args):
        self.args = args
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.log = []
    def run(self):
        if(self.args.listen):
            self.listen()
        else:
            self.connect()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen()
        while True:
            client_socket, addr = self.socket.accept()
            self.connections.append(client_socket)
            print(f'{addr[0]}:{addr[1]} has connected to the server')
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()
            

    def handle(self, client_socket):
        try:
            client_socket.send(b'\n Welcome to The Matrix!')
            while True:
                message = client_socket.recv(4096).decode()
                while message:
                    for connection in self.connections:
                        connection.send(message.encode())
                    message = ''
        except Exception as e:
            print(f'Server got killed {e}')
            self.socket.close()
            sys.exit()


    def connect(self):
        self.socket.connect((self.args.target, self.args.port))
        try:
            while True:
                recv_len = 1 
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 1024:
                        break
                if response:
                    print(response)
                    buffer = f'{self.args.username}: ' +  input(f'{self.args.username} #> ')
                    self.socket.send(buffer.encode())
                    
                        
        except KeyboardInterrupt:
            print(f'\n@{self.args.username} logged out')
            self.socket.close()
            sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description= "The Matrix chatroom </> by @killfaggunati",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent('''Example:
            matrix_chat.py -t 127.0.0.1 -p 5555 -l # start the server
            matrix_chat.py -t 127.0.0.1 -p 5555 -u killfaggunati # join with username
            ''')
            )
    parser.add_argument('-t','--target', default='127.0.0.1', help='IPv4 of the server')
    parser.add_argument('-p','--port', default=5555, help='port of the server')
    parser.add_argument('-l','--listen', action='store_true', help='start the server')
    parser.add_argument('-u','--username',help='set a username')
    args = parser.parse_args()
    mc = MatrixChat(args)
    mc.run()
