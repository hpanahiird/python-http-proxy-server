import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def server():
    secure_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    secure_server.bind(('0.0.0.0', 7000))

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

    key = RSA.import_key(
        b'-----BEGIN RSA PRIVATE KEY-----\nMIICXgIBAAKBgQDo1cbUa/keHACfZkRAJ0A985pKmKoYbeWgKhmabyoJ1XetO+B3\nyvDz4RB/wcDkIUlntOkUdhxIDji0kpI4cVS8zjiPgC/ZcJV38r8iAjDc4+VoySWq\nr8NpR6HdjQM/xGZiHLdbZezSTNek+AiUT5jexULybaC1/647gRescORriwIDAQAB\nAoGAFB582tglo5tp1lxA44ZAv9mv6Gg+snO0lt1sbvLSIB1pBPgakl9f6ML26QM2\nBsB1lleEmHcIRJWuArRznBr25lt3gok0dJ1qd59thfduTaiFt+7oS+IDzVImGURd\nYJIv7FXwnxz9DY4beASabT+nCEPA59BHupAIxMeRm++UlbECQQDrye7qVyAhdyTG\nJlZu+x+y1IlLtf7/sNfexARveXeQmnUYITjLPr6I2HfwqAbzSVlLa2yko61a8c9w\nO/+4NF1TAkEA/MsHFGC1+Dq2XDyxflALc12cmjjM5mD8GOyFaywp9PAz0PaloMZ2\ntrSJHA+vk+al2lkxMmI2FgGvivDxmzw56QJBAN7v/iqqGCIsMaP8qaqjXBRM6keg\nm6sMfP8OnRb9ZTRfJimbd8SL3cEr0zPC21d6Wah6uK1uaMFdcwIuaJm1QSsCQQDa\nDP6UUz9jWLGIKkon3D+kSXEVjj0f0zRhA1OqODQQtUjczIPdhJNN0bga3mTivKb/\nCsRm41Qn81hKDr842eBRAkEA1PeLm+ADpQXgGYvAj3x+cLHYnJQMrH2eIUjoxE6+\nW7sqxQwfIK4TNFO64teD2v+epSCxNiw9cm67H4S0SAfzgA==\n-----END RSA PRIVATE KEY-----')
    decryptor = PKCS1_OAEP.new(key)
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

    body = client_request[client_request.find(b'\r\n\r\n') + len(b'\r\n\r\n'):-4]
    yyy = body.split(b'\n\n')
    decrypted = b''
    for i in range(0, len(yyy)):
        decrypted += decryptor.decrypt(yyy[i])
    print(decrypted)
    response = b'<html>\r\n' + b'<head><title>OKKKK</title></head>\r\n' + b'<body bgcolor="white">\r\n' + b'<center><h1>Allowed</h1></center>\r\n' + b'<hr><center>Your Securejnjrnghh Server</center>\r\n' + b'<br> <p>You sent us: ' + decrypted + b'</p></body>\r\n' + b'</html>\r\n'
    print(len(response))
    client.send(b'HTTP/1.0 200 OK\r\n'
                b'Server: nginx/1.14.0 (Ubuntu)\r\n'
                b'Date: Sun, 28 Oct 2018 14:08:03 GMT\r\n'
                b'Content-Type: text/html\r\n'
                b'Content-Length: '+bytes(len(response))+b'\r\n'
                b'Connection: close\r\n\r\n'
                b'<html>\r\n'
                b'<head><title>OKKKK</title></head>\r\n'
                b'<body bgcolor="white">\r\n'
                b'<center><h1>Allowed</h1></center>\r\n'
                b'<hr><center>Your Secure Server</center>\r\n'
                b'<br>'
                + decrypted +
                b'</body>\r\n'
                b'</html>\r\n'
                )

    client.close()


# path = client_request.split()[1]
# print(path)
# params = path[path.find(b'?') + 1:]
# print(params)
# print(params.split(b'&'))
# print(host)


if __name__ == "__main__":
    server()
