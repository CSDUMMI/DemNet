/*
Server to access IPFS Files encrypted
and create new files on IPFS
*/

const crypto      = require( 'crypto' );
const util        = require( 'util' );
const IPFS        = require( 'ipfs' );
const express     = require( 'express' );
const bodyParser  = require( 'body-parser' );
const app         = express();
const PORT        = 3000;

app.use( bodyParser() );

app.get( "/create",async ( req, res ) => {
  const type        = req.body.type;
  const content     = req.body.content;
  const node        = await IPFS.create();
  const content_id  = await node.add( JSON.stringify( { type : type, content : content } ) );
  console.log( content_id );
  return JSON.stringify( content_id );
})

app.listen( PORT, () => console.log( `Listening on localhost:${PORT}` ) );
