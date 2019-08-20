const crypto = require('crypto');
/*
Personal function library
*/

// Object that can't be touched by main.js or anyother library
let logged_in = {};


// All routes after this middleware are only accessible for logged in users
function authenticate(req,res,next) {
  name = req.cookies.name;
  key = req.cookies.auth;
  if ( logged_in[name] == key && key != undefined && name != undefined ) {
    next();
  } else {
    res.redirect("/login");
  }
}

function login (name,pass) {
  // Neither name nor pass can be undefined
}

module.exports = {
  login : login,
  authenticate: authenticate
}
