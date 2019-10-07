/*
Simple Server, registering users,
logging in users, counting votes,
publishing results.
*/

const fs      = require( 'fs' );
const crypto  = require( 'crypto' );
const express = require( 'express' );
const cookieParser = require( 'cookie-parser' );
const bodyParser = require( 'body-parser' );
const cookieSession = require( 'cookie-session' );
const app     = express();

app.use( cookieParser() );
app.use( bodyParser() );
app.use( cookieSession( {
  name: 'session',
  keys: process.env.SECRET
} ) );

const users = JSON.parse( fs.readFileSync( 'users.json' ) );
const elections = JSON.parse( fs.readFileSync( 'elections.json' ) );

const PORT = 3000;

app.set( 'view engine', 'ejs' );

app.get( '/', ( req, res ) => {
    console.log( 'GET index' );
    res.render( 'index' );
});

app.get( '/home', ( req, res ) => {
  console.log( 'GET home' );
  if( req.session.username ) {
    const username = req.body.username;

    res.render( 'home', { messages : users[ username ].messages, name : username } );
  } else {
    res.redirect( '/' );
  }
});

app.post( '/register', ( req, res ) => {
  if( req.session.username ) {
    res.redirect( '/' );
  } else {

    const username = req.body.username;
    const email = req.body.email;
    const password = crypto.createHmac('sha256', process.env.SUPER_SECRET ).update( req.body.password );

    console.log( 'POST /register' );
    if( !( username in users ) ) {

      users[ username ] = {
        'email'     : email,
        'password'  : password.digest( 'hex' ),
        'messages'  : [
          {
            title   : "Welcome",
            author  : "DemNet Team",
            content : 'Welcome to DemNet. Hope you will participate in the next vote.'
          }
        ]
      };
      req.session.username = username;
      res.redirect( '/home' );
    }

    res.redirect( '/' );
  }
} );

app.listen( PORT, () => console.log( `Listening on ${PORT}` ) );
