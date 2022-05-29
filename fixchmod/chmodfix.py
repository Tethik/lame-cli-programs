#!/usr/bin/python3

import os
import os.path
import sys
from subprocess import call


def main():
    dir = sys.argv[1]
    chmod = "644"

    if len(sys.argv) > 2:
        chmod = str(int(sys.argv[2]))

    queue = os.listdir(dir)
    while queue:
        f = dir + "/" + queue.pop()
    #    path = os.path.abspath(f)
        print(f)
        if os.path.isdir(f):
            queue += [f + "/" + v for v in os.listdir(f)]
        elif os.path.isfile(f):
            print(f, chmod)
            print(call(["chmod", chmod, f]))
        elif not os.path.isfile(f):
            raise Exception(f + " is not a file or folder??")

    print("done!")
