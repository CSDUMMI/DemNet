#!/usr/bin/env python3
import sys, subprocess, os


if sys.argv[1] == "test":
    exit(subprocess.run("pytest").returncode)
elif sys.argv[1] == "run":
    os.environ["BUILDER"] = sys.argv[2]
    exit(subprocess.run("./start").returncode)
else:
    print("""Please provide a command:
test : To run the tests
run : To run the Server""", file=sys.stderr)
