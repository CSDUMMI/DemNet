/*
Server to access IPFS Files encrypted
and create new files on IPFS
*/

async function main() {
  const crypto      = require( 'crypto' );
  const util        = require( 'util' );
  const IPFS        = require( 'ipfs' );
  const express     = require( 'express' );
  const bodyParser  = require( 'body-parser' );
  const app         = express();
  const PORT        = 3000;
  const node        = await IPFS.create();

  app.use( bodyParser() );

  app.get( "/create", async ( req, res ) => {
    const type        = req.query.type;
    const content     = req.query.content;
    const content_id  = await node.add( JSON.stringify( { type : type, content : content } ) );
    console.log( content_id );
    res.json( content_id );
  });

  app.get( "/read", async ( req, res ) => {
    const id          = req.query.id;
    const content     = await node.cat( id );
    res.json( content.toString() );
  });

  app.get( "/read_json", async ( req, res ) => {
    const id          = req.query.id;
    const encoding    = req.query.encoding ? req.query.encoding : "utf-8";
    const content     = await node.cat( id );
    res.json( JSON.parse( content.toString( encoding ) ) );
  });


  app.listen( PORT, () => console.log( `Listening on localhost:${PORT}` ) );
}

main();
