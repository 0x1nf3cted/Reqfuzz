
from src.utils import RequestFileParser


class ReqFuzzer:
    def __init__(self):
        self.parser = RequestFileParser()   
        self.headers = {}
        self.request_info = {}
        self.payload_list = []
        self.body_content = ""
        self.reponse_metrics = {}
    


    def load_request_file(self, filename):
         
        self.headers, self.request_info, self.body_content = self.parser.parse_req_file(filename)


        if not self.headers:
            print("Failed to load headers from the request file.")
        if not self.body_content:
            print("Failed to load body content from the request file.")
        
    

    def fuzz(self):
        self.search_for_header_fuzz()
        self.search_for_req_body_fuzz()

    def search_for_header_fuzz(self):

        for key, value in self.headers.items():
            if "FUZZ" in value:
                original_header_val = value
                for p in self.payload_list:
                    new_header_val = original_header_val.replace("FUZZ", p)
                     
                    temp_headers = self.headers.copy()
                    temp_headers[key] = new_header_val

 
                    self.parser.print_header(temp_headers, self.body_content)
                    self.reponse_metrics, response_data = self.parser.send_request(temp_headers, self.request_info, self.body_content)
                    self.parser.print_response(data=response_data, response_metrics=self.reponse_metrics)

    def search_for_req_body_fuzz(self):
        if "FUZZ" in self.body_content:
            original_body_content = self.body_content
            for p in self.payload_list:
                temp_body_content = original_body_content.replace("FUZZ", p)
                 
                temp_headers = self.headers.copy()
                temp_headers["Content-Length"] = str(len(temp_body_content))
                
                self.parser.print_header(temp_headers,temp_body_content)
                self.reponse_metrics, response_data = self.parser.send_request(temp_headers, self.request_info, temp_body_content)
                self.parser.print_response(data=response_data, response_metrics=self.reponse_metrics)



    def display_request_info(self):
        print("Headers:", self.headers)
        print("Body Content:", self.body_content)