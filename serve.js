const express = require('express');
const app     = express();
const port    = 3000;
const options = {  root: __dirname };

app.get( "/", ( req, res ) => {
  res.sendFile( "/views/index.ejs", options );
});

app.get( "/login", ( req, res ) => {
  res.sendFile( "/views/login.ejs", options );
});

app.get( "/register", ( req, res ) => {
  res.sendFile( "/views/register.ejs", options );
});

app.get( "/feed", ( req, res ) => {
  res.sendFile(  "/views/feed.ejs", options );
})

app.get( "/vote", ( req, res ) => {
  res.sendFile( "/views/vote.ejs", options );
});

app.listen( port, () => console.log( "Serving static files on port 3000") );
