import socket
import sys
import threading


def proxy():
    host = '127.0.0.1'
    port = 5000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket created")

    try:
        server.bind((host, port))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    print("server bind complete")

    server.listen(10)
    print("server is now listening")

    while 1:
        conn, addr = server.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        handlerThread = threading.Thread(target=clientHandler, args=(conn,))
        handlerThread.start()


def clientHandler(client):
    buffer_size = 500
    buffer = client.recv(buffer_size)
    client_request = buffer
    while len(buffer) == buffer_size:
        buffer = client.recv(buffer_size)
        client_request += buffer

    print(client_request)


if __name__ == "__main__":
    proxy()
