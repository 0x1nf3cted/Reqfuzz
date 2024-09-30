import socket
import ssl
import threading
from urllib.parse import urlparse

BUFFER_SIZE = 4096

CERT_FILE = "cert.pem"
KEY_FILE = "cert.pem"


class Proxy:
    def __init__(self, port_number):
        self.listen_host = "127.0.0.1"  
        self.listen_port = port_number       

    def relay_data(self, client_ssl_socket, server_ssl_socket):
        while True:
 
            client_data = client_ssl_socket.recv(BUFFER_SIZE)
            if len(client_data) > 0:
 
                try:
                    print(f"[Intercepted Client Request]\n{client_data.decode('utf-8', 'ignore')}\n")
                except Exception as e:
                    print(f"Error printing client request: {e}")

                server_ssl_socket.sendall(client_data)
            else:
                break


            server_data = server_ssl_socket.recv(BUFFER_SIZE)
            if len(server_data) > 0:

                client_ssl_socket.sendall(server_data)
            else:
                break


        server_ssl_socket.close()


    def handle_https_client(self, client_socket, addr):
        try:

            full_request = b''
            
            while True:
                # Keep receiving data until the request headers are fully received
                request_chunk = client_socket.recv(BUFFER_SIZE)
                full_request += request_chunk
                if b'\r\n\r\n' in full_request or len(request_chunk) == 0:
                    break

            request_str = full_request.decode('utf-8', 'ignore')
            request_lines = request_str.splitlines()

            print(f"[Intercepted HTTPS Request]\n{request_str}\n")

            f = open("request", "w")
            f.write(request_str)
            f.close()


            request_line = request_lines[0]
            if request_line.startswith("CONNECT"):
                target_host_port = request_line.split(' ')[1]
            else:
                # Extract the hostname and port from the full URL in a POST or GET request
                url = request_line.split(' ')[1]
                parsed_url = urlparse(url)
                target_host_port = f"{parsed_url.hostname}:{parsed_url.port or 443}"

            print(f"[Parsed Target] {target_host_port}")

            target_host, target_port = target_host_port.split(":")
            target_port = int(target_port)

            # Send a "200 Connection Established" response to the client
            client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")

            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
            client_ssl_socket = context.wrap_socket(client_socket, server_side=True)

            try:
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_ssl_socket = ssl.wrap_socket(server_socket)
                server_ssl_socket.connect((target_host, target_port))

    
                self.relay_data(client_ssl_socket, server_ssl_socket)

            except Exception as e:
                print(f"Error connecting to server: {e}")

 
            client_ssl_socket.close()

        except Exception as e:
            print(f"Error handling HTTPS client: {e}")
            client_socket.close()

    def start_proxy(self):

        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.bind((self.listen_host, self.listen_port))
        proxy_socket.listen(5)

        print(f"[Proxy] Listening on {self.listen_host}:{self.listen_port}")

        while True:

            client_socket, addr = proxy_socket.accept()
            print(f"[Proxy] Accepted connection from {addr}")


            client_thread = threading.Thread(target=self.handle_https_client, args=(client_socket, addr))
            client_thread.start()
