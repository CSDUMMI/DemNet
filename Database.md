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
A proposal can only affect a single 
```json
``

# patches

# laws

# users

# messages
