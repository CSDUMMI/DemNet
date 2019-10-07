/*
Simple Server, registering users,
logging in users, counting votes,
publishing results.
*/

const fs      = require( 'fs' );
const crypto  = require( 'crypto' );
const express = require( 'express' );
const cookieParser = require( 'cookie-parser' );
const session = require( 'express-session' );
const app     = express();


app.use( cookieParser() );
app.use( session( { secret : process.env.SECRET } ) );

const users = JSON.parse( fs.readFileSync( 'users.json' ) );
const elections = JSON.parse( fs.readFileSync( 'elections.json' ) );

app.set( 'view-engine', 'ejs' );

app.get( '/', async ( req, res ) => {
  if( req.session.looged_in ) {
    res.render( 'home', { messages : users[ req.session.user_id ].messages } );
  } else {
    res.render( 'index' );
  }
})
