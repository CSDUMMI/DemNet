const express       = require('express');
const cookieParser  = require('cookie-parser');
const bodyParser    = require('body-parser');
const session       = require('express-session');

const app           = express()
const port          = process.env.PORT;
const host_data     = (process.env.DATA=5555,process.env.DATA_PORT);
const SECRET        = process.env.SECRET;
// Own module
let options         = { root : __dirname };

const users         = require('./users');
const db            = require('./database');


app.set('view engine', 'ejs');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended : true }));

app.use(cookieParser());
app.use(express.static('public'));


app.post( '/login', ( req, res ) => {
  const password  = req.body.password;
  const username  = req.body.username;

});

app.use( session( {
  secret            : SECRET,
  resave            : true,
  saveUninitilized  : false,
  name              : 'sessionId'
} ) );

app.get(  '/', ( req, res ) => {
  if( req.session.logged_in ) {
    res.render( 'pages/index', { feed : req.session.feed } );
  } else {
    res.render( 'pages/login' );
  }
});




app.listen(port, () => console.log(`Example app listening on port ${port}!`));
