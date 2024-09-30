# ReqFuzz: everything is fuzzable if you have the right tool ;)

![ReqFuzz](images/reqfuzz.png)

## Overview

ReqFuzz is a Swiss Army knife for web testing and fuzzing, providing everything you need to run multiple tests on a system. You can intercept any HTTP request using the integrated proxy and fuzz the request file—just put 'FUZZ' where you need it, load a wordlist, and you're good to go. You can specify the number of threads for faster execution and filter the results with conditions.

If that's not enough, you can also apply custom scripts to your wordlists. For example, if you have a wordlist with usernames but want to use base64 encoding instead of plain text, no problem. You can use the predefined script, which will be applied to each item in the wordlist, or create your own scripts in 13 different languages. The script will then be executed in a sandbox environment.



## Key Features

- **Intuitive Fuzzing**: Automatically test a range of HTTP headers to discover potential security flaws.
- **Multithreading Support**: Perform multiple fuzzing operations simultaneously, significantly reducing test duration.
- **Integrated Proxy**: Capture and log HTTP requests in real-time, allowing for detailed analysis of server interactions.
- **Scripting Capabilities**: Write custom scripts or utilize predefined ones to modify payloads dynamically during fuzzing.
- **Integrated sandbox**: Your proxy will run in a secure environement .
- **Extensible Design**: Easily extend and customize the tool with new features as your testing needs evolve.
- **Subdomain Enumeration**: Automatically generate and test various subdomain possibilities.
- **Response Filtering**: Focus on specific criteria during testing, such as status codes or response times, for a more targeted analysis.

## Getting Started

### Installation

To get started with **ReqFuzz**, ensure you have Python 3.x installed on your system. Clone the repository and install any necessary dependencies.

```bash
git clone <repository-url>
cd reqfuzz
pip install -r requirements.txt
```

### Usage

#### Basic Command

To start using ReqFuzz, execute the following command in your terminal:

```bash
python reqfuzz.py -b <request_file>
```

- **`<request_file>`**: A file containing details of the HTTP request, including the method, endpoint, headers, and body. 

### Command-Line Options

- **`-b <request_file>`**: 
  - Specifies the main HTTP request to test from a given file.
  
- **`-H <header_file>`** *(optional)*: 
  - Add extra headers for testing. Each header should be on a new line, formatted as `Header-Name: Header-Value`.

- **`-f <request_file>`**: 
  - A specific request file to fuzz using designated payloads.

- **`-proxy <port>`**: 
  - Starts an integrated proxy server on the specified port, enabling interception and logging of HTTP requests.
  - Example: `python reqfuzz.py -proxy 8000`.

- **`-p <payload_file>`**: 
  - Specifies a file containing different payloads to replace the placeholder `FUZZ` in headers or the body of the request.

- **`-s <domain>`**: 
  - Enumerate subdomains by substituting `FUZZ` in the specified domain format.

- **`-filter "condition"`**: 
  - Filters responses based on criteria like status codes or response times for focused analysis.

- **`-script <script>`**: 
  - Apply custom scripts to modify payloads for advanced testing. This allows users to write their own scripts or use predefined options.
  - Example: `python reqfuzz.py -f request -p <wordlist> -script scripts/md5_hash.py`.

- **`-t <nb_threads>`**: 
  - Sets the number of concurrent threads to use during the fuzzing process, optimizing performance.

- **`-help`**: 
  - Displays a help menu with detailed instructions on using ReqFuzz effectively.

### Examples

1. **Fuzz Headers from a Request File**:
   ```bash
   python reqfuzz.py -b request.txt
   ```

2. **Add Additional Headers**:
   ```bash
   python reqfuzz.py -b request.txt -H headers.txt
   ```

3. **Fuzz Headers Using Payloads**:
   ```bash
   python reqfuzz.py -f request.txt -p payloads.txt
   ```

4. **Run an Integrated Proxy**:
   ```bash
   python reqfuzz.py -proxy 8000
   ```

5. **Enumerate Subdomains**:
   ```bash
   python reqfuzz.py -s domain.com -p payloads.txt
   ```

6. **Filter Responses by Criteria**:
   ```bash
   python reqfuzz.py -s domain.com -p payloads.txt -filter "status:200; time:<100ms"
   ```

7. **Apply a script on the wordlist**:
   ```bash
   python reqfuzz.py -f request -p wordlist -script scripts/base64_en.py
   ```
8. **Use multithreading**:
   ```bash
   python reqfuzz.py -t 20
   ```

9. **Display Help Menu**:
   ```bash
   python reqfuzz.py -help
   ```


### Important features

#### Proxy Feature

The integrated proxy feature allows users to intercept and analyze HTTP requests sent to the specified port. When enabled, the request is captured and saved to a file named `request`, making it easy to review how different requests are processed by the server, and avoid using other third party tools to do so.


#### Scripting Feature

With the scripting capability, users can create custom scripts to modify or generate payloads dynamically during fuzzing. This flexibility allows for tailored testing scenarios that adapt to various requirements. Users can also utilize predefined scripts included with ReqFuzz for common tasks.

the code will run on an integrated sandbox, it's minimal and only block socket connections and file operations to critical parts. so you should check your scripts and make sure they are safe.

#### supported scripting languages:

Python, Ruby, Dart, Perl, PHP, Node.js, Shell Script, R, Lua, Haskell, Elixir, Swift.

**note**: here are some things to look out for in order to make the scripts work 

- make sure the scripting language that you want to use is already installed in your system

- your script should `PRINT` the returned value and not just `RETURN` it



PS: even tho this tool has an integrated sandbox, i cannot be 100% sure that it will block malicious scripts (aside from the provided scripts in /scripts which are secure), i'm not responsible of the scripts you provide, you should NEVER use a script from the internet without knowing what it do, and make sure your wordlist doesn't contain any malicious code.


 
### Contributing

We welcome and encourage contributions to ReqFuzz! If you'd like to help improve this tool, feel free to fork the repository, make changes, and submit a pull request. Whether it's fixing bugs, adding new features, or improving documentation, your contributions are greatly appreciated. Please make sure to follow our contribution guidelines and ensure your code is well-tested.

also feel free to provide useful scripts that we can add to predefined scripts

### Platform Support

Please note that this tool has been tested primarily on Linux environments. While it may work on other platforms, we cannot guarantee full compatibility or functionality on systems like Windows or macOS. Contributions to improve cross-platform support are also welcome!

though ReqFuzz supports 13 scripting languages, so far we have only tested scripts using Python, Bash, and PHP. The other languages should work **theoretically**, but they haven't been fully tested yet. Contributions to improve cross-platform support and test other languages are welcome!