const express = require('express');


const app       = express();
const port      = process.env.PORT;

app.use( static( 'public' ) );

app.get( '/', ( req, res ) => {
  res.sendFile( '/pages/index.html' );
});

app.get( '/feed', ( req, res ) => {
  res.sendFile( '/pages/index.html' );
});

app.get( '/login', ( req, res ) => {
  res.sendFile( '/pages/login.html' );
});

app.get( '/register', ( req, res ) => {
  res.sendFile( '/pages/register.html' );
}

app.listen(port, ()  => console.log(  `Serving files on 0.0.0.0:${port}`  ) );
