import socket
import threading


def server():
    secure_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    secure_server.bind(('127.0.0.1', 6000))

    secure_server.listen(10)
    print("server is now listening")
    while 1:
        conn, addr = secure_server.accept()
        print("new connection")
        print(addr)
        handler_thread = threading.Thread(target=client_handler, args=(conn,))
        handler_thread.start()


def client_handler(client):
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
        client.send(b'HTTP/1.0 405 Method Not Allowed\r\n'
                    b'Server: nginx/1.14.0 (Ubuntu)\r\n'
                    b'Date: Sun, 28 Oct 2018 14:08:03 GMT\r\n'
                    b'Content-Type: text/html\r\n'
                    b'Content-Length: 182\r\n'
                    b'Connection: close\r\n\r\n'
                    b'<html>\r\n'
                    b'<head><title>405 Not Allowed</title></head>\r\n'
                    b'<body bgcolor="white">\r\n'
                    b'<center><h1>405 Not Allowed</h1></center>\r\n'
                    b'<hr><center>nginx/1.14.0 (Ubuntu)</center>\r\n'
                    b'</body>\r\n'
                    b'</html>\r\n')
        client.close()
        return

    body = client_request[client_request.find(b'\r\n\r\n')+len(b'\r\n\r\n'):]
    print(body)


    # path = client_request.split()[1]
    # print(path)
    # params = path[path.find(b'?') + 1:]
    # print(params)
    # print(params.split(b'&'))
    # print(host)


if __name__ == "__main__":
    server()
