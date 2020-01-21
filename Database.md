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
{ "book" : <book_id>
, "title" : <unique_title>
, "ammendments" : [ { "law" : <law_title>
                    , "paragraphs" : [ <§1 ammended>, <§2 ammended>, …]
                    }
                  ]
, "additions" : [ { "title" : <unique title in the book>
                  , "paragraphs" : [ <§1>, <§2>, …]
                  }
                ]
, "removals" : [ <law title> ]
}
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

# messages
