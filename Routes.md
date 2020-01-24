# All the Routes of the HTTP Server
There are two kinds of people,
that will use the Server:
- Contributors
Anyone changing the site in any way
- Users
Anyone registered on the network

Thus any route can be allocated to one
of those groups.

## Contributors 
This Group can be separated again, which can be seen in
this Venn diagram:

![Contributors-Developer-Patcher](Contributors.png)

Developers are all Contributors, working on the Source Code,
the difference to the other Contributors is, that Contributors
may also only or also change the human executable laws of the network,
which have rather little to do with Source Code.
Another subgroup in Developers are the Patchers, who are all
developers, currently working on their own Patch.

## Users
**All Users are guranteed to be human!**
This is important and to gurantee it, we don't have
a public register function **yet**.
All Users receive a RSA key pair,
which are used to encrypt their messages when stored on the 
server.
The private key is encrypted using a random string encrypted again by the password of the user.
This is done to provide security, for example preventing the storage of the plain text password
of the user in either session or client.


# Routes
## Contributor Routes
