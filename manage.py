#!/usr/bin/env python3
import sys, subprocess, os


if sys.argv[1] == "test":
    subprocess.run("pytest")
elif sys.argv[1] == "run":
    os.environ["BUILDER"] = sys.argv[2]
    subprocess.run("./start")
else:
    print("""Please provide a command:
test : To run the tests
run : To run the Server""", file=sys.stderr)
