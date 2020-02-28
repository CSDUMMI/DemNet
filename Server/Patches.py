#!/usr/bin/env python3
import subprocess, os, json
from Crypto.Hash import SHA256
from pymongo import MongoClient
from typing import List

def create  ( patcher                   : str
            , patch_name                : str
            , is_user                   : bool
            , simple_description        : str
            , technical_description     : str
            , references                : List[str]
            ):
    client = MongoClient()
    db = client.demnet
    patches = db.patches
    patch = { "patcher" : patcher
            , "is_user" : is_user
            , "name" : patch_name
            , "simple_description" : simple_description
            , "technical_description" : technical_description
            , "references" : references
            , "closed" : False
            }
    patch['hash'] = SHA256.new().update(json.dumps(patch)).encode('utf-8')).hexdigest()
    patch_id = patches.insert_one(patch).inserted_id

    subprocess.run(['bash', 'patch.sh', 'create', os.environ["ORIGIN_REPOSITORY"], patcher, patch_name])

    return patch['hash']

def merge(patcher, patch_name):
    subprocess.run(['bash', 'patch.sh', 'merge', patcher, patch_name])

def lock(patcher, patch_name):
    path_of_patch   = path_of_patch(patcher,patch_name)
    if not path_of_patch:
        return False
    else:
        os.chmod(path_of_patch, 0444) # readonly to all
        return True

"""
Closing a patch means:
Deleting the Git Repo.
Setting the "closed" flag to True.
"""
def close(patcher, patch_name, id, merge=False):
    client = MongoClient()
    db = client.demnet
    patches = db.patches
    patch = patches.find_one( { "patcher"   : patcher
                              , "name"      : patch_name
                              , "hash"      : id
                              , "closed"    : False
                              } )

    repo_path = path_of_patch(patcher, patch_name, check_existence=False)
    if patch and os.path.isdir(repo_path):
        if merge:
            merge(patcher, patch_name)

        print(subprocess.run([f"rm -rf { repo_path }"], shell=True))

        patches.update_one({ "hash" : id }, { "$set" : { "closed" : True } })
        return True
    else:
        return False

def path_of_patch(patcher, patch_name, check_existence=True):
    path    = f"{os.environ["PATCHES"]}/{patcher}-{patch_name}"
    if check_existence:
        return path if os.path.isdir(path) else False
    else:
        return path
