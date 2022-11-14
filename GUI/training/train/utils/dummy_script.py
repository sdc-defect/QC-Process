#!/usr/bin/python3
import argparse

import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--json',
                    required=True)
args = parser.parse_args()
print(args.json)
for i in range(0,5):
    print(f"============ {i} ===")
    time.sleep(1)

# sys.stderr.write("Testing stderr...\n")
print("Enter name:")
# name = sys.stdin.readline()
# print(f"Got {name}")