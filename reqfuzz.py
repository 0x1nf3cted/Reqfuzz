import http.client
import sys
import threading
import os
from colorama import Fore, Style, init

 
init(autoreset=True)

class ReqFuzz:
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

    def not_a_hacking_tool_without_ascii_art(self):
        ascii_art = f"""
{Fore.MAGENTA}{Style.NORMAL}
 ███████████                         ██████                                  
░░███░░░░░███                       ███░░███                                 
 ░███    ░███   ██████   ████████  ░███ ░░░  █████ ████  █████████  █████████
 ░██████████   ███░░███ ███░░███  ███████   ░░███ ░███  ░█░░░░███  ░█░░░░███ 
 ░███░░░░░███ ░███████ ░███ ░███ ░░░███░     ░███ ░███  ░   ███░   ░   ███░  
 ░███    ░███ ░███░░░  ░███ ░███   ░███      ░███ ░███    ███░   █   ███░   █
 █████   █████░░██████ ░░███████   █████     ░░████████  █████████  █████████
░░░░░   ░░░░░  ░░░░░░   ░░░░░███  ░░░░░       ░░░░░░░░  ░░░░░░░░░  ░░░░░░░░░ 
                            ░███                                             
                            █████                                            
                           ░░░░░
  {Style.RESET_ALL}"""
        print(f"{Fore.RED}{Style.BRIGHT}can't be a hacking tool without some cool Ascii art ;){Style.RESET_ALL}")
        print(ascii_art)

        description = f"""
{Fore.GREEN}{Style.BRIGHT}Reqfuzz is a tool for Bypassing http headers, and many more features (to come).
{Style.RESET_ALL}
    """
        print(description)

    def print_help_menu(self):
        print(f"""
{Fore.YELLOW}{Style.BRIGHT}ReqFuzz Help Menu{Style.RESET_ALL}

    Usage:
    python reqfuzz.py -b <request_file>  : Fuzz HTTP headers using the specified request file.
    python reqfuzz.py -b <request_file> -h <header_file>  : Fuzz HTTP headers with additional headers from the specified header file.
    python reqfuzz.py -help              : Show this help menu.

    Options:
    -b <request_file>  : Specify a file with the HTTP request details (method, endpoint, protocol, headers, body) you can get it from intercepting the request.
    -h <header_file>   : Provide a file with additional headers to test.
    -help              : Display this help menu.

    {Fore.CYAN}{Style.BRIGHT}For more information and updates, visit https://github.com/0x1nf3cted.{Style.RESET_ALL}
        """)



    def check_file(self, fname):
        return os.path.isfile(fname)


def run():
    fuzzer = ReqFuzz()

    if len(sys.argv) < 2:
        print("Usage: python3 reqfuzz.py -h <request file>")
        return

    fuzzer.not_a_hacking_tool_without_ascii_art()

    match sys.argv[1]:
        case '-b':
            if len(sys.argv) >= 5 and sys.argv[3] == "-h":
                header_file = sys.argv[4]
                if not fuzzer.check_file(header_file):
                    print(f"{Fore.RED}Error, the header file that you provided doesn't exist")
                    fuzzer.print_help_menu()
                    return
                else:
                    fuzzer.headers_provided = True
                    with open(header_file) as file:
                        fuzzer.forward_headers = [line.rstrip() for line in file]
            elif len(sys.argv) == 4:
                print(f"{Fore.RED}Error, number of arguments is not enough")
                fuzzer.print_help_menu()
                return

            filename = sys.argv[2]
            if not fuzzer.check_file(filename):
                print(f"{Fore.RED}Error, the request file that you provided doesn't exist")
                fuzzer.print_help_menu()
                return

            fuzzer.headers, fuzzer.body_content = fuzzer.parse_req_file(filename)

            import time
            start_time = time.time()
            fuzzer.fuzz_in_threads(20)
            print("--- %s seconds ---" % (time.time() - start_time))


        case _:
            print(f"{Fore.RED}Error, can't recognize the argument")
            fuzzer.print_help_menu()
    


if __name__ == "__main__":
    run()
