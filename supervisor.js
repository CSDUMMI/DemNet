/*
Simple Server, registering users,
logging in users, counting votes,
publishing results.
*/

const fs            = require( 'fs' );
const crypto        = require( 'crypto' );
const express       = require( 'express' );
const app           = express();

const bodyParser    = require( 'body-parser' );

app.use( bodyParser.urlencoded( { extended: false } ) );

app.use( bodyParser.json() );

const cookieSession = require( 'cookie-session' );
app.use( cookieSession( {
  name : 'session',
  keys: [ process.env.SECRET ]
} ) )

const users     = JSON.parse( fs.readFileSync( 'users.json' ) );
const elections = JSON.parse( fs.readFileSync( 'elections.json' ) );

app.get( '/', ( req, res ) => {
  if( req.session.username ) {
    // is logged in.

    res.send( JSON.stringify( users[ req.session.username ].messages ) );
  } else {
    req.session.username = "joris";
    res.send( "Please login <a href=\"\/\"> Home </a>" );
  }
});

app.get( '/create', ( req, res ) => {
  if( req.session.username ) {
    const content       = req.query.content;
    const recipient     = req.query.recipient;
    users[ recipient ].messages.push( {
      content : content,
      author  : req.session.username
    } );
    res.send( "Created" );
    fs.writeFileSync( 'users.json', JSON.stringify( users ) );
  } else {
    res.send( "Not created" );
  }
});

app.get( '/login', ( req, res ) => {
  const username = req.query.username;
  const password = req.query.password;

  const encrypted = crypto.createHmac( 'SHA256', process.env.SUPER_SECRET )
                          .update( password )
                          .digest( 'hex' );

  if( users[ username ].password_encrypted == encrypted ) {
    req.session.username = username;
    res.send( 'logged in' );
  } else {
    res.send( 'failure' );
  }

});

app.get( '/register', ( req, res ) => {
  const username  = req.query.username;
  const email     = req.query.email;
  const password  = req.query.password;

  const encrypted = crypto.createHmac( 'SHA256', process.env.SUPER_SECRET )
                          .update( password )
                          .digest( 'hex' );

  if( !( username in users ) ) {
    users[ username ] = {
      'messages' : [
        {
          'title'   : 'Welcome to DemNet',
          'content' :
          'We are happy to see, that you use DemNet.\nHopefully you will participate in upcoming elections.',
          'author'  : 'joris',
          'type'    : 'text'
        }
      ],
      'password_encrypted' : encrypted,
      'email'              : email
    };
    fs.writeFileSync( 'users.json', JSON.stringify( users ) );
    res.send( 'Registered' );
  } else {
    res.send( 'Already registered' );
  }
});

app.get( '/vote', ( req, res ) => {

  const vote      = req.query.vote;
  const election  = req.query.election;
  const username  = req.session.username;

  if( !( username in elections[ election ].participants ) && username ) {
    elections[ election ].participants.push( username );
    elections[ election ].votes.push( vote );
    fs.writeFileSync( 'elections.json', JSON.stringify( elections ) );
    res.send( "Voted, thank you!" );

  } else {

    res.send( "Not voted, because already voted. You can't take back your vote." );
  }

})

app.listen( 3000 );
