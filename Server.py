import socket


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(('127.0.0.1', 6000))

    server.listen(10)
    print("server is now listening")
    while 1:
        conn, addr = server.accept()
        print("new connection")
        print(addr)


if __name__=="__main__":
    server()
