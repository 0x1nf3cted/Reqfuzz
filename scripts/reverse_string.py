import sys

def transform(item):
    return item[::-1]

if __name__ == "__main__":
    item = sys.stdin.read().strip() 
    transformed_item = transform(item) 
    print(transformed_item)
