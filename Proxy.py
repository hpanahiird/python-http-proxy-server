import socket
import sys
import threading


def proxy():
    host = '127.0.0.1'
    port = 5000
    proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket created")

    try:
        proxy_server.bind((host, port))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    print("server bind complete")

    proxy_server.listen(10)
    print("server is now listening")

    while 1:
        conn, addr = proxy_server.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        handler_thread = threading.Thread(target=client_handler, args=(conn,))
        handler_thread.start()


def client_handler(client):
    buffer_size = 128
    buffer = client.recv(buffer_size)
    client_request = buffer
    while len(buffer) == buffer_size:
        buffer = client.recv(buffer_size)
        client_request += buffer
    tmp = client_request[client_request.find(b'Host'):]
    tmp = tmp[len('host: '):tmp.find(b'\n')]
    host = tmp[:-1].decode("utf-8")

    print(client_request)
    path = client_request.split()[1]
    print(path)
    params = path[path.find(b'?') + 1:]
    print(params)
    print(params.split(b'&'))
    print(host)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, 80))
    # print(server)

    server.send(client_request)
    # print(server.recv(500))

    buffer = server.recv(buffer_size)
    client_response = buffer
    print(len(buffer))
    # read header
    while len(buffer) == buffer_size:
        buffer = server.recv(buffer_size)
        client_response += buffer
        # print(len(buffer))

    print(client_response)
    # read body
    buffer = server.recv(buffer_size)
    client_response += buffer
    while len(buffer) == buffer_size:
        buffer = server.recv(buffer_size)
        client_response += buffer
        # print(len(buffer))
    # print(server.recv(100))
    print(client_response)
    client.send(client_response)
    server.close()
    client.close()


if __name__ == "__main__":
    proxy()
