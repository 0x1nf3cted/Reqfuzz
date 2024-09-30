import base64
import sys

def transform(item):
    
    return base64.b64encode(item.encode()).decode()

if __name__ == "__main__":

    item = sys.stdin.read().strip() 
    transformed_item = transform(item) 
    print(transformed_item) 
