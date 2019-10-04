/*
Supervisor Node
Load this, if you want to start a
node, that can be a supervisor.

*/

// Require priv_key to exist: ( of the user running this node)
const crypto = require('crypto');

const user_id   = process.argv[2];
const password  = process.argv[3];

const util      = require('util');
const IPFS      = require( 'ipfs');

function init_node( password, user_id ) {
  const node      = new IPFS();
  const node_once = util.promisify( node.once );

  let node_ready  = node_once( 'ready' );

  node_ready.then( node => {
    cat   = util.promisify( node.cat );
    user  = cat( user_id );

    user.then( user_id, ( error, user ) => {

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
        throw "Invalid Keys provided, Invalid user ID";
      }

    });

    user.catch( console.error );

  });

  node_ready.catch( console.error );

  return node_ready;
}

function belong( public_key, private_key ) {
  // Create sign of "BELONGS" string and if the same string comes out on decryption,
  // public_key belongs to private_key.

  const sign      = crypto.createSign( "SHA256" );
  sign.write( "BELONGS" );
  sign.end();
  const signature = sign.sign( private_key, 'hex' );

  const verify    = crypto.createVerify( 'SHA256' );
  verify.write( 'BELONGS' );
  verify.end();
  return verify.verify( public_key, signature );

}

module.exports = {
  init_node : init_node,
  belong    : belong
}
