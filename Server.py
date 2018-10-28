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
    method = client_request[:client_request.find(b' ')]
    if method != b'POST':
        client.send(
            b'HTTP/1.0 405 Method Not Allowed\r\nServer: nginx/1.14.0 (Ubuntu)\r\nDate: Sun, 28 Oct 2018 14:08:03 GMT\r\nContent-Type: text/html\r\nContent-Length: 182\r\nConnection: close\r\n\r\n<html>\r\n<head><title>405 Not Allowed</title></head>\r\n<body bgcolor="white">\r\n<center><h1>405 Not Allowed</h1></center>\r\n<hr><center>nginx/1.14.0 (Ubuntu)</center>\r\n</body>\r\n</html>\r\n')
        client.close()
    else:
        print("allowed")
    # path = client_request.split()[1]
    # print(path)
    # params = path[path.find(b'?') + 1:]
    # print(params)
    # print(params.split(b'&'))
    # print(host)


if __name__=="__main__":
    server()
