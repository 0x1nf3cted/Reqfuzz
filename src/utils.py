from colorama import Fore, Style, init


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
{Fore.GREEN}{Style.BRIGHT}Reqfuzz is a tool for Bypassing http headers, and many more features (to come).
{Style.RESET_ALL}
    """
    print(description)

def print_help_menu():
    print(f"""
{Fore.YELLOW}{Style.BRIGHT}ReqFuzz Help Menu{Style.RESET_ALL}

    Usage:
    python reqfuzz.py -b <request_file>  : Fuzz HTTP headers using the specified request file.
    python reqfuzz.py -b <request_file> -h <header_file>  : Fuzz HTTP headers with additional headers from the specified header file.
    python reqfuzz.py -help              : Show this help menu.

    Options:
    -b <request_file>  : Specify a file with the HTTP request details (method, endpoint, protocol, headers, body) you can get it from intercepting the request.
    -h <header_file>   : Provide a file with additional headers to test.
    -help              : Display this help menu.

    {Fore.CYAN}{Style.BRIGHT}For more information and updates, visit https://github.com/0x1nf3cted.{Style.RESET_ALL}
        """)
