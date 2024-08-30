import http.client
import threading
import os
from colorama import Fore, Style, init

from src.utils import RequestFileParser



class ReqBypass:
    def __init__(self):
        self.request_parser = RequestFileParser()
        self.forward_headers_base = ["CACHE_INFO: 127.0.0.1", "CF_CONNECTING_IP: 127.0.0.1", "CF-Connecting-IP: 127.0.0.1", "CLIENT_IP: 127.0.0.1", "Client-IP: 127.0.0.1", "COMING_FROM: 127.0.0.1", "CONNECT_VIA_IP: 127.0.0.1", "FORWARD_FOR: 127.0.0.1", "FORWARD-FOR: 127.0.0.1", "FORWARDED_FOR_IP: 127.0.0.1", "FORWARDED_FOR: 127.0.0.1", "FORWARDED-FOR-IP: 127.0.0.1", "FORWARDED-FOR: 127.0.0.1", "FORWARDED: 127.0.0.1", "HTTP-CLIENT-IP: 127.0.0.1", "HTTP-FORWARDED-FOR-IP: 127.0.0.1", "HTTP-PC-REMOTE-ADDR: 127.0.0.1", "HTTP-PROXY-CONNECTION: 127.0.0.1", "HTTP-VIA: 127.0.0.1", "HTTP-X-FORWARDED-FOR-IP: 127.0.0.1", "HTTP-X-IMFORWARDS: 127.0.0.1", "HTTP-XROXY-CONNECTION: 127.0.0.1", "PC_REMOTE_ADDR: 127.0.0.1", "PRAGMA: 127.0.0.1", "PROXY_AUTHORIZATION: 127.0.0.1", "PROXY_CONNECTION: 127.0.0.1", "Proxy-Client-IP: 127.0.0.1", "PROXY: 127.0.0.1", "REMOTE_ADDR: 127.0.0.1", "Source-IP: 127.0.0.1", "True-Client-IP: 127.0.0.1", "Via: 127.0.0.1", "VIA: 127.0.0.1", "WL-Proxy-Client-IP: 127.0.0.1", "X_CLUSTER_CLIENT_IP: 127.0.0.1", "X_COMING_FROM: 127.0.0.1", "X_DELEGATE_REMOTE_HOST: 127.0.0.1", "X_FORWARDED_FOR_IP: 127.0.0.1",            "X_FORWARDED_FOR: 127.0.0.1", "X_FORWARDED: 127.0.0.1", "X_IMFORWARDS: 127.0.0.1", "X_LOCKING: 127.0.0.1", "X_LOOKING: 127.0.0.1", "X_REAL_IP: 127.0.0.1", "X-Backend-Host: 127.0.0.1", "X-BlueCoat-Via: 127.0.0.1", "X-Cache-Info: 127.0.0.1", "X-Forward-For: 127.0.0.1", "X-Forwarded-By: 127.0.0.1", "X-Forwarded-For-Original: 127.0.0.1", "X-Forwarded-For: 127.0.0.1", "X-Forwarded-For: 127.0.0.1, 127.0.0.1, 127.0.0.1", "X-Forwarded-Server: 127.0.0.1", "X-Forwarded-Host: 127.0.0.1", "X-From-IP: 127.0.0.1", "X-From: 127.0.0.1", "X-Gateway-Host: 127.0.0.1", "X-Host: 127.0.0.1", "X-Ip: 127.0.0.1", "X-Original-Host: 127.0.0.1", "X-Original-IP: 127.0.0.1", "X-Original-Remote-Addr: 127.0.0.1", "X-Original-Url: 127.0.0.1", "X-Originally-Forwarded-For: 127.0.0.1", "X-Originating-IP: 127.0.0.1", "X-ProxyMesh-IP: 127.0.0.1", "X-ProxyUser-IP: 127.0.0.1", "X-Real-IP: 127.0.0.1", "X-Remote-Addr: 127.0.0.1", "X-Remote-IP: 127.0.0.1", "X-True-Client-IP: 127.0.0.1", "XONNECTION: 127.0.0.1", "XPROXY: 127.0.0.1", "XROXY_CONNECTION: 127.0.0.1", "Z-Forwarded-For: 127.0.0.1", "ZCACHE_CONTROL: 127.0.0.1"]
        self.forward_headers = []
        self.request_info = {}
        self.body_content = ""
        self.headers_provided = False

    def parse_req_file(self, filename):
        self.headers, self.request_info, self.body_content = self.request_parser.parse_req_file(filename)
        # Optionally update self.request_info here if needed

    def fuzz_headers(self, headers_chunk):
        for header in headers_chunk:
            if isinstance(header, tuple):
                header_name, header_value = header
            else:
                header_name, header_value = header.split(":", 1)

            local_headers = self.headers.copy()
            local_headers[header_name.strip()] = header_value.strip()

            status, data = self.request_parser.send_request(local_headers, self.request_info, self.body_content)

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
            thread.join(timeout=10)

