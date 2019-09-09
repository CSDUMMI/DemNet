const express = require('express');


const app       = express();
const port      = process.env.PORT;

app.get('/', ( req, res ) => {
  res.sendFile( '/pages/index.html' );
});

app.get('/feed', ( req, res ) => {
  res.sendFile( '/pages/index.html' );
});

app.listen(port, ()  => console.log(  `Serving files on 0.0.0.0:${PORT}`  ) );
