
# ReqFuzz

![ReqFuzz](images/reqfuzz.png)

### Overview

**ReqFuzz** is a tool designed for fuzzing HTTP headers to detect potential security vulnerabilities and bypass restrictions. By testing a wide range of header configurations, it helps identify issues related to header handling and access control.

### Usage

#### Basic Command

To initiate ReqFuzz, run the following command:

```bash
python reqfuzz.py -b <request_file>
```

- **`<request_file>`**: Specifies the file containing HTTP request details, including the method, endpoint, protocol, headers, and body.

#### Options

- **`-b <request_file>`**:
  - **Purpose**: Defines the file with the HTTP request to be tested.
  - **Format**: The request file should include the method, endpoint, protocol, and optionally headers and body content.

- **`-H <header_file>`** (optional, used with `-b`):
  - **Purpose**: Specifies an additional file containing headers to be tested.
  - **Format**: Each line in the file should follow the format `Header-Name: Header-Value`.

- **`-f <request_file>`**:
  - **Purpose**: Provides a request file to be fuzzed using a specified payload.
  - **Format**: The request file should be formatted similarly to the `-b` option, containing HTTP request details.

- **`-p <payload_file>`**:
  - **Purpose**: Supplies a file containing payloads to replace the placeholder `FUZZ` in the headers or body.
  - **Format**: Each line in the file represents a different payload for testing.

- **`-s <domain>`**:
  - **Purpose**: Enumerates subdomains or formats domains for fuzzing by replacing `FUZZ`.
  - **Format**: For instance, `FUZZ.example.com` or a standard URL format.

- **`-filter "condition"`**:
  - **Purpose**: Filters responses based on specified criteria.
  - **Format**: Example: `python reqfuzz.py -filter "status:200; time:14ms"`.

- **`-t <nb_threads>`**:
  - **Purpose**: Specifies the number of threads to be used for concurrent fuzzing.
  - **Format**: Example: `python reqfuzz.py -t 20` will execute the fuzzing process using 20 threads.

- **`-help`**:
  - **Purpose**: Displays the help menu with detailed usage instructions.

#### Examples

1. **Fuzz Headers from a Request File**:
   ```bash
   python reqfuzz.py -b request.txt
   ```
   - Reads the HTTP request from `request.txt` and tests it with the default header fuzzing options.

2. **Fuzz Headers with Additional Headers**:
   ```bash
   python reqfuzz.py -b request.txt -H headers.txt
   ```
   - Tests the HTTP request from `request.txt` using the additional headers specified in `headers.txt`.

3. **Fuzz Headers Using Payloads**:
   ```bash
   python reqfuzz.py -f request.txt -p payloads.txt
   ```
   - Fuzzes the HTTP request from `request.txt` by using payloads from `payloads.txt`.

4. **Subdomain Enumeration**:
   ```bash
   python reqfuzz.py -s domain -p <payload_file>
   ```

5. **Filter Responses**:
   ```bash
   python reqfuzz.py -s domain -p <payload_file> -filter "status:200; time:14ms"
   ```

6. **Display Help Menu**:
   ```bash
   python reqfuzz.py -help
   ```
   - Shows detailed help and usage information.

### Key Features

- **Multithreading**
- **Header Fuzzing**
- **Extensible Design**
- **Subdomain Enumeration**
- **Response Filtering**

### Use Cases

**Local File Inclusion (LFI) Detection**: You can create a request file and use ReqFuzz to replace the `FUZZ` keyword with payloads from your LFI dictionary. Afterward, you can filter responses with specific criteria such as `-filter "status:200"` to identify successful LFI attempts.

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


