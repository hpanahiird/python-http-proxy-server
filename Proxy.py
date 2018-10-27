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
    buffer_size = 128
    buffer = client.recv(buffer_size)
    client_request = buffer
    while len(buffer) == buffer_size:
        buffer = client.recv(buffer_size)
        client_request += buffer
    tmp = client_request[client_request.find(b'Host'):]
    tmp = tmp[len('host: '):tmp.find(b'\n')]
    host = tmp[:-1].decode("utf-8")
    print(host)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, 80))
    # print(server)

    print(client_request)
    server.send(client_request)
    # print(server.recv(500))

    buffer = server.recv(buffer_size)
    client_response = buffer
    print(len(buffer))
    # read header
    while len(buffer) == buffer_size:
        buffer = server.recv(buffer_size)
        client_response += buffer
        print(len(buffer))
    # read body
    buffer = server.recv(buffer_size)
    client_response += buffer
    while len(buffer) == buffer_size:
        buffer = server.recv(buffer_size)
        client_response += buffer
        print(len(buffer))
    # print(server.recv(100))
    print(client_response)
    client.send(client_response)
    server.close()
    client.close()


if __name__ == "__main__":
    proxy()
