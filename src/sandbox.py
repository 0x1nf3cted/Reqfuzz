from src.utils import RequestFileParser
import subprocess
import resource
import os
import tempfile
import socket
import sys

LANGUAGES = {
    'python': 'python3',
    'ruby': 'ruby',
    'dart': 'dart',
    'perl': 'perl',
    'php': 'php',
    'node': 'node',
    'bash': '/bin/bash',
    'R': 'Rscript',
    'lua': 'lua',
    'haskell': 'runghc',
    'elixir': 'elixir',
    'swift': 'swift',
}


class Sandbox:
    def __init__(self):
        self.parser = RequestFileParser()
        self.headers = {}
        self.script = False
        self.script_code = ""
        self.script_location = ""
        self.request_info = {}
        self.payload_list = []
        self.body_content = ""
        self.reponse_metrics = {}



    def limit_resources(self):
        resource.setrlimit(resource.RLIMIT_CPU, (5, 5))  # Limit CPU time to 5 seconds
        resource.setrlimit(resource.RLIMIT_AS, (128 * 1024 * 1024, 128 * 1024 * 1024))  # Limit memory usage to 128 MB

    def block_file_operations(self):
        def restricted_open(filepath, *args, **kwargs):
            forbidden_paths = ["/tmp", "/etc", "/var", "/root"]
            if any(filepath.startswith(path) for path in forbidden_paths):
                raise PermissionError(f"Access to {filepath} is restricted.")
            return open(filepath, *args, **kwargs)


        globals()['open'] = restricted_open


    def block_internet_connections(self):
        def block_socket(*args, **kwargs):
            raise PermissionError("Internet connection is blocked.")


        socket.socket = block_socket

    def run_code(self, language, code, item=None):
        if language not in LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")

        interpreter = LANGUAGES[language]


        with tempfile.TemporaryDirectory() as temp_dir:
            if language == "bash":
                interpreter = "sh" # to create a temp file with the right extension
            
            temp_code_filename = os.path.join(temp_dir, f'code.{language}')

            with open(temp_code_filename, 'w') as temp_code_file:
                temp_code_file.write(code)

            try:
                def preexec_fn():
                    self.limit_resources()
                    self.block_file_operations()
                    self.block_internet_connections()
                    # will add more limits later
 
                input_data = item if item is not None else None

                result = subprocess.run(
                    [interpreter, temp_code_filename],
                    capture_output=True,  
                    text=True,  
                    timeout=5,  
                    input=input_data,      
                    preexec_fn=preexec_fn,
                    cwd=temp_dir,
                    env={"PATH": "/usr/bin"}  # Limit the environment variables
                )

                if result.stderr:
                    raise RuntimeError(f"Script error: {result.stderr.strip()}")

                output = result.stdout.strip()
                if not output:
                    print("Warning: The script returned no output.")
                    return None

                return output

            except subprocess.TimeoutExpired:
                raise RuntimeError(f"Error: Code execution timed out")
            except Exception as e:
                raise ValueError(f"{str(e)}")
