const express = require('express');
const cookieParser = require('cookie-parser');
const app = express()
const port = 3000

// Own module
const lib = require('./lib');

let options = {
  root : __dirname
};

app.use(cookieParser());
app.use(express.static('public'));

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

  let name = req.body.name;
  let pass = req.body.pass;

  let auth = lib.login(name,pass);
  res.cookie("auth",auth);
})

app.use(lib.authenticate);

app.get('/feed', (req,res) => {
  console.log("GET /feed")
  res.sendFile('pages/feed.html',options);
});


app.listen(port, () => console.log(`Example app listening on port ${port}!`));
