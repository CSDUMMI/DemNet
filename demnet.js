const express       = require('express');
const cookieParser  = require('cookie-parser');
const bodyParser    = require('body-parser');
const session       = require('express-session');
const crypto = require('crypto');

const app           = express()
const port          = process.env.PORT;
const host_data     = (process.env.DATA=5555,process.env.DATA_PORT);
const secret        = process.env.SECRET;
// Own module
let options         = { root : __dirname };

const users         = require('./users');
const db            = require('./database');


app.set('view engine', 'ejs');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended : true }));

app.use(cookieParser());
app.use(express.static('public'));

app.use( session( {
  secret            : secret,
  resave            : true,
  saveUninitialized : false,
  name              : 'sessionId'
} ) );

app.get( '/login', ( req, res ) => {
  if( req.session.logged_in ) {
    res.redirect( '/' );
  } else {
    res.render( 'login' );
  }
} );

app.post( '/login', ( req, res ) => {
  const password  = req.body.password;
  const username  = req.body.username;
  const hmac      = crypto.createHmac( 'sha256', secret ).update( password );
  if( db.password_of( username ) == crypto.createHmac('sha256', secret).digest( 'hex' ) ) {
    req.session.logged_in = true;
    res.redirect('/');
  } else {
    res.redirect('/login');
  }
});


app.get(  '/', ( req, res ) => {
  if( req.session.logged_in ) {
    res.render( 'index', { feed : req.session.feed } );
  } else {
    res.render( 'login' );
  }
});




app.listen(port, () => console.log(`Example app listening on port ${port}!`));
