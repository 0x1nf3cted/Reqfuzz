import hashlib
import sys

def transform(item):
    return hashlib.sha256(item.encode()).hexdigest()

if __name__ == "__main__":
    item = sys.stdin.read().strip() 
    transformed_item = transform(item) 
    print(transformed_item)
