from src.utils import RequestFileParser
import subprocess

class ReqFuzzer:
    def __init__(self):
        self.parser = RequestFileParser()
        self.headers = {}
        self.script = False
        self.script_location = ""
        self.request_info = {}
        self.payload_list = []
        self.body_content = ""
        self.reponse_metrics = {}

    def apply_script(self, item):
        try:
            process = subprocess.Popen(
                ['python3', self.script_location],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate(input=item.encode())

            if stderr:
                raise RuntimeError(f"Script error: {stderr.decode().strip()}")

            output = stdout.decode().strip()
            if not output:
                print("Warning: The script returned no output.")
                return None
            
            return output

        except FileNotFoundError:
            print(f"Error: The script '{self.script_location}' was not found.")
        except Exception as e:
            print(f"Error applying script: {e}")

        return None

    def load_request_file(self, filename):
        self.headers, self.request_info, self.body_content = self.parser.parse_req_file(filename)

        if not self.headers:
            print("Failed to load headers from the request file.")

    def fuzz(self):
        self.search_for_header_fuzz()
        self.search_for_req_body_fuzz()

    def should_fuzz(self):
        items_to_check = [
            self.request_info["Host"],
            self.request_info["method"],
            self.request_info["endpoint"]
        ]

        for key, value in self.headers.items():
            items_to_check.append(value)
            items_to_check.append(key)
        
        return any("FUZZ" in item for item in items_to_check)

    def search_for_header_fuzz(self):
        if not self.payload_list:
            print("Payload list is empty. No fuzzing will be done.")
            return
        
        if self.should_fuzz():
            for key, value in self.headers.items():
                original_header_val = value

                for p in self.payload_list:
                    if p is None:
                        exit
                    if self.script:
                        p = self.apply_script(p)

                    temp_request_info = self.request_info.copy()
                    temp_request_info["Host"] = temp_request_info["Host"].replace("FUZZ", p)
                    temp_request_info["endpoint"] = temp_request_info["endpoint"].replace("FUZZ", p)
                    new_header_val = original_header_val.replace("FUZZ", p)

                    temp_headers = self.headers.copy()
                    temp_headers[key] = new_header_val

                    self.parser.print_header(temp_headers, self.body_content, temp_request_info)

                    self.reponse_metrics, response_data = self.parser.send_request(
                        temp_headers, temp_request_info, self.body_content
                    )
                    self.parser.print_response(
                        data=response_data, response_metrics=self.reponse_metrics
                    )

    def search_for_req_body_fuzz(self):
        if "FUZZ" in self.body_content:
            original_body_content = self.body_content

            for p in self.payload_list:
                
                if not p:
                    print("Warning: The payload is empty. Skipping replacement.")
                    continue 
                if self.script:
                    p = self.apply_script(p)

                temp_body_content = original_body_content.replace("FUZZ", p)
                temp_headers = self.headers.copy()
                temp_headers["Content-Length"] = str(len(temp_body_content))

                self.parser.print_header(temp_headers, temp_body_content, self.request_info)

                self.reponse_metrics, response_data = self.parser.send_request(
                    temp_headers, self.request_info, temp_body_content
                )
                self.parser.print_response(
                    data=response_data, response_metrics=self.reponse_metrics
                )
        else:
            print("No 'FUZZ' keyword found in body content. No fuzzing will be done.")

    def display_request_info(self):
        print("Headers:", self.headers)
        print("Body Content:", self.body_content)
