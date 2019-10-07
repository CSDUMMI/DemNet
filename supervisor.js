/*
Simple Server, registering users,
logging in users, counting votes,
publishing results.
*/

const crypto  = require( 'crypto' );
const express = require( 'express' );
const cookieParser = require( 'cookie-parser' );
const session = require( 'express-session' );
const app     = express();

app.use( cookieParser() );
app.use( session( { secret : process.env.SECRET } ) );

const users = JSON.parse( fs.readFileSync( 'users.json' ) );
const elections = JSON.parse( fs.readFileSync( 'elections.json' ) );
app.get( '/', async ( req, res ) => {
  if( req.session.looged_in ) {
    res.send( )
  }
})
