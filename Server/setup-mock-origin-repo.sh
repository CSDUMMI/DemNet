#!/usr/bin/env bash

if [ $1 = "create" ]
then
  current_loc=$PWD
  mkdir /tmp/demnet_origin
  cd /tmp/demnet_origin
  git init
  echo "TEST" > TEST
  git add .
  git commit -m "INITIAL COMMIT"
  cd $current_loc
else
  rm /tmp/demnet_origin -rf
fi
