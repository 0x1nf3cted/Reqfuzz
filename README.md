# ReqFuzz

![ReqFuzz](images/reqfuzz.png)

### Overview

**ReqFuzz** is a powerful tool for security testing that focuses on fuzzing HTTP headers to uncover potential vulnerabilities and bypass restrictions. By experimenting with various header configurations, ReqFuzz can help identify issues related to how headers are processed and managed in web applications. This tool is essential for security researchers and penetration testers looking to enhance their assessment of web application security.

### Usage

#### Basic Command

To start using ReqFuzz, you can execute the following command:

```bash
python reqfuzz.py -b <request_file>
```

- **`<request_file>`**: This is the file that contains details of the HTTP request, including the method, endpoint, protocol, headers, and body.

#### Options

- **`-b <request_file>`**: 
  - Specifies the main HTTP request to test.
  
- **`-H <header_file>`** (optional): 
  - Allows you to specify additional headers for testing, one per line in the format `Header-Name: Header-Value`.

- **`-f <request_file>`**: 
  - A request file to fuzz using a specified payload.

- **`-proxy <port>`**: 
  - Starts an integrated proxy server on a given port to intercept HTTP requests.
  - Example: `python reqfuzz.py -proxy 8000`.

- **`-p <payload_file>`**: 
  - A file with different payloads that will replace the placeholder `FUZZ` in the headers or body.

- **`-s <domain>`**: 
  - Enumerates subdomains by replacing `FUZZ` in the specified domain format.

- **`-filter "condition"`**: 
  - Filters responses based on specified criteria, such as status codes or response times.

- **`-script <script>`**: 
  - Allows you to apply custom scripts to modify the payloads for advanced testing. Users can write their own scripts or use predefined ones.
  - Example: `python reqfuzz.py -f request -p <wordlist> -script scripts/md5_hash.py`.

- **`-t <nb_threads>`**: 
  - Sets the number of concurrent threads for the fuzzing process.

- **`-help`**: 
  - Displays a help menu with detailed instructions on how to use the tool.

#### Examples

1. **Fuzz Headers from a Request File**:
   ```bash
   python reqfuzz.py -b request.txt
   ```

2. **Fuzz Headers with Additional Headers**:
   ```bash
   python reqfuzz.py -b request.txt -H headers.txt
   ```

3. **Fuzz Headers Using Payloads**:
   ```bash
   python reqfuzz.py -f request.txt -p payloads.txt
   ```

4. **Integrated Proxy to Intercept HTTP Requests**:
   ```bash
   python reqfuzz.py -proxy <port_number>
   ```

5. **Subdomain Enumeration**:
   ```bash
   python reqfuzz.py -s domain -p <payload_file>
   ```

6. **Filter Responses**:
   ```bash
   python reqfuzz.py -s domain -p <payload_file> -filter "status:200; time:14ms"
   ```

7. **Display Help Menu**:
   ```bash
   python reqfuzz.py -help
   ```

### Key Features

- **Multithreading**: Conduct multiple fuzzing operations simultaneously for efficiency.
- **Header Fuzzing**: Test various HTTP headers for vulnerabilities.
- **Integrated Proxy**: Intercept HTTP requests and log them for further analysis.
- **Scripting Support**: Apply custom or predefined scripts to modify payloads dynamically.
- **Extensible Design**: Easily add new features or customize existing ones.
- **Subdomain Enumeration**: Automatically generate subdomains for testing.
- **Response Filtering**: Filter responses to focus on specific criteria during testing.

### Use Cases

**Local File Inclusion (LFI) Detection**: Create a request file and use ReqFuzz to replace the `FUZZ` keyword with payloads from your LFI dictionary. You can then filter responses to identify successful attempts.

Example Request for LFI:
```
GET /FUZZ HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: close
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i
```

**Note**: You can fuzz any part of the HTTP request file as needed.

### Proxy Feature

The integrated proxy allows users to intercept HTTP requests. When you run the proxy, any request sent to the specified port will be captured and written to a file named `request`. This feature is particularly useful for testing and analyzing how different requests are processed by the server.

### Scripting Feature

The scripting capability allows users to apply custom scripts to the payloads during the fuzzing process. This enables advanced testing scenarios where users can modify or generate payloads dynamically, making it easier to adapt to various testing needs. Users can create their own scripts or utilize predefined scripts available with ReqFuzz.

