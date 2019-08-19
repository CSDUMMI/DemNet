const express = require('express');
const cookieParser = require('cookie-parser');
const bodyParser = require('cookie-parser');
const app = express()
const port = 3000

let options = {
  root : __dirname
};

app.use(cookieParser());
app.use(express.static('public'));

let logged_in = {};

function authenticate(req,res,next) {
  name = req.cookies.name;
  key = req.cookies.auth;
  if ( logged_in[name] == key && key != undefined && name != undefined ) {
    next();
  } else {
    res.redirect("/login");
  }
}


app.get('/', (req,res) => {
  console.log("GET /");
  res.sendFile('pages/index.html',options)
});

app.get('/register', (req,res) => {
  console.log("GET /register")
  res.sendFile('pages/register.html',options);
});

app.get('/login', (req,res) => {
  console.log("GET /login");
  res.sendFile('pages/login.html', options);
});

app.post('/login', (req,res) => {
  console.log("POST /login");
  // Load information (SHA256 of User pass)
  let name = req.body.name;
  let pass = req.body.pass; // SHA256 of the password
  let stored_pass = load_user_pass(name); // SHA256(SHA256(pass))
  if( pass == stored_pass ) {

  }
})
app.use(authenticate);

app.get('/feed', (req,res) => {
  console.log("GET /feed")
  res.sendFile('pages/feed.html',options);
});


app.listen(port, () => console.log(`Example app listening on port ${port}!`));
