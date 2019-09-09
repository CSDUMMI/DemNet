const express = require('express');


const app       = express();
const port      = process.env.PORT;

app.use( express.static( 'public' , { root:__dirname }) );

app.get( '/', ( req, res ) => {
  res.sendFile( `${__dirname}/pages/index.html` );
});

app.get( '/feed', ( req, res ) => {
  res.sendFile( `${__dirname}/pages/feed.html` );
});

app.get( '/login', ( req, res ) => {
  res.sendFile( `${__dirname}/pages/login.html` );
});

app.get( '/register', ( req, res ) => {
  res.sendFile( `${__dirname}/pages/register.html` );
});

app.listen(port, ()  => console.log(  `Serving files on 0.0.0.0:${port}`  ) );
