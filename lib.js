const crypto = require('crypto');
const fs = require('fs');
/*
Personal function library
*/

// Module state

// Database JSON file ( dev only | alpha only)
// Don't use this variable directly, use the wrapper functions
let database = JSON.parse(fs.readFileSync("./database.alpha.json"));

// Object that can't be touched by main.js or anyother library
let logged_in = {};

// Database handlers ( wrappers )

function pass_of(username) {
  return database.users[username] ? database.users[username] : "0x0"; // Return sha256(pass)
}

// Authentication / User login and registration

// All routes after this middleware are only accessible for logged in users
function authenticate(req,res,next) {
  name = req.cookies.get('name');
  key = req.cookies.get('auth');
  if ( logged_in[name] == key && key != undefined && name != undefined ) {
    next();
  } else {
    res.redirect("/login");
  }
}

function login (name,pass) {

  let hash = crypto.createHash('sha256');
  pass = hash.update(pass).digest('hex');
  if( pass != pass_of(name)) {
    return false;
  } else if (pass_of(name) == "0x0") {
    // Username doesn't exist
    return false;
  }
  return logged_in[name] ? logged_in[name] : false; // Change undefined to false
}

module.exports = {
  login : login,
  authenticate: authenticate
}
