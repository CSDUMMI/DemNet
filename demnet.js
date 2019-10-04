/*
Supervisor Node
Load this, if you want to start a
node, that can be a supervisor.

*/

// Require priv_key to exist: ( of the user running this node)
const crypto = require('crypto');

const user_id   = process.argv[2];
const password  = process.argv[3];

const IPFS    = require( 'ipfs');
const node    = new IPFS();

node.once( 'ready', () => {
  user = node.cat( user_id, ( error, user ) => {
    if( error ) return console.error( error );

    user = JSON.parse( user );

    const public_key = crypto.createPublicKey({
      key   : user['public_key'],
      format: 'pem'
    });

    // Use the password to encrypt the private_key.
    // Thus you can verify that the user has at least the right password.
    const private_key = crypto .createPrivateKey({
      key       : Buffer.from( user[ 'private_key' ] ),
      passphrase: password,
      format    : 'pem'
    });

    // Verify that keys belong to each other
    if(! belong( public_key, private_key ) ) {
      throw "Error in verifying";
    }
  });

});

function belong( public_key, private_key ) {
  // Create sign of "BELONGS" string and if the same string comes out on decryption,
  // public_key belongs to private_key.
  return true;
}
