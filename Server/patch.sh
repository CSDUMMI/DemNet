#!/usr/bin/env bash

if [ $1 = "create" ]
# $2 = Path of Origin Repository
# $3 = Name of the Patcher (all without whitespaces)
# $4 = Name of the Patch (all without whitespaces)
then
  git clone $2 $PATCHES/"$3-$4"
elif [ $1 = "merge" ]
# $2 = Name of the Patcher (without whitespaces)
# $3 = Name of the Patch
then
  current_pwd=pwd
  cd $PATCHES/"$2-$3"
  git push
else
  echo "Please provide a command"
fi
