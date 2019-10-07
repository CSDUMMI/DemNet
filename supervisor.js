/*
Create Supervisor Node.
This node is the centralized element of the alpha element.

It holds a list of all accepted users' id.
( In a simple JSON File )
These are always participants to the elections,
which the Supervisor initializes.

It also has a buffer of File IDs for each user,
whom you send a message by adding an ID to that.
*/
async function main() {
  const fs      = require( 'fs' );
  const express = require( 'express' );
  const crypto  = require( 'crypto' );
  const node    = await require( './node' ).init_node();
  const app     = express();
  const current = process.env.CURRENT; // CID of the current codebase on IPFS
  const PORT    = 3000;

  let users     = JSON.parse( fs.readFileSync( 'users.json' ) );
  let elections = JSON.parse( fs.readFileSync( 'elections.json' ) );

  app.get( '/send', async ( req, res ) => {

    const user_id     = req.query.user_id;
    const message     = req.query.message;
    const type        = req.query.type;
    try {
      const content_id  = await node.create( type, message );

      users[ user_id ].messages.push( content_id.hash );
      res.json( true );
    } catch( e ) {
      console.error( e );
    }
  });

  app.get( '/vote', async ( req, res ) => {

    const vote        = req.query.vote;
    const election_id = req.query.election_id;

    const vote_id     = await node.create( "vote", vote );
    elections[ election_id ].push( vote_id.hash );
    res.json( vote_id.hash );

  });

  app.get( '/messages', async ( req, res ) => {

    const user_id     = req.query.user_id;
    const auth        = req.query.auth; // "AUTH" String encrypted using private_key

    const user        = JSON.parse( await node.cat ( user_id ) );
    const public_key  = crypto.createPublicKey( {
      key     : user[ 'public_key' ],
      format  : 'pem'
    } );

    const verify      = crypto.createVerify( 'SHA256' );
    verify.write( 'AUTH' );
    verify.end();
    if( verify.verify( public_key, auth ) ) {
      const messages  = [];
      for( message in users[ user_id ].messages ) {
        messages.push( await node.read_json( message['content'] ) );
      }
    } else {
      res.json( false );
    }

  })

  app.get( '/register', async ( req, res ) => {
    const name        = req.query.name;
    const password    = req.query.password;

    const { publicKey, privateKey } = crypto.generateKeyPairSync( 'rsa', {
      modulusLength       : 2048,
      publicKeyEncoding   : {
        type        : 'spki',
        format      : 'pem'
      },
      privateKeyEncoding  : {
        type        : 'pkcs8',
        format      : 'pem',
        cipher      : 'aes-256-cbc',
        passphrase  : password
      }
    });

    const user_id     = await node.create( 'user', JSON.stringify( {
      name        : name,
      public_key  : publicKey,
      private_key : privateKey,
      expires     : Date.now() + 63072000 // Expires in 2 years
    } ) );
    users[ user_id ] = {
      messages : [ {
          type      : "text",
          content   : "QmcbycSTKySJ9P2MxwERfmYuA42943BkEZ8U3dC1Gu2Wew"
       } ],
    }
    res.json ( user_id );

  })

  app.get( '/current', async ( req, res ) => {
    res.send( current );
  } );

  app.listen( PORT, () => console.log( `Listening on ${PORT}`))
}
main();
