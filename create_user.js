const crypto  = require( 'crypto' );
const fs      = require( 'fs' );
const ipfs    = require( 'ipfs' );

const node    = new ipfs();

node.once( 'ready', () => {
  const user                      = {};
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
      passphrase  : process.argv[2]
    }
  });

  user[ 'name' ]                  = process.argv[3];
  user[ 'expires' ]               = Date.now() + 63072000; // Now + 2 years
  user[ 'public_key' ]            = publicKey;
  user[ 'private_key' ]           = privateKey;

  const user_id                   = node.add( ipfs.Buffer.from( JSON.stringify( user ) ) );
  user_id.then  ( console.log   );
  user_id.catch ( console.error );
});
