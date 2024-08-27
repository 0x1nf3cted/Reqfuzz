import http.client
import sys
import threading
from colorama import Fore, Style, init
init(autoreset=True)
# later on it can be loaded from a file
forward_headers = ["CACHE_INFO: 127.0.0.1", "CF_CONNECTING_IP: 127.0.0.1", "CF-Connecting-IP: 127.0.0.1", "CLIENT_IP: 127.0.0.1", "Client-IP: 127.0.0.1", "COMING_FROM: 127.0.0.1", "CONNECT_VIA_IP: 127.0.0.1", "FORWARD_FOR: 127.0.0.1", "FORWARD-FOR: 127.0.0.1", "FORWARDED_FOR_IP: 127.0.0.1", "FORWARDED_FOR: 127.0.0.1", "FORWARDED-FOR-IP: 127.0.0.1", "FORWARDED-FOR: 127.0.0.1", "FORWARDED: 127.0.0.1", "HTTP-CLIENT-IP: 127.0.0.1", "HTTP-FORWARDED-FOR-IP: 127.0.0.1", "HTTP-PC-REMOTE-ADDR: 127.0.0.1", "HTTP-PROXY-CONNECTION: 127.0.0.1", "HTTP-VIA: 127.0.0.1", "HTTP-X-FORWARDED-FOR-IP: 127.0.0.1", "HTTP-X-IMFORWARDS: 127.0.0.1", "HTTP-XROXY-CONNECTION: 127.0.0.1", "PC_REMOTE_ADDR: 127.0.0.1", "PRAGMA: 127.0.0.1", "PROXY_AUTHORIZATION: 127.0.0.1", "PROXY_CONNECTION: 127.0.0.1", "Proxy-Client-IP: 127.0.0.1", "PROXY: 127.0.0.1", "REMOTE_ADDR: 127.0.0.1", "Source-IP: 127.0.0.1", "True-Client-IP: 127.0.0.1", "Via: 127.0.0.1", "VIA: 127.0.0.1", "WL-Proxy-Client-IP: 127.0.0.1", "X_CLUSTER_CLIENT_IP: 127.0.0.1", "X_COMING_FROM: 127.0.0.1", "X_DELEGATE_REMOTE_HOST: 127.0.0.1", "X_FORWARDED_FOR_IP: 127.0.0.1",
           "X_FORWARDED_FOR: 127.0.0.1", "X_FORWARDED: 127.0.0.1", "X_IMFORWARDS: 127.0.0.1", "X_LOCKING: 127.0.0.1", "X_LOOKING: 127.0.0.1", "X_REAL_IP: 127.0.0.1", "X-Backend-Host: 127.0.0.1", "X-BlueCoat-Via: 127.0.0.1", "X-Cache-Info: 127.0.0.1", "X-Forward-For: 127.0.0.1", "X-Forwarded-By: 127.0.0.1", "X-Forwarded-For-Original: 127.0.0.1", "X-Forwarded-For: 127.0.0.1", "X-Forwarded-For: 127.0.0.1, 127.0.0.1, 127.0.0.1", "X-Forwarded-Server: 127.0.0.1", "X-Forwared-Host: 127.0.0.1", "X-From-IP: 127.0.0.1", "X-From: 127.0.0.1", "X-Gateway-Host: 127.0.0.1", "X-Host: 127.0.0.1", "X-Ip: 127.0.0.1", "X-Original-Host: 127.0.0.1", "X-Original-IP: 127.0.0.1", "X-Original-Remote-Addr: 127.0.0.1", "X-Original-Url: 127.0.0.1", "X-Originally-Forwarded-For: 127.0.0.1", "X-Originating-IP: 127.0.0.1", "X-ProxyMesh-IP: 127.0.0.1", "X-ProxyUser-IP: 127.0.0.1", "X-Real-IP: 127.0.0.1", "X-Remote-Addr: 127.0.0.1", "X-Remote-IP: 127.0.0.1", "X-True-Client-IP: 127.0.0.1", "XONNECTION: 127.0.0.1", "XPROXY: 127.0.0.1", "XROXY_CONNECTION: 127.0.0.1", "Z-Forwarded-For: 127.0.0.1", "ZCACHE_CONTROL: 127.0.0.1"]


