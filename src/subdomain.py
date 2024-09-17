import http.client
from urllib.parse import urlparse

from src.utils import RequestFileParser



class Subdomain:
    def __init__(self):
        self.parser = RequestFileParser()
        self.url = ""
        self.payload_list = []

    def run(self):
        self.parser.thread_worker(self.payload_list, self.iterate_subdomains)

    def format_url(self, prefix):
        if "FUZZ" in self.url:
            temp_u = self.url.replace("FUZZ", prefix)
            return temp_u
        else:
            u = urlparse(self.url).netloc
            return prefix.join([".", u])

    def iterate_subdomains(self):
        for s in self.payload_list:
            self.ping_single_domain(self.format_url(s))

    def ping_single_domain(url):


        conn = http.client.HTTPConnection() 
        conn.request("GET")
        response = conn.getresponse()
        if(response.status == 200):
            print("exists")
        else:
            print("does not exist")

