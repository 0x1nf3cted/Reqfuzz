import http.client
import socket
from urllib.parse import urlparse

from colorama import Fore
from src.utils import RequestFileParser


class Subdomain:
    def __init__(self):
        self.parser = RequestFileParser()
        self.url = ""
        self.payload_list = []

    def run(self):
        self.parser.thread_worker(self.payload_list, self.iterate_subdomains)

    def format_url(self, prefix):
        parsed_url = urlparse(self.url)
        if not parsed_url.scheme:
            parsed_url = urlparse("http://" + self.url)

        if "FUZZ" in self.url:
            temp_url = self.url.replace("FUZZ", prefix)
            return temp_url
        else:
            domain = parsed_url.netloc or parsed_url.path
            return f"{prefix}.{domain}"

    def iterate_subdomains(self):
        for s in self.payload_list:
            formatted_url = self.format_url(s)
            self.ping_single_domain(formatted_url)

    def resolve_domain(self, url):
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc or parsed_url.path
            ip_address = socket.gethostbyname(domain)
            return ip_address
        except socket.gaierror:
            return None



    def ping_single_domain(self, subdomain):
        conn = None  # Initialize conn variable
        try:
            # Build the full URL
            full_url = f"http://{subdomain}"

            # Parse the URL to extract the host and the path
            parsed_url = urlparse(full_url)
            host = parsed_url.netloc
            path = parsed_url.path or "/"

            # Check if the domain resolves
            try:
                socket.gethostbyname(host)
            except socket.gaierror:
                # If DNS resolution fails, do nothing
                return

            # Establish an HTTP connection to the host
            conn = http.client.HTTPConnection(host)
            conn.request("GET", path)

            # Get response and check status
            response = conn.getresponse()
            if response.status == 200:
                print(f"{Fore.GREEN}Domain {host} exists")
            else:
                print(f"{Fore.RED}Domain {host} does not exist")
        except Exception as e:
            # Print error message for unexpected exceptions
            print(f"Error pinging {full_url}: {e}")
        finally:
            # Close the connection only if it was successfully created
            if conn:
                conn.close()
