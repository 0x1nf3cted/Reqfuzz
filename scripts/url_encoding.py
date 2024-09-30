import urllib.parse
import sys

def transform(item):
    return urllib.parse.quote(item)

if __name__ == "__main__":
    item = sys.stdin.read().strip() 
    transformed_item = transform(item) 
    print(transformed_item)
