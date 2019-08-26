const express       = require('express');
const cookieParser  = require('cookie-parser');
const bodyParser    = require('body-parser');

const app           = express()
const port          = 3000

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

app.get('/feed', (req,res) => {
  console.log("GET /feed")
  res.sendFile('pages/feed.html',options);
} );


app.listen(port, () => console.log(`Example app listening on port ${port}!`));
