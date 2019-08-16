const express = require('express');
const crypto = require('crypto');
const fs = require('fs');
const app = express()
const port = 3000

let options = {
  root: __dirname,
  dotfiles: 'deny',
  headers: {
    'x-timestamp': Date.now(),
    'x-sent': true
  }
}


function load_login_info(user) {
  // Return SHA256 of pass of user
}

app.use(express.json()); // for parsing application/json
app.use(express.urlencoded( { extended: true })) // for parsing application/x-www-form-urlencoded

app.get('/', (req,res) => {
  res.sendFile('pages/index.html',options)
});

app.get('/register', (req,res) => {
  res.sendFile('pages/register.html',options);
});

app.get('/login', (req,res) => {
  res.sendFile('pages/login.html', options);
});

app.post('/login', (req,res) => {
  if (authenticate(req.body['name'],req.body['pass'])) {;
    res.
  }

  res.send("LOGGED IN");
});

app.get('/feed', (req,res) => {
  res.sendFile('pages/feed.html',options);
});

app.use(express.static('public'));

app.listen(port, () => console.log(`Example app listening on port ${port}!`));
