import hashlib
import sys

def transform(item):
    return hashlib.md5(item.encode()).hexdigest()

if __name__ == "__main__":
    item = sys.stdin.read().strip() 
    transformed_item = transform(item) 
    print(transformed_item)
