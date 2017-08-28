import os
import deepdish as dd

if __name__ == '__main__':
    for root, dirs, files in os.walk("tmp/train/events"):
        print(root, dirs, files)
