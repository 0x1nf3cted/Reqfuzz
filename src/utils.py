import threading
from colorama import Fore, Style, init
import os
import http.client
import time
import re


class RequestFileParser:
    def __init__(self):
        self.request_info = {}
        self.global_conditions = {}
        self.with_condition = False
        self.body_content = ""
        self.headers = {}
        self.threads = 0
        self.http_methods = ["GET", "POST", "PUT", "DELETE",
                             "PATCH", "HEAD", "OPTIONS", "CONNECT", "TRACE"]

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
        response_metrics = {
            "status": "",
            "size": "",
            "type": "",
            "time": ""
        }

        host = request_dest.get("Host", "").strip()
        if not host:
            print("Error: Host is not specified.")
            return None, None

        url = "http://" + host + request_dest["endpoint"]
        method = request_dest["method"]

        conn = http.client.HTTPConnection(host)

        # calculate reponse time

        start_time = time.time()
        conn.request(
            method, request_dest["endpoint"], body_content, local_headers)
        response = conn.getresponse()
        response_metrics["time"] = time.time() - start_time

        # calculate the size of a response
        content_length = response.getheader('Content-Length')
        if content_length is not None:
            response_metrics["size"] = int(content_length)
        else:
            response_metrics["size"] = len(response.read())

        content_type = response.getheader('Content-Type')
        if content_type is not None:
            response_metrics["type"] = int(content_length)
        response_metrics["status"] = response.status

        response_data = response.read().decode()
        conn.close()

        return response_metrics, response_data

    def parse_time_condition(condition: str, time_value: str):

        condition_pattern = r'([><=!]=?|!=)\s*(\d+(?:\.\d+)?)\s*(ms|s)'
        time_pattern = r'(\d+(?:\.\d+)?)\s*(ms|s)'

        condition_match = re.match(condition_pattern, condition.strip())
        if not condition_match:
            raise ValueError(f"Invalid time condition: {condition}")

        operator = condition_match.group(1)
        condition_value = float(condition_match.group(2))
        condition_unit = condition_match.group(3)

        if condition_unit == 's':
            condition_value *= 1000

        time_match = re.match(time_pattern, time_value.strip())
        if not time_match:
            raise ValueError(f"Invalid time value: {time_value}")

        check_value = float(time_match.group(1))
        time_unit = time_match.group(2)

        if time_unit == 's':
            check_value *= 1000

        if operator == '>':
            return check_value > condition_value
        elif operator == '<':
            return check_value < condition_value
        elif operator == '>=':
            return check_value >= condition_value
        elif operator == '<=':
            return check_value <= condition_value
        elif operator == '=' or operator == '==':
            return check_value == condition_value
        elif operator == '!=':
            return check_value != condition_value
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def parse_conditions(self, conditions):
        print(conditions)
        c = conditions.split(";")
        for cond in c:
            cond = cond.split(":", 1)
            if (len(cond) != 2):
                print("Error, condition format is corrupted")
                exit()
            if (self.global_conditions[cond[0].strip()] not in ["size", "status", "type", "time"]):
                print("Error: condition is not recognized")
            else:
                self.global_conditions[cond[0].strip()] = cond[1].strip()
        print(self.global_conditions)

    def thread_worker(self, payload, function):
        threads = []
        # Ceiling division to ensure all headers are covered
        chunk_size = (len(payload) + self.threads - 1) // self.threads
        print("on")
        for i in range(0, len(payload), chunk_size):
            chunks = payload[i:i + chunk_size]
            thread = threading.Thread(target=function, args=(chunks,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join(timeout=10)

    def print_header(self, headers, request_body):
        print(
            f"{Fore.YELLOW}_____________________________________________________________________")
        print(
            f"{Fore.YELLOW}_____________________________________________________________________")
        print(f"{Fore.LIGHTMAGENTA_EX}headers\n")
        for k, v in headers.items():
            print(f"{k}: {v}")

        if (len(request_body) != 0):
            print("\n")
            print(f"{Fore.LIGHTMAGENTA_EX}body\n")
            print(request_body)

        print(
            f"{Fore.YELLOW}_____________________________________________________________________")

    def print_response(self, data, response_metrics):
        status = int(response_metrics.get("status", 0))
        time = response_metrics.get("time", "0ms")
        type = response_metrics.get("type", "")
 
        size = response_metrics.get("size", 0)

        if self.with_condition:

            status_condition = self.global_conditions.get("status")
            if status_condition:

                if not eval(f"{status} {status_condition}"):
                    return

            time_condition = self.global_conditions.get("time")
            if time_condition:

                if not self.parse_time_condition(time_condition, time):
                    return

            type_condition = self.global_conditions.get("type")
            if type_condition:
                if type != type_condition:
                    return

            size_condition = self.global_conditions.get("size")
            if size_condition:

                if not eval(f"{size} {size_condition}"):
                    return

        print(f"{Fore.GREEN}status: {status}\n")
        print("reponse data:\n")
        print(f"{Fore.LIGHTGREEN_EX}data: {data}")

        
        print(
            f"{Fore.YELLOW}_____________________________________________________________________")
        print(
            f"{Fore.YELLOW}_____________________________________________________________________")

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
    print(f"{Fore.RED}{Style.BRIGHT}can't be a hacking tool without some cool Ascii art ;){
          Style.RESET_ALL}")
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
    python reqfuzz.py -filter "status:200; time:14ms"     : Filter the response based on the passed filters.
    python reqfuzz.py -s example.com -p <payload_file>    : Subdomain enumeration
    python reqfuzz.py -s example.com  -t 20               : Specify the number of threads to use
    python reqfuzz.py -help                               : Show this help menu.

    Options:
    -b <request_file>  : Specify a file with the HTTP request details (method, endpoint, protocol, headers, body) you can get it from intercepting the request.
    -h <header_file>   : Provide a file with additional headers to test.
    -f request         : Indicate that the tool should fuzz the request headers.
    -p <payload_file>  : Specify a file with payloads to replace the 'FUZZ' placeholder in the headers.
    -s <domain>        : Subdomain enumeration.
    -t <nb_threads>    : Provide number of threads to use
    -filter "status:200; time:14ms" : Filter the response based on the passed filters
    -help              : Display this help menu.

    {Fore.CYAN}{Style.BRIGHT}For more information and updates, visit https://github.com/0x1nf3cted{Style.RESET_ALL}
    """)
