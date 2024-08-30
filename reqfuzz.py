import sys
from colorama import Fore, Style, init
import argparse
from src.bypass import ReqBypass
from src.utils import not_a_hacking_tool_without_ascii_art, print_help_menu, RequestFileParser
from src.fuzzer import ReqFuzzer



init(autoreset=True)


def run():
    bypass = ReqBypass()
    handler = RequestFileParser()
    fuzzer = ReqFuzzer()


    if len(sys.argv) < 2:
        print("Usage: python3 reqfuzz.py -h <request file>")
        return

    not_a_hacking_tool_without_ascii_art()
    parser = argparse.ArgumentParser(description="ReqFuzz: A tool for fuzzing HTTP headers.")

    parser = argparse.ArgumentParser(description="ReqFuzz: A tool for fuzzing HTTP headers.")

    parser.add_argument('-b', '--request-file', type=str, help='Specifies the file with HTTP request details.')
    parser.add_argument('-H', '--header-file', type=str, help='Provides a file with additional headers to test.')
    parser.add_argument('-f', '--fuzz-file', type=str, help='Specifies the file with HTTP request details for fuzzing.')
    parser.add_argument('-p', '--payload-file', type=str, help='Provides a file with payloads for fuzzing.')

    args = parser.parse_args()

 

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

        filename = args.request_file
        if not handler.check_file(filename):
            print(f"{Fore.RED}Error, the request file that you provided doesn't exist")
            print_help_menu()
            return

        bypass.parse_req_file(filename)


        bypass.fuzz_headers()
 

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

        filename = args.fuzz_file
        if not handler.check_file(filename):
            print(f"{Fore.RED}Error, the request file that you provided doesn't exist")
            print_help_menu()
            return

        fuzzer.load_request_file(filename)
        fuzzer.fuzz()

    else:
        print(f"{Fore.RED}Error, can't recognize the argument")
        print_help_menu()


if __name__ == "__main__":
    run()
