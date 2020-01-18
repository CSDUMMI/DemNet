import Patches
import random, os, string
from pymongo import MongoClient

def random_string():
    return ''.join(random.choice(string.printable) for i in range(random.randint(0,500)))

def generate_random_patch():
    patcher = random_string()
    patch   = random_string()

    options =   { "is_user"                 : random.choice([True, False])
                , "simple_description"      : random_string()
                , "technical_description"   : random_string()
                , "hold_pre_election"       : random.choice([True, False])
                , "references"              : [ random_string() for i in range(random.randint(0,5000)) ]
                }
    return (patcher, patch, options)

def test_patch():
    os.environ['PATCHES'] = "/tmp/demnet_test"
    os.environ['ORIGIN_REPOSITORY'] = "/tmp/demnet_origin"
    
    (patcher, patch, options) = generate_random_patch()

    patch_hash = Patches.create(patcher, patch, options)

    assert os.path.isdir(f"{os.environ['PATCHES']}/{patcher}-{patch}")

    client  = MongoClient()
    db      = client.demnet
    patches = db.patches

    patch_formula = patches.find_one({ "hash" : patch_hash })

    assert patch_formula['patcher'] == patcher
    assert patch_formula['is_user'] == options['is_user']
    assert patch_formula['name'] == patch
    assert patch_formula['simple_description'] == options['simple_description']
    assert patch_formula['technical_description'] == options['technical_description']
    assert patch_formula['hold_pre_election'] == options['hold_pre_election']
    assert patch_formula['references'] == options['references']
    assert patch_formula['closed'] == False

    (patcher_2, patch_2, options_2) = generate_random_patch()

    patch_2_hash = Patches.create(patcher, patch, options)

    # Close Patches without merging