request_info = {}
http_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "CONNECT", "TRACE"]
body_content = ""


def parse_req_file(filename):
    lines = []
    headers = {}
    body_content = ""  # Initialize body_content

    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    if len(lines) == 0:
        print("Error in parsing the file")
        return headers  # Early return if no lines are found

    if len(lines[0].split()) == 3:
        method, endpoint, protocol = lines[0].split()
        if method not in http_methods:
            print("Error, the HTTP method was not recognized")
        else:
            request_info["method"] = method
            request_info["endpoint"] = endpoint
            request_info["protocol"] = protocol
    else:
        print("Error, the request file cannot be parsed")
        return headers  # Early return if the header line is not in the expected format

    # Process lines for headers and body
    body_found = False
    for i in range(1, len(lines)):
        t = lines[i].split(":", 1) # to split only by the first occurance
        if t[0] == "Host":
            request_info["Host"] = t[1].strip()
        if(lines[i].split(":", 1)[0] == "Host"):
            request_info["Host"] = lines[i].split(":", 1)[1]
        if not body_found and len(lines[i].strip()) == 0:
            # Start of the body content
            body_content = '\n'.join(lines[i+1:])
            body_found = True
        elif not body_found:
            arr = lines[i].split(":", 1)  # Split only by the first occurrence
            if len(arr) == 2:
                headers[arr[0].strip()] = arr[1].strip()
            else:
                print("Error, cannot parse the file")
    
    return headers, body_content


def fuzz_headers(forward_headers):

 
    for header in forward_headers:
        status, data = send_request(header)
        if(status == 200):
            # print(f"Success, status code {status}")
            print(headers)
        else:
            print(f"Error {status}")




def fuzz_in_threads(forward_headers, num_threads):
    threads = []
    chunk_size = (len(forward_headers) + num_threads - 1) // num_threads  # Ceiling division to ensure all headers are covered

    # Split the list into chunks and create a thread for each chunk
    for i in range(0, len(forward_headers), chunk_size):
        headers_chunk = forward_headers[i:i + chunk_size]
        thread = threading.Thread(target=fuzz_headers, args=(headers_chunk,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()




def send_request(forward_header):
    # Create a new connection for each thread
    host = request_info["Host"].strip()
    url = "http://" + host + request_info["endpoint"]
    # add the single header to the rest of the request header
    h = forward_header.split(":", 1)

    print(h)
    if len(h) == 2:
        header_name = h[0].strip()
        header_value = h[1].strip()
        headers[header_name] = header_value
    else:
        print("Error in header parsing")
        return
    method = request_info["method"]

    conn = http.client.HTTPConnection(host)
    # Send the request
    conn.request(method, url, body_content, headers)
    response = conn.getresponse()
    
    response_data = response.read().decode()
    conn.close()

    del headers[header_name]

    return response.status, response_data



def not_a_hacking_tool_without_ascii_art():
 
    
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


def print_help_menu():
  
    print(f"""{Fore.YELLOW}{Style.BRIGHT}Reqfuzz Help Menu{Style.RESET_ALL}

Usage:
  python reqfuzz.py -h <file_name>  : Test multiple headers using the specified file.
  python reqfuzz.py -help           : Show this help menu.

Options:
  -h <file_name>                   : Specify a request file to test.
  -help                            : Display this help menu.

Examples:
  python reqfuzz.py -h request
    - This command will test the headers listed with the request file.

  python reqfuzz.py -help
    - This command will display this help menu.

Description:
  Reqfuzz is a tool for Bypassing http headers, and many more features.

{Fore.CYAN}{Style.BRIGHT}For more information and usage details, checkout https://github.com/0x1nf3cted.{Style.RESET_ALL}
    """)


if __name__ == "__main__":
    num_threads = 5
    threads = []

    if len(sys.argv) < 2:
        print("Usage: python3 reqfuzz.py -h <request file>")
    else:
        not_a_hacking_tool_without_ascii_art()
        match sys.argv[1]:
            case '-h': 
                # later on, we should check if the file exist
                filename = sys.argv[2]
                headers, body_content = parse_req_file(filename=filename)
                import time
                start_time = time.time()
                fuzz_in_threads(forward_headers, 20)
                print("--- %s seconds ---" % (time.time() - start_time))


            case '-help':
                print_help_menu()