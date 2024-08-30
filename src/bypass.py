import http.client
import threading
import os
from colorama import Fore, Style, init



class ReqBypass:
    def __init__(self):
 
        self.request_info = {}
        self.http_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "CONNECT", "TRACE"]
        self.body_content = ""
        self.headers = {}
        self.forward_headers_base = ["CACHE_INFO: 127.0.0.1", "CF_CONNECTING_IP: 127.0.0.1", "CF-Connecting-IP: 127.0.0.1", "CLIENT_IP: 127.0.0.1", "Client-IP: 127.0.0.1", "COMING_FROM: 127.0.0.1", "CONNECT_VIA_IP: 127.0.0.1", "FORWARD_FOR: 127.0.0.1", "FORWARD-FOR: 127.0.0.1", "FORWARDED_FOR_IP: 127.0.0.1", "FORWARDED_FOR: 127.0.0.1", "FORWARDED-FOR-IP: 127.0.0.1", "FORWARDED-FOR: 127.0.0.1", "FORWARDED: 127.0.0.1", "HTTP-CLIENT-IP: 127.0.0.1", "HTTP-FORWARDED-FOR-IP: 127.0.0.1", "HTTP-PC-REMOTE-ADDR: 127.0.0.1", "HTTP-PROXY-CONNECTION: 127.0.0.1", "HTTP-VIA: 127.0.0.1", "HTTP-X-FORWARDED-FOR-IP: 127.0.0.1", "HTTP-X-IMFORWARDS: 127.0.0.1", "HTTP-XROXY-CONNECTION: 127.0.0.1", "PC_REMOTE_ADDR: 127.0.0.1", "PRAGMA: 127.0.0.1", "PROXY_AUTHORIZATION: 127.0.0.1", "PROXY_CONNECTION: 127.0.0.1", "Proxy-Client-IP: 127.0.0.1", "PROXY: 127.0.0.1", "REMOTE_ADDR: 127.0.0.1", "Source-IP: 127.0.0.1", "True-Client-IP: 127.0.0.1", "Via: 127.0.0.1", "VIA: 127.0.0.1", "WL-Proxy-Client-IP: 127.0.0.1", "X_CLUSTER_CLIENT_IP: 127.0.0.1", "X_COMING_FROM: 127.0.0.1", "X_DELEGATE_REMOTE_HOST: 127.0.0.1", "X_FORWARDED_FOR_IP: 127.0.0.1",            "X_FORWARDED_FOR: 127.0.0.1", "X_FORWARDED: 127.0.0.1", "X_IMFORWARDS: 127.0.0.1", "X_LOCKING: 127.0.0.1", "X_LOOKING: 127.0.0.1", "X_REAL_IP: 127.0.0.1", "X-Backend-Host: 127.0.0.1", "X-BlueCoat-Via: 127.0.0.1", "X-Cache-Info: 127.0.0.1", "X-Forward-For: 127.0.0.1", "X-Forwarded-By: 127.0.0.1", "X-Forwarded-For-Original: 127.0.0.1", "X-Forwarded-For: 127.0.0.1", "X-Forwarded-For: 127.0.0.1, 127.0.0.1, 127.0.0.1", "X-Forwarded-Server: 127.0.0.1", "X-Forwarded-Host: 127.0.0.1", "X-From-IP: 127.0.0.1", "X-From: 127.0.0.1", "X-Gateway-Host: 127.0.0.1", "X-Host: 127.0.0.1", "X-Ip: 127.0.0.1", "X-Original-Host: 127.0.0.1", "X-Original-IP: 127.0.0.1", "X-Original-Remote-Addr: 127.0.0.1", "X-Original-Url: 127.0.0.1", "X-Originally-Forwarded-For: 127.0.0.1", "X-Originating-IP: 127.0.0.1", "X-ProxyMesh-IP: 127.0.0.1", "X-ProxyUser-IP: 127.0.0.1", "X-Real-IP: 127.0.0.1", "X-Remote-Addr: 127.0.0.1", "X-Remote-IP: 127.0.0.1", "X-True-Client-IP: 127.0.0.1", "XONNECTION: 127.0.0.1", "XPROXY: 127.0.0.1", "XROXY_CONNECTION: 127.0.0.1", "Z-Forwarded-For: 127.0.0.1", "ZCACHE_CONTROL: 127.0.0.1"]
        self.forward_headers = []
        self.headers_provided = False

    def parse_req_file(self, filename):
        lines = []
        headers = {}
        body_content = ""

        with open(filename) as file:
            lines = [line.rstrip() for line in file]

        if len(lines) == 0:
            print("Error in parsing the file")
            return headers, body_content  

        if len(lines[0].split()) == 3:
            method, endpoint, protocol = lines[0].split()
            if method not in self.http_methods:
                print("Error, the HTTP method was not recognized")
            else:
                self.request_info["method"] = method
                self.request_info["endpoint"] = endpoint
                self.request_info["protocol"] = protocol
        else:
            print("Error, the request file cannot be parsed")
            return headers, body_content   

        body_found = False
        for i in range(1, len(lines)):
            t = lines[i].split(":", 1) 
            if t[0] == "Host":
                self.request_info["Host"] = t[1].strip()

            if not body_found and len(lines[i].strip()) == 0:
                # Start of the body content
                body_content = '\n'.join(lines[i+1:])
                body_found = True
            elif not body_found:
                arr = lines[i].split(":", 1)   
                if len(arr) == 2:
                    headers[arr[0].strip()] = arr[1].strip()
                else:
                    print("Error, cannot parse the file")
        
        return headers, body_content

    def fuzz_headers(self, headers_chunk):
        for header in headers_chunk:
            if isinstance(header, tuple):
                header_name, header_value = header
            else:
                header_name, header_value = header.split(":", 1)

             
            local_headers = self.headers.copy()

            # Add the current header to the local headers
            local_headers[header_name.strip()] = header_value.strip()

            
            status, data = self.send_request(local_headers)

            if status == 200:
                print(f"{Fore.GREEN}Success, status code {status}{Style.RESET_ALL}")
                print(local_headers)
                print("\n\n")
            else:
                print(f"{Fore.RED}Error {status}{Style.RESET_ALL}")
                print(local_headers)

    def fuzz_in_threads(self, num_threads):
        f_headers = self.forward_headers if self.headers_provided else self.forward_headers_base
        threads = []
        chunk_size = (len(f_headers) + num_threads - 1) // num_threads  # Ceiling division to ensure all headers are covered

        # Split the list into chunks and create a thread for each chunk
        for i in range(0, len(f_headers), chunk_size):
            headers_chunk = f_headers[i:i + chunk_size]
            thread = threading.Thread(target=self.fuzz_headers, args=(headers_chunk,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def send_request(self, local_headers):
        host = self.request_info["Host"].strip()
        url = "http://" + host + self.request_info["endpoint"]
        method = self.request_info["method"]

        conn = http.client.HTTPConnection(host)

 
        conn.request(method, url, self.body_content, local_headers)
        response = conn.getresponse()

        response_data = response.read().decode()
        conn.close()

        return response.status, response_data


    def check_file(self, fname):
        return os.path.isfile(fname)



