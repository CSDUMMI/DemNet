#!/usr/bin/env python
from Server.Database import register
import sys

argv    = sys.argv
register(argv[1], argv[2], argv[3], argv[4], argv[5])
