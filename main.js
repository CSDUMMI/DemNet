const express       = require('express');
const cookieParser  = require('cookie-parser');
const bodyParser    = require('body-parser');

const app           = express()
const port          = process.env.PORT;

// Own module
const users         = require('./users');
const db            = require('./database');

let options = { root : __dirname };

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended : true }));

app.use(cookieParser());
app.use(express.static('public'));



app.get( '/', (req,res) => {
  console.log("GET /");
  res.sendFile('pages/index.html',options)
} );

app.get( '/register', (req,res) => {
  console.log("GET /register")
  res.sendFile('pages/register.html',options);
} );

app.post( '/register', users.register(db), () => res.redirect('/feed'))


app.get( '/login', (req,res) => {
  console.log("GET /login");
  res.sendFile('pages/login.html', options);
} );

app.post('/login', users.login(db), (req,res,next) => res.redirect('/feed'));


app.use(users.authentication());

app.get( '/feed', ( req, res ) => {
  console.log( "GET /feed" );
  res.sendFile( 'pages/feed.html', options );
} );

app.post( '/feed', ( req, res ) => {
  console.log ( "POST /feed" );
  // req.cookies.username is the username, that is authenticated
  feed = db.get_feed( req.cookies.username, req.body.maximum );
  res.set( 'Content-Type', 'application/json' );
  res.send( JSON.stringify( { 'feed' : feed } ) );
} );


app.post( '/data:field', ( req, res ) => {
  console.log( "GET /data" );
  res.set( 'Content-Type', 'application/json' );
  res.send( JSON.stringify( { 'data' : db.get_field( req.params['field'], req.cookies.username ) } ) );
} );

app.post( '/create', ( req, res ) => {
  console.log( "POST /create");
  db.add_content( req.cookies.username, req.body.content );
  res.set( 'Content-Type', 'text/plain' );
  res.send( created.toString() );
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`));
