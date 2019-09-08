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



app.listen(port, () => console.log(`Example app listening on port ${port}!`));
