#!/usr/bin/env python3
import subprocess, os, json
from Crypto.Hash import SHA256
from pymongo import MongoClient

"""
Env Variables:
$PATCHES : Folder with the Git Repositories of the Patches (format: patcher-patch/)
$ORIGIN_REPOSITORY : Location of the Original Git Repository, from which patches are cloned from
and to whom patches are pushed after being approved.

create a patch:
- clone the origin_repository, as stored in the $ORIGIN_REPOSITORY envvar.
- create an entry in the collection patches on the demnet database.

This patch needs the following options:

- The name of the patcher, that can either be the username in demnet
or a pseudonyme chosen by a non-user, which will then be noted in a separate
variable called "is_user".

- The name of the patch, that should be descriptive (hopefully)

- The simple_description of the patcher's intent.
This is useful for users, if the patcher wants to hold an election before
starting development. These users won't often be interested in the technical
details, for whom this description should suffice.

- The technical_description is for all developers trying to understand
the patcher's intent on a deeper level.

- As part of the technical_description, the patcher can also reference issues,
bug reports and generally link to ressources, detailing his intention.
This is separatly done in the "references" field.
The Patcher should put a most conclusive list here
and reference only some of it in the descriptions.

- The Patcher may not want to start developing, waste hours and hours of time,
and see that the users don't even have an interest their patch.
All patches have to pass an election eventually, but if the patcher wants to,
they can hold an election before starting to develop, just to see if there
is any interest. If the election is lost, the patcher will either have to delete
the patch or modify it substantially. If they want to hold such an election,
"hold_pre_election" must be set to True.

- After the Patch has been closed and the Patch Repository deleted, the
patch entry gets two additional fields, called "closed" = True

- And "refs", which are all the git-commit ids, that this patch created.
This is, so you can easily see what changes have been made in this patch
and generate a Diff. (This could be done with git-blame too, maybe.)
Returns:
After creating the patch,
a SHA256 of all the data is created and
returned as the reference to the patch.
This is also put into one field called "sha256".
(That this isn't included in the calculation of the hash is self-evident.)
"""
def create(patcher,patch_name, options):
    client = MongoClient()
    db = client.demnet
    patches = db.patches
    patch = { "patcher" : patcher
            , "is_user" : options['is_user']
            , "name" : patch_name
            , "simple_description" : options['simple_description']
            , "technical_description" : options['technical_description']
            , "hold_pre_election" : options['hold_pre_election']
            , "references" : options['references']
            , "closed" : False
            }
    patch['hash'] = SHA256.new(data=json.dumps(patch).encode('utf-8')).hexdigest()
    patch_id = patches.insert_one(patch).inserted_id

    subprocess.run(['bash', 'patch.sh', 'create', os.environ["ORIGIN_REPOSITORY"], patcher, patch_name])

    return patch['hash']

def merge(patcher, patch_name):
    subprocess.run(['bash', 'patch.sh', 'merge', patcher, patch_name])

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

    if (not (patch == None)) and os.path.isdir(os.environ['PATCHES'] + "/" + patcher + "-" + patch_name):
        if merge:
            merge(patcher, patch_name)

        subprocess.run(["rm", os.environ['PATCHES'] + "/" + patcher + "-" + patch_name])

        patches.update_one({ "hash" : id }, { "$set" : { "closed" : True } })
        return True
    else:
        return False
