# Reqfuzz

![Reqfuzz](image/reqfuzz.png)


### Description:

**ReqFuzz** is a specialized tool for fuzzing HTTP headers to identify potential security vulnerabilities and bypass localhost restrictions. It tests how various headers affect web applications and can help in discovering issues related to header handling and access controls. This tool supports multiple HTTP methods (`GET`, `POST`, `PUT`, etc.) and utilizes multithreading to efficiently process a large number of header variations.

### Usage Guide:

#### Basic Command:
```bash
python reqfuzz.py -b <request_file>
```
- **`<request_file>`**: Specifies the file with HTTP request details, including the method, endpoint, protocol, headers, and body.

#### Options:

- **`-b <request_file>`**:
  - **Purpose**: Defines the file that contains the HTTP request to be tested.
  - **Format**: The file should include the request method, endpoint, protocol, and optionally, headers and body content.

- **`-h <header_file>`** (optional, used with `-b`):
  - **Purpose**: Provides a file with additional headers to test.
  - **Format**: Each line in the file should follow the format `Header-Name: Header-Value`.

- **`-help`**:
  - **Purpose**: Displays the help menu with instructions on how to use the tool.

#### Examples:

1. **Fuzz Headers from Request File**:
   ```bash
   python reqfuzz.py -b request.txt
   ```
   - Reads the HTTP request from `request.txt` and tests it with the default headers.

2. **Fuzz Headers with Additional Headers**:
   ```bash
   python reqfuzz.py -b request.txt -h headers.txt
   ```
   - Tests the HTTP request from `request.txt` using additional headers specified in `headers.txt`.

3. **Show Help Menu**:
   ```bash
   python reqfuzz.py -help
   ```
   - Provides information on how to use the tool and its available options.

### Features:

- **Multithreading**: Enhances performance by testing multiple headers concurrently.
- **Header Fuzzing**: Tests various headers to detect how they influence server behavior and identify possible security issues.
- **Bypassing Localhost Restrictions**: Helps in testing and bypassing restrictions that might be applied on localhost environments.
- **Extensible Design**: The object-oriented structure allows for easy feature addition and modification.
- **Error Handling**: Provides clear feedback on issues such as missing files or incorrect formats.

### Use Cases:

- **Security Testing**: Evaluate how different headers impact the security of your web applications.
- **Localhost Restriction Bypass**: Test and bypass localhost-specific access controls.
- **Fuzzing request headers**: it can fuzz request headers and request body on the fly
- **Compliance and Performance Checks**: Ensure that your application meets security standards and performs well under various header configurations.