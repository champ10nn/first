import socket, sys
import argparse
import select

HEADER = 12
HOST = '127.0.0.1'
PORT = 12345

def create_message(msg):
    return f"{len(msg):<{HEADER}}" + msg

def recv_message(msg):
    msglen = int(msg[:HEADER])
    msg = msg[HEADER:]

    if msglen == len(msg):
        return msg
    return ""

def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    print(f"Listening at ({host}, {port})")
    while True:
        sc, sockname = sock.accept()
        print(f"{sockname} joined")

        while True:
            msg = recv_message(sc.recv(2048).decode('utf-8'))
            #...
def client(host, port):
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect((host, port))

    while True:
        try:
            socket_list = [sys.stdin, client_socket]
            read_sockets, write_socket, error_sockets = select.select(socket_list, [], [])

            for sock in read_sockets:
                if sock == client_socket:
                    msg = recv_message(sock.recv(2048).decode('utf-8'))
                    print(msg)
                else:
                    msg = sys.stdin.readline()
                    client_socket.send(create_message(msg))
        except KeyboardInterrupt:
            client_socket.close()
            sys.exit()

def main():
    choices = {'server': server, 'client': client}
    parser = argparse.ArgumentParser()
    parser.add_argument(description="Name of the app")
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='which host ip address to assign')
    parser.add_argument('-p', metavar="PORT", help='which port number to assign')
    
    args = parser.parse_args()
    func = choices[args.choices]
    func(choices.host, choices.port)


if __name__ == "__main__":
    main()

