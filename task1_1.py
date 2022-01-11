import argparse, socket
import sys
import select
import math

host = '127.0.0.1'
port = 1060

def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', port))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    while True:
        conn, addr = sock.accept()
        coordinates = {}
        print('We have accepted a connection from', addr)
        while True:
            try:
                message = conn.recv(1024)
                message = message.decode('utf-8').strip()
                keywords = message.split()
                if message == "end_session;":
                    conn.close()
                elif keywords[0] == "add" and message.endswith(';'):
                    city = keywords[1].strip(' :')
                    x = int(keywords[2].strip(' ,'))
                    y = int(keywords[3].strip(' ;'))
                    coordinates[city] = [x, y]
                elif keywords[0] == "distance" and message.endswith(';'):
                    city = keywords[1].strip('; ')
                    x1 = coordinates[city][0]
                    y1 = coordinates[city][1]
                    for key in coordinates:
                        if key != city:
                            x2 = coordinates[key][0]
                            y2 = coordinates[key][1]
                            distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                            response = key + ': ' + str(round(distance,3)) + '\n'
                            conn.sendall(response.encode('utf-8'))
            except KeyboardInterrupt:
                sys.exit()
            except:
                continue


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', port))
    keyword = input()
    if keyword.strip() == 'start_session;':
        while True:
            sockets_list = [sys.stdin, sock]
            read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
            for socks in read_sockets:
                if socks == sock:
                    print(sock.recv(1024).decode('utf-8'))
                else:
                    command = sys.stdin.readline()
                    sock.sendall(command.encode('utf-8'))
                    if command.strip() == "end_session;": 
                        sock.close()
                        sys.exit()
    else:
        print("You must start the session")
        print("The wrong format")
    sock.close()


if __name__ == "__main__":
    choices = {'server': server, 'client': client}
    parser = argparse.ArgumentParser(description="Compute the Euclidean distance")
    parser.add_argument('role', choices=choices, help='which role to play')
    args = parser.parse_args()
    function = choices[args.role]
    function()