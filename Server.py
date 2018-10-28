import socket
import threading


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(('127.0.0.1', 6000))

    server.listen(10)
    print("server is now listening")
    while 1:
        conn, addr = server.accept()
        print("new connection")
        print(addr)
        handlerThread = threading.Thread(target=clientHandler, args=(conn,))
        handlerThread.start()


def clientHandler(client):
    buffer_size = 128
    buffer = client.recv(buffer_size)
    client_request = buffer
    while len(buffer) == buffer_size:
        buffer = client.recv(buffer_size)
        client_request += buffer
    # tmp = client_request[client_request.find(b'Host'):]
    # tmp = tmp[len('host: '):tmp.find(b'\n')]
    # host = tmp[:-1].decode("utf-8")

    print(client_request)

    # path = client_request.split()[1]
    # print(path)
    # params = path[path.find(b'?') + 1:]
    # print(params)
    # print(params.split(b'&'))
    # print(host)


if __name__=="__main__":
    server()
