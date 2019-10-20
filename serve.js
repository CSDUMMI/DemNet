const express = require('express');
const app     = express();
const port    = 3000;
const options = {  root: __dirname };

app.use( express.static( "static/" ) );

app.get( "/", ( req, res ) => {
  res.sendFile( "/views/index.html", options );
});

app.get( "/login", ( req, res ) => {
  res.sendFile( "/views/login.html", options );
});

app.get( "/register", ( req, res ) => {
  res.sendFile( "/views/register.html", options );
});

app.get( "/feed", ( req, res ) => {
  res.sendFile(  "/views/feed.html", options );
})

app.get( "/vote", ( req, res ) => {
  res.sendFile( "/views/vote.html", options );
});

app.listen( port, () => console.log( "Serving static files on port 3000") );
