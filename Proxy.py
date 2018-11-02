import socket
import sys
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import json
import ast


def proxy():
    # key = RSA.import_key(b'-----BEGIN RSA PRIVATE KEY-----\nMIICXgIBAAKBgQDo1cbUa/keHACfZkRAJ0A985pKmKoYbeWgKhmabyoJ1XetO+B3\nyvDz4RB/wcDkIUlntOkUdhxIDji0kpI4cVS8zjiPgC/ZcJV38r8iAjDc4+VoySWq\nr8NpR6HdjQM/xGZiHLdbZezSTNek+AiUT5jexULybaC1/647gRescORriwIDAQAB\nAoGAFB582tglo5tp1lxA44ZAv9mv6Gg+snO0lt1sbvLSIB1pBPgakl9f6ML26QM2\nBsB1lleEmHcIRJWuArRznBr25lt3gok0dJ1qd59thfduTaiFt+7oS+IDzVImGURd\nYJIv7FXwnxz9DY4beASabT+nCEPA59BHupAIxMeRm++UlbECQQDrye7qVyAhdyTG\nJlZu+x+y1IlLtf7/sNfexARveXeQmnUYITjLPr6I2HfwqAbzSVlLa2yko61a8c9w\nO/+4NF1TAkEA/MsHFGC1+Dq2XDyxflALc12cmjjM5mD8GOyFaywp9PAz0PaloMZ2\ntrSJHA+vk+al2lkxMmI2FgGvivDxmzw56QJBAN7v/iqqGCIsMaP8qaqjXBRM6keg\nm6sMfP8OnRb9ZTRfJimbd8SL3cEr0zPC21d6Wah6uK1uaMFdcwIuaJm1QSsCQQDa\nDP6UUz9jWLGIKkon3D+kSXEVjj0f0zRhA1OqODQQtUjczIPdhJNN0bga3mTivKb/\nCsRm41Qn81hKDr842eBRAkEA1PeLm+ADpQXgGYvAj3x+cLHYnJQMrH2eIUjoxE6+\nW7sqxQwfIK4TNFO64teD2v+epSCxNiw9cm67H4S0SAfzgA==\n-----END RSA PRIVATE KEY-----')

    # print(key.export_key())

    # decryptor = PKCS1_OAEP.new(key)
    # decrypted = decryptor.decrypt(ast.literal_eval(str(encrypted)))
    # print(decrypted)

    # en=publickey.encrypt('gfrgnurgtbybgy',32)
    # print(en)
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
    port = "80"
    if host.find(":") > 0:
        port = host[host.find(":") + 1:]
        host = host[0:host.find(":")]
    print(port)
    print(host)
    path = client_request.split()[1]
    params = path[path.find(b'?') + 1:]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, int(port)))

    publickey = RSA.import_key(
        b'-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDo1cbUa/keHACfZkRAJ0A985pK\nmKoYbeWgKhmabyoJ1XetO+B3yvDz4RB/wcDkIUlntOkUdhxIDji0kpI4cVS8zjiP\ngC/ZcJV38r8iAjDc4+VoySWqr8NpR6HdjQM/xGZiHLdbZezSTNek+AiUT5jexULy\nbaC1/647gRescORriwIDAQAB\n-----END PUBLIC KEY-----')
    encryptor = PKCS1_OAEP.new(publickey)

    # ebuffer = b''
    encrypted = b''
    lllll = []
    for i in range(0, int(len(params) / 86)):
        ebuffer = encryptor.encrypt(params[i * 86:(i + 1) * 86])
        encrypted += ebuffer
        lllll.append(str(ebuffer)[2:-1])
    ebuffer = encryptor.encrypt(params[int(len(params) / 86) * 86:])
    encrypted += ebuffer
    lllll.append(str(ebuffer)[2:-1])
    # print(encrypted)
    # print(lllll.__getitem__(0)+lllll.__getitem__(1))
    stri = json.dumps(lllll)
    print(stri)

    print(stri.encode())

    # print(encrypted)

    req_header = client_request[:client_request.find(b'\r\n\r\n')]
    print("header")
    method = req_header[:req_header.find(b' ')]
    print(req_header.replace(method, b'POST', 1))

    req = req_header.replace(method, b'POST', 1) + b'\r\n' + b'Content-Length: ' + str(len(encrypted)).encode(
        "ascii") + b'\r\n\r\n' + encrypted + b'\r\n\r\n'
    print("req")
    print(req)

    server.send(req)
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
    # server.close()
    client.close()
    print("closed")


if __name__ == "__main__":
    proxy()
