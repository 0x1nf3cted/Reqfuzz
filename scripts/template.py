import sys  # Import the sys module to read from standard input

# Define the transformation function
def transform(item):
    """
    Transform the input string in some way.
    Modify this function to implement the desired string operation.
    For example, to encode in Base64, you can use:
    
    import base64
    return base64.b64encode(item.encode()).decode()

    Args:
        item (str): The input string to transform.

    Returns:
        str: The transformed string.
    """
    # Example transformation: Convert the string to uppercase
    return item.upper()  # Change this line based on the desired operation

if __name__ == "__main__":
    # Read input from standard input (stdin)
    item = sys.stdin.read().strip()  # Read the input and remove any surrounding whitespace

    # Call the transformation function
    transformed_item = transform(item)  # Pass the input to the transformation function

    # Print the transformed output
    print(transformed_item)  # Output the result
