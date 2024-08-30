from colorama import Fore, Style, init
import os
import http.client


class RequestFileParser:
    def __init__(self):
        self.request_info = {}
        self.body_content = ""
        self.headers = {}
        self.http_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "CONNECT", "TRACE"]

    def parse_req_file(self, filename):
        lines = []
        headers = {}
        body_content = ""

        # Read the file and remove trailing spaces
        with open(filename) as file:
            lines = [line.rstrip() for line in file]

        if len(lines) == 0:
            print("Error: The request file is empty or could not be read.")
            return headers, self.request_info, body_content  

        # Parse the request line (first line in the file)
        if len(lines[0].split()) == 3:
            method, endpoint, protocol = lines[0].split()
            if method not in self.http_methods:
                print(f"Error: HTTP method '{method}' not recognized.")
                return headers, self.request_info, body_content
            else:
                self.request_info["method"] = method
                self.request_info["endpoint"] = endpoint
                self.request_info["protocol"] = protocol
        else:
            print("Error: The request file cannot be parsed.")
            return headers, self.request_info, body_content   

        # Parse headers and body
        body_found = False
        for i in range(1, len(lines)):
            if not body_found and len(lines[i].strip()) == 0:
                # Empty line indicates start of the body content
                body_content = '\n'.join(lines[i+1:])
                body_found = True
            elif not body_found:
                # Parse headers
                arr = lines[i].split(":", 1)
                if len(arr) == 2:
                    headers[arr[0].strip()] = arr[1].strip()
                    if arr[0].strip().lower() == "host":
                        self.request_info["Host"] = arr[1].strip()
                else:
                    print(f"Error: Cannot parse the header '{lines[i]}'.")
                    return headers, self.request_info, body_content
        
        return headers, self.request_info, body_content




    def send_request(self, local_headers, request_dest, body_content):
        host = request_dest.get("Host", "").strip()
        if not host:
            print("Error: Host is not specified.")
            return None, None
        
        url = "http://" + host + request_dest["endpoint"]
        method = request_dest["method"]

        conn = http.client.HTTPConnection(host) 
        conn.request(method, request_dest["endpoint"], body_content, local_headers)
        response = conn.getresponse()

        response_data = response.read().decode()
        conn.close()

        return response.status, response_data


    def print_header(self, headers, request_body):
        print(f"{Fore.YELLOW}_____________________________________________________________________")
        print(f"{Fore.YELLOW}_____________________________________________________________________")
        print(f"{Fore.LIGHTMAGENTA_EX}headers\n")
        for k, v in headers.items():
            print(f"{k}: {v}")
        print("\n")
        print(f"{Fore.LIGHTMAGENTA_EX}body\n")
        print(request_body)

        print(f"{Fore.YELLOW}_____________________________________________________________________")

    def print_response(self, status, data):
        if(status == 200):
            print(f"{Fore.GREEN}status: {status}\n")
            print("reponse data:\n")
            print(f"{Fore.LIGHTGREEN_EX}data: {data}")
        else:
            print(f"{Fore.RED}status: {status}\n")
            print("reponse data:\n")
            print(f"{Fore.LIGHTRED_EX}data: {data}")
        print(f"{Fore.YELLOW}_____________________________________________________________________")
        print(f"{Fore.YELLOW}_____________________________________________________________________")
            

    def check_file(self, fname):
        return os.path.isfile(fname)




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
{Fore.GREEN}{Style.BRIGHT}Reqfuzz is a tool for Fuzzing request headers, and many more features (to come).
{Style.RESET_ALL}
    """
    print(description)

def print_help_menu():
    print(f"""
{Fore.YELLOW}{Style.BRIGHT}ReqFuzz Help Menu{Style.RESET_ALL}

    Usage:
    python reqfuzz.py -b <request_file>                   : Fuzz HTTP headers using the specified request file.
    python reqfuzz.py -b <request_file> -h <header_file>  : Fuzz HTTP headers with additional headers from the specified header file.
    python reqfuzz.py -f request -p <payload_file>        : Fuzz HTTP headers using the specified payload file.
    python reqfuzz.py -help                               : Show this help menu.

    Options:
    -b <request_file>  : Specify a file with the HTTP request details (method, endpoint, protocol, headers, body) you can get it from intercepting the request.
    -h <header_file>   : Provide a file with additional headers to test.
    -f request         : Indicate that the tool should fuzz the request headers.
    -p <payload_file>  : Specify a file with payloads to replace the 'FUZZ' placeholder in the headers.
    -help              : Display this help menu.

    {Fore.CYAN}{Style.BRIGHT}For more information and updates, visit https://github.com/0x1nf3cted.{Style.RESET_ALL}
    """)
