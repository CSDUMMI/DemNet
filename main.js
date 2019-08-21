const express = require('express');
const cookieParser = require('cookie-parser');
const app = express()
const port = 3000

// Own module
const lib = require('./lib');

let options = {
  root : __dirname,

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
  if (req.body.hasOwnProperty('name')
      && req.body.hasOwnProperty('auth')
    ) {
    let name = req.query.name;
    let pass = req.query.pass;

    let auth = lib.login(name,pass);
    if (!auth) {
      // Redirect to login if wrong pass/name
      res.redirect("/login");
    }
    res.cookie("auth",auth);
  } else {
    res.redirect("/login");
  }
})

app.use(lib.authenticate);

app.get('/feed', (req,res) => {
  console.log("GET /feed")
  res.sendFile('pages/feed.html',options);
});


app.listen(port, () => console.log(`Example app listening on port ${port}!`));
