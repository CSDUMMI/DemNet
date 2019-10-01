/*
API Interface between IPFS
and a frontend.
All API calls are through POST.
Their arguments are in the body.
I will write them like this:

POST /uri
Argument1   : Description1
Argument2   : Description2



POST /vote
signed_vote : Vote signed by the user's temporary private key.
election_id : ID of the election to be used. ( CID of it's Ballot File )
supervisor  : "you", so this server by default,nothing else possible yet.
res         : Response Object, Returns either "success" or "failure"
POST /user_info

*/
const IPFS      = require( 'ipfs' );
const express   = require('express' );
const app       = express();
async function get_node() {
  return await IPFS.create();
}

const node      = get_node();

IPFS.files.mkdir( '/elections');

app.post( "/vote", ( req, res ) => vote( req.body.signed_vote, req.body.election_id, req.body.supervisor, res ) );


async function vote( vote_signed, election_id, supervisor, res ) {
  election = JSON.parse( await node.cat( election_id ) );

  // These tests aren't required to make voting work, but they protect from spamming.
  let success = "failure";
  if( election.deadline >= Date.now() ) {
    success = "failure";
  }  else {
    node.files.read( "elections/" + election_id )
    success = "success";
  }
}
