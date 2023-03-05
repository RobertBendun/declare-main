#!/usr/bin/env python3
from declare import main
import os

@main
def mkdir(path: str, /, *, mode: int = False):
    "Create directory"
    os.mkdir(path=path, mode=mode)

@main
def ls(path: str = ".", /):
    "List files in directory"
    for entry in os.listdir(path):
        print(entry)

@main
def rmdir(path: str, /):
    "Remove directory"
    os.rmdir(path)

if __name__ == "__main__":
    main()
