# Abstract
I want to introduce a system, that ensures
that all voter's choice is secret and
that everybody can check the tally,
without knowing who voted how.
But to ensure the secrecy we need to
have a trusted party, called the supervisor.
This might be automatized by using a Smart Contract
on a Blockchain, that can access IPFS.
Otherwise the whole Election is decentralized  
and can be validated by anyone who wants to.

# Introduction
I wanted to build a social network,
where every user would have a vote
and could decided upon the future development
of the network.
In the early days this network would be very much like
the Athenian democracy, letting anybody vote on anybody,
but without any such restrictions, as the disenfranchisement
of woman, slaves, children and so forth.
Later there would be a simple parliamentary democracy,
similar to the British or representative, like the Germans.
How and when these later systems would be implemented must have been
the decision of the users, as anything else.
But to properly do this, we would have to have a solid mechanism
for holding Elections, of whichever kind.
In Germany we have 4 principles, that every democratic elections
should hold up:

1. Equal, every vote counts the same ( nobody has more influence than another )
2. Immediate, no intermediates, like with the electoral colleague in the USA.
3. Free, every voter can choose whatever they want and must not expect personal reprisals from their choice.
4. Secrecy, nobody knows how a voter voted.

The proposed system cannot ensure all of these and if the supervisor is not
trustworthy, the whole Election is invalid.
But it can ensure both a free and secret Election, as well as another
side effect, which is that everybody can count the votes ( I would call that
principles checkable or controllable ).

# The Supervisor of an Election
Every Election needs a trusted party,
which counts the votes and
administers the Election.
This party cannot take part in the
political process in any other way,
meaning they can't be part of a political party or movement.
Our supervisor initializes an Election by giving each voter a
temporary private key and publishing the public keys on an
IPFS File, which I will call the Public Key Index.
