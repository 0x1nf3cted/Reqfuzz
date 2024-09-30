import codecs
import sys

def transform(item):
    return codecs.encode(item, 'rot_13')

if __name__ == "__main__":
    item = sys.stdin.read().strip() 
    transformed_item = transform(item) 
    print(transformed_item)
