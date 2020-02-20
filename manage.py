#!/usr/bin/env python3
import sys, subprocess


if sys[1] == "test":
    subprocess.run("pytest")
