#!/usr/bin/env bash





if [$1 = "create"]
# $2 = Path of Origin Repository
# $3 = Name of the Patcher (all without whitespaces)
# $4 = Name of the Patch (all without whitespaces)
then
  git clone $2
