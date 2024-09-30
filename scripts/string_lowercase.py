import sys

def transform(item):
    return item.upper()

if __name__ == "__main__":
    item = sys.stdin.read().strip() 
    transformed_item = transform(item) 
    print(transformed_item)
