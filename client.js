/*
Run simple Node, where a single user is logged in.
*/

const user_id   = process.argv[2];
const password  = process.argv[3];

const demnet    = require( './demnet' );
const crypto    = require( 'crypto' );
const util      = require( 'util' );

node  = demnet.init_node( password, user_id );

node.catch( console.error );

function publish_content( content, content_type ) {
  switch( content_type ) {
    case "text":

      break;
    default:

  }
}
