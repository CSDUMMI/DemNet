# Database Architecture

The Database uses MongoDB.
The Database is called `demnet`.

The Database contains the following
collections:

1. [`elections`](#elections), the collection of the Elections
2. [`patches`](#patches), the collection of the Patches Metadata.
3. [`laws`](#laws), the collection of the human readable Laws.
4. [`users`](#users), the collection of the user's information and personal data.
5. [`messages`](#messages), the collection of the user's messages. Posts are a special kind
of messages addressed to everybody and signed with only the public key of the author.

# elections
A sample Election Document looks like this:
```json
{ "proposals" : [<proposals>]
, "deadline" : [<deadline>]
, "closed" : <Bool: is Closed?>
, "winner" : <Winner Proposal>
, "type" : "<either machine or human>"
}
```
There can be two kinds of proposals:
Human and Machine Executable Proposals.
These derive from the two kinds of "laws"
our network has:
Human Executable and Machine Executable Laws.
While Human Executable Laws are stored in the `laws` collection
and can be downloaded as a Text Document, the Machine Executable
Laws are the Git Repository and can be cloned, pushed, pulled and
patched.

Any Election can only be held between proposals of the same kind.
So nobody can vote between a human executable and machine executable law
as two alternative proposals.
All proposals in the `proposals` list are alternatives to each other.

## Human Executable Proposals
These kinds of laws are stored in the `laws` collection.
There they are subdivided into distinct groups called "books".
A proposal can only amend, remove and add to a single book
and an election about human executable laws can only
have proposals for the same books.
```json
{ "book" : "<book_id>"
, "title" : "<title>"
, "ammendments" : [ { "law" : "<law_title>"
                    , "paragraphs" :
                      [ "<§1 ammended>"
                      , "<§2 ammended>",
                      "<…>"]
                    }
                  ]
, "additions" : [ { "title" : <unique title in the book>
                  , "paragraphs" : [ <§1>, <§2>, …]
                  }
                ]
, "removals" : [ <law title> ]
}
```

## machine executbale proposals
These are simpler in structure,
because most of the data is present
on disk in a Repository.
```json
{ "patch_id" : "<hash field of the patch in demnet.patches" }
```

# patches
A Patch is all the metadata about a patch,
that has been or is still in process of being developed.
```json
{ "patcher" : <patcher>
, "is_user" : <True if patcher is user of demnet>
, "name" : <name of the patch>
, "simple_description" : <simple description using simple language>
, "technical_description" : <detailed description of the patch>
, "hold_pre_election" : <True if the patcher wants to hold an election, before starting development>
, "references" : <Links relevant to the patch>
, "closed" : <True if the patch has been closed>
, "hash" : "<SHA256 of all the other fields>"
}
```
This Collection is soley managed by `Patches.py`
# laws
Laws are subdivided into books of the same responsibility.
A Law Document looks like this:
```json
{ "book" : <book_id>
, "title" : <unique title in the book>
, "paragraphs" : [ <§1>, <§2>, …]
}
```

# users
For every Registered user there is a
Public and Private PGP Key (GnuPG):
```json
{ "public_key" : "<RSA Public Key>"
, "private_key" : "<Encrypted RSA Private Key>"
, "username" : "<unique username>"
, "first_name" : "<first real name>"
, "last_name" : "<last real name>"
, "expiration" : "<date of expiration of key pair>"
, "feed" : ["<hash of message where this user is either in the to or from part>"]
, "readings" : ["<hash of messages, that the user is reading>"]
, "writings" : ["<hash of messages, that the user is writing>"]
, "old_keys" : [{ "expiration" : "<unix timestamp of their expiration>"
                , "public_key" :"<old public key until the expiration>"
                , "private_key" : "<old, encrypted private key>"
                }]
}
```

# messages
Anybody can send end-to-end encypted messages to anyone.
A message, that is addressed to `all` is a post.
The process of encrypting and decrypting a message
from Alice to Bob is like this:

    Alice's Message -> Alice's Private Key -> Bob's Public Key -> Send -> Bob's Private Key -> Alice's Public Key

A post is just signed by the author

    Alice's Message -> Alice's Private Key -> Published

```json
{ "from" : "<username of the author>"
, "to" : [ "<username's of the recipients or 'all', when the message is a post>" ]
, "body" : [{ "recipient_name" : "<username of the recipient>"
  , "ciphertext" : "<encrypted text of the message, D(D(body, recipient_private_key), author_public_key) == message>"
  }]
, "hash" : "<SHA256 of a dict of all the other fields in the message, used as unique and secure identifier>"
, "draft" : <true if message is a draft and not yet ready to be send.>
}
```
If in "to" there is `"all"` then the body isn't encrypted
and everybody can read it, but only those
users who are also in `"to"` get notification or something
of the sort.
