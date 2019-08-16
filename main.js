const express = require('express');
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
app.get('/', (req,res) => res.sendFile('pages/index.html',options));
app.get('/register', (req,res) => res.sendFile('pages/register.html',options));
app.get('/login', (req,res) => res.sendFile('pages/login.html', options));
app.get('/feed', (req,res) => res.sendFile('pages/feed.html',options));

app.use(express.static('public'));

app.listen(port, () => console.log(`Example app listening on port ${port}!`));
