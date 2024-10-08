import sys
from colorama import Fore, Style, init
import argparse
from src.bypass import ReqBypass
from src.utils import not_a_hacking_tool_without_ascii_art, print_help_menu, RequestFileParser
from src.fuzzer import ReqFuzzer
from src.subdomain import Subdomain
from src.proxy import Proxy
import validators

init(autoreset=True)


def run():
    bypass = ReqBypass()
    handler = RequestFileParser()
    fuzzer = ReqFuzzer()
    
    subdomain = Subdomain()

    if len(sys.argv) < 2:
        print_help_menu()
        return

    not_a_hacking_tool_without_ascii_art()
    parser = argparse.ArgumentParser(description="ReqFuzz: A tool for fuzzing HTTP headers.")


    parser.add_argument('-b', '--request-file', type=str, help='Specifies the file with HTTP request details.')
    parser.add_argument('-proxy', '--proxy', type=int, help='Start a proxy at a certain to capture http requests.')
    parser.add_argument('-script', '--script', type=str, help='Apply the script code on the payload.')
    parser.add_argument('-H', '--header-file', type=str, help='Provides a file with additional headers to test.')
    parser.add_argument('-filter', '--filter-response', type=str, help='Filter responses according to user conditions.')
    parser.add_argument('-f', '--fuzz-file', type=str, help='Specifies the file with HTTP request details for fuzzing.')
    parser.add_argument('-p', '--payload-file', type=str, help='Provides a file with payloads for fuzzing.')
    parser.add_argument('-s', '--subdomain', type=str, help='Provides a file with subdomain list.')
    parser.add_argument('-t', '--threads', type=int, help='Provide number of threads.')

    args = parser.parse_args()

    if args.threads:
        if isinstance(args.threads, int): 
            handler.threads = args.threads
        else:
            print("Error: number of threads should be an integer")


    if args.proxy:
        proxy = Proxy(args.proxy)
        proxy.start_proxy()
        
    if args.request_file:
        if args.header_file:
            header_file = args.header_file
            if not handler.check_file(header_file):
                print(f"{Fore.RED}Error, the header file that you provided doesn't exist")
                print_help_menu()
                return
            else:
                bypass.headers_provided = True
                with open(header_file) as file:
                    bypass.forward_headers = [line.rstrip() for line in file]
        elif args.filter_response:
            handler.with_condition = True
            handler.parse_conditions(args.filter_response)
        filename = args.request_file
        if not handler.check_file(filename):
            print(f"{Fore.RED}Error, the request file that you provided doesn't exist")
            print_help_menu()
            return

        bypass.parse_req_file(filename)


        # bypass.fuzz_headers()
 

    elif args.fuzz_file:
        if args.payload_file:
            header_file = args.payload_file
            if not handler.check_file(header_file):
                print(f"{Fore.RED}Error, the header file that you provided doesn't exist")
                print_help_menu()
                return
            else:
                with open(header_file) as file:
                    fuzzer.payload_list = [line.rstrip() for line in file]

        # elif args.filter_response:
        #     handler.with_condition = True
        #     handler.parse_conditions(args.filter_response)
            
        filename = args.fuzz_file
        if not handler.check_file(filename):
            print(f"{Fore.RED}Error, the request file that you provided doesn't exist")
            print_help_menu()
            return
        
        if args.script:
            if not handler.check_file(args.script):
                print(f"{Fore.RED}Error, the script file that you provided doesn't exist")
                print_help_menu()
                return
            else:
                fuzzer.script = True
                fuzzer.script_location = args.script
                with open(args.script, 'r') as script_file:
                    fuzzer.script_code = script_file.read()


        fuzzer.load_request_file(filename)
        fuzzer.fuzz()

    elif args.subdomain:
        if args.payload_file:
            subdomain_file = args.payload_file
            if not handler.check_file(subdomain_file):
                print(f"{Fore.RED}Error, the header file that you provided doesn't exist")
                print_help_menu()
                return
            else:
                with open(subdomain_file) as file:
                    subdomain.payload_list = [line.rstrip() for line in file]
        else:
            print("Error: you should provide the subdomain wordlist")
        subdomain.url = args.subdomain
        if(args.subdomain):
            subdomain.iterate_subdomains()
        else:
            print(f"Error {args.subdomain} is not a valid domain")

    else:
        print(f"{Fore.RED}Error, can't recognize the argument")
        print_help_menu()


if __name__ == "__main__":
    run()
