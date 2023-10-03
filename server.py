import socket
import threading

# server class that handles the requests
class Server:
    # initialize the server
    def __init__(self, port):
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', port))
        self.server_socket.listen(4)
        self.threads = []

    # start the server
    def start(self):
        while True:
            # Accept a connection from a client
            print(f'Listening on port {self.port}...')
            client_socket, client_addr = self.server_socket.accept()
            # Create a thread to handle the client
            thread = threading.Thread(target=self.handle_client, args=(client_socket, client_addr))
            thread.start()
            self.threads.append(thread)

    # handle the client
    def handle_client(self, client_socket, client_addr):
        # Receive the request from the client
        request = client_socket.recv(1024).decode()
        print(f'Request:\n{request}')
        # Split the request into the filename and the proxy chain
        request_lines = request.split('\n', 1)  # Split only on the first newline
        filename = request_lines[0]  # First line goes into 'filename'
        proxies = request_lines[1].split('\n')  # Split the remaining lines into 'proxies' array
        # If there are no proxies, then the server is the final destination
        if proxies[0] == '':
            self.send_file(client_socket, filename)
        else:
            # Connect to the next proxy in the chain
            next_proxy = proxies[0]
            next_proxy_ip, next_proxy_port = next_proxy.split(' ')
            next_proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            next_proxy_socket.connect((next_proxy_ip, int(next_proxy_port)))

            # modify the request to remove the first proxy
            request = f'{filename}\n'
            request += '\n'.join(proxies[1:])
            # Forward the request to the next proxy
            print(f'Forwarding request:\n{request} to {next_proxy}')
            next_proxy_socket.sendall(request.encode())

            # Receive the response from the next proxy
            print('Receiving response...')
            response = next_proxy_socket.recv(1024)
            print(f'Received response from {next_proxy}')

            # Forward the response to the client
            client_socket.sendall(response)

            # Close the connection to the next proxy
            next_proxy_socket.close()

        # Close the connection to the client
        client_socket.close()

    def send_file(self, client_socket, filename):
        print(f'Sending file {filename}...')
        # Send the file to the client
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break

                client_socket.sendall(data)
        
        client_socket.close()

if __name__ == '__main__':
    port = int(input('Enter port number: '))

    server = Server(port)
    server.start()