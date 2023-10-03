import socket

# Client class
class Client:
    # Initialize the client with the filename and proxy chain
    def __init__(self, filename, proxy_chain):
        self.filename = filename
        self.proxy_chain = proxy_chain

    # Connect to the first proxy in the chain
    def connect(self):
        # Create a socket to the first proxy in the chain
        proxy_ip, proxy_port = self.proxy_chain[0].split(' ')
        print(proxy_ip, proxy_port)
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.connect((proxy_ip, int(proxy_port)))

        print(f'Client connected to {self.proxy_chain[0]}')

        # Forward the request to the first proxy
        request = f'{self.filename}\n'
        request += '\n'.join(self.proxy_chain[1:])
        proxy_socket.sendall(request.encode())

        # Receive the response from the first proxy
        print('Receiving response...')
        response = proxy_socket.recv(1024)

        # Save the response to a file
        with open("client_file.txt", 'wb') as f:
            f.write(response)

def read_input_file(filename):
    # Read the input file
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        print(lines)

        # Split the first line into the filename and the proxy chain
        filename = lines[0]
        proxies = lines[1:]

        return filename, proxies

if __name__ == '__main__':
    # Get the filename and proxy chain from the input file
    filename, proxy_chain = read_input_file('input.txt')

    client = Client(filename, proxy_chain)
    client.connect()