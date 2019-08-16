const express = require('express');
const app = express()
const port = 3000

app.get('/', (req,res) => res.send('Mainpage'));
app.get('/register', (req,res) => res.send('register'));
app.get('/login', (req,res) => res.send('login'));
app.get('/feed', (req,res) => res.send('feed'));



app.listen(port, () => console.log(`Example app listening on port ${port}!`));
