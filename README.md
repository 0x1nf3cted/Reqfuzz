# ReqFuzz

![Reqfuzz](images/reqfuzz.png)

### Description

**ReqFuzz** is a versatile tool designed for fuzzing HTTP headers to uncover potential security vulnerabilities and bypass restrictions. It tests various header configurations to see how they affect web applications, helping identify issues related to header handling and access control. The tool supports multiple HTTP methods (`GET`, `POST`, `PUT`, etc.) and leverages multithreading to efficiently manage and test a large number of header variations.

### Usage Guide

#### Basic Command

To start using ReqFuzz, you can run:

```bash
python reqfuzz.py -b <request_file>
```

- **`<request_file>`**: Specifies the file containing the HTTP request details, including the method, endpoint, protocol, headers, and body.

#### Additional Options

- **`-b <request_file>`**:
  - **Purpose**: Defines the file with the HTTP request to be tested.
  - **Format**: This file should include the request method, endpoint, protocol, and optionally, headers and body content.

- **`-H <header_file>`** (optional, used with `-b`):
  - **Purpose**: Provides a file with additional headers to be tested.
  - **Format**: Each line in the file should follow the format `Header-Name: Header-Value`.

- **`-f <request_file>`**:
  - **Purpose**: Specifies a request file to be fuzzed using a payload.
  - **Format**: This file should include the HTTP request details similar to the `-b` option.

- **`-p <payload_file>`**:
  - **Purpose**: Provides a file with payloads to test in place of `FUZZ` in the headers or request body.
  - **Format**: Each line in the file represents a different payload to be tested.

- **`-s <domain>`**:
  - **Purpose**: Enumerate subdomains to test in place of `FUZZ` or format the domains automatically.
  - **Format**: `FUZZ.example.com` or a simple url.

- **`-t <nb_threads>`**:
  - **Purpose**: Specify the number of threads to use.
  - **Format**: `python reqfuzz.py -t 20` this will use 20 threads.

- **`-help`**:
  - **Purpose**: Displays the help menu with instructions on how to use the tool.

#### Examples

1. **Fuzz Headers from Request File**:
   ```bash
   python reqfuzz.py -b request.txt
   ```
   - Reads the HTTP request from `request.txt` and tests it with the default headers.

2. **Fuzz Headers with Additional Headers**:
   ```bash
   python reqfuzz.py -b request.txt -H headers.txt
   ```
   - Tests the HTTP request from `request.txt` using additional headers specified in `headers.txt`.

3. **Fuzz Headers Using Payloads**:
   ```bash
   python reqfuzz.py -f request.txt -p payloads.txt
   ```
   - Fuzzes the HTTP request from `request.txt` with payloads provided in `payloads.txt`.

4. **Subdomain enumeration**:
  ```bash
  python reqfuzz.py *s domain -p <payload_file>
  ```

5. **Show Help Menu**:
   ```bash
   python reqfuzz.py -help
   ```
   - Provides information on how to use the tool and its available options.

### Features

- **Multithreading**.
- **Header Fuzzing**.
- **Bypassing Localhost Restrictions**.
- **Extensible Design**.
- **Subdomain enumeration**
- **Error Handling**.

