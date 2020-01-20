#!/usr/bin/env bash

# Whenever a Patcher creates a Patch formula, this Script is called.
# It creates a clone of the origin repository (which needs to be bare).
# After the patcher has developed successfully and won the election for their patch,
# this script is called again and merged with the origin repository.
#

# Wie erstellt man einen Patch?
# 1. Man füllt ein Formula auf der Webseite aus
# 2. Patcher schreibt seinen Patch, kann auf das Repo zugreifen durch: https://dev.demnet.org/joris/direct-messages.git
# 3. Wenn Patch fertig, erstelle Wahl
#  - Wird das Patch Repo Readonly
# Wenn die Wahl gewonnen wird nach einer Deadline

# bash patch.sh create <origin_repo --bare> <patcher's name> <patch name>
if [ $1 = "create" ]
# $2 = Path of Origin Repository
# $3 = Name of the Patcher (all without whitespaces)
# $4 = Name of the Patch (all without whitespaces)
then
  location="$PATCHES/$3-$4"
  if [[ ! -e $location ]]
  then
    echo "git clone $2 $location"
    git clone $2 $location
  fi
# bash patch.sh merge <patcher's name> <patch name>
elif [ $1 = "merge" ]
# $2 = Name of the Patcher (without whitespaces)
# $3 = Name of the Patch
then
  current_pwd=pwd
  location=$PATCHES/"$2-$3"
  if [[ ! -e $location ]]
    then
      cd $location
      git push
    else
      echo "No Patch with that name"
  fi
else
  echo "Please provide a command"
fi
