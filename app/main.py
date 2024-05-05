import os.path
import socket
import sys
import threading


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        connection, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_request, args=([connection, client_address]))
        thread.start()


def get_user_agent(headers):
    for h in headers:
        if h.startswith('User-Agent: '):
            user_agent = h.replace('User-Agent: ', '')
    return user_agent


def handle_request(connection, client_address):
    print("Connection from", client_address)
    data = connection.recv(1024)
    data = data.decode()
    if (data != ''):
        startLine, headers = data.split('\r\n', 1)
        method, path, _ = startLine.split(' ', 2)
        headers = headers.split('\r\n')
        if method == 'GET':
            handle_get(path, connection, headers)
        if method == 'POST':
            handle_post(path, connection, headers)


def get_body(headers):
    end_of_headers = False
    body = ''
    for header in headers:
        if end_of_headers:
            body = body + header
        if (header == ''):
            end_of_headers = True
    return body

def handle_post(path, connection, headers):
    _, _, filename = path.split('/')
    flag = sys.argv[1]
    if (flag == '--directory'):
        directory = sys.argv[2]
        path_to_file = directory + '/' + filename
        body = get_body(headers)
        print('body: ' + body)
        f = open(path_to_file, "a")
        f.truncate(0)
        f.write(body)
        f.close()
        response = "HTTP/1.1 201 Created\r\n\r\n"
        connection.sendall(response.encode())
    return


def handle_file(path, connection):
    _, _, filename = path.split('/')
    flag = sys.argv[1]
    if (flag == '--directory'):
        directory = sys.argv[2]
        path_to_file = directory + '/' + filename
        if (os.path.isfile(path_to_file)):
            file = open(path_to_file, "r")
            file_contents = file.read()
            response = f"HTTP/1.1 200 OK\r\nContent-type: application/octet-stream\r\nContent-Length: {len(file_contents)}\r\n\r\n{file_contents}"
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    connection.sendall(response.encode())


def handle_get(path, connection, headers):
    if path.startswith('/user-agent'):
        userAgent = get_user_agent(headers)
        response = f"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-Length: {len(userAgent)}\r\n\r\n{userAgent}"
        connection.sendall(response.encode())
    elif path.startswith('/files'):
        handle_file(path, connection)
    elif path == '/':
        response = "HTTP/1.1 200 OK\r\n\r\n"
        connection.sendall(response.encode())
    elif path.startswith('/echo/'):
        _, _, requestString = path.split('/')
        response = f"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-Length: {len(requestString)}\r\n\r\n{requestString}"
        connection.sendall(response.encode())
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        connection.sendall(response.encode())
    connection.close()
    return


if __name__ == "__main__":
    main()

