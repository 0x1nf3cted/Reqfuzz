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

    match sys.argv[1]:
        case '-b':
            if len(sys.argv) >= 5 and sys.argv[3] == "-h":
                header_file = sys.argv[4]
                if not handler.check_file(header_file):
                    print(f"{Fore.RED}Error, the header file that you provided doesn't exist")
                    print_help_menu()
                    return
                else:
                    bypass.headers_provided = True
                    with open(header_file) as file:
                        bypass.forward_headers = [line.rstrip() for line in file]
            elif len(sys.argv) == 4:
                print(f"{Fore.RED}Error, number of arguments is not enough")
                print_help_menu()
                return

            filename = sys.argv[2]
            if not handler.check_file(filename):
                print(f"{Fore.RED}Error, the request file that you provided doesn't exist")
                print_help_menu()
                return

            bypass.parse_req_file(filename)

            import time
            start_time = time.time()
            bypass.fuzz_in_threads(20)
            print("--- %s seconds ---" % (time.time() - start_time))

        case '-f':
            if len(sys.argv) >= 5 and sys.argv[3] == "-p":
                header_file = sys.argv[4]
                if not handler.check_file(header_file):
                    print(f"{Fore.RED}Error, the header file that you provided doesn't exist")
                    print_help_menu()
                    return
                else:
 
                    with open(header_file) as file:
                        fuzzer.payload_list = [line.rstrip() for line in file]
            elif len(sys.argv) == 4:
                print(f"{Fore.RED}Error, number of arguments is not enough")
                print_help_menu()
                return
            

            filename = sys.argv[2]
            if not handler.check_file(filename):
                print(f"{Fore.RED}Error, the request file that you provided doesn't exist")
                print_help_menu()
                return
            fuzzer.load_request_file(filename)
            fuzzer.fuzz()
        

        case _:
            print(f"{Fore.RED}Error, can't recognize the argument")
            print_help_menu()
    
 


if __name__ == "__main__":
    run()
