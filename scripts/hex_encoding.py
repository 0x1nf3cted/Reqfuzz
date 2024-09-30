import sys

def transform(item):
    return item.encode().hex()

if __name__ == "__main__":
    item = sys.stdin.read().strip() 
    transformed_item = transform(item) 
    print(transformed_item)
