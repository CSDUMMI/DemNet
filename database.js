const fs = require('fs');

const db = JSON.parse(fs.readFileSync("database.alpha.json"));

function password_of(name) {
  return db.users[name].pass;
}

function create_user(username,password_hash) {
  db.users[username] = password_hash;
}

module.exports = {
  password_of : password_of,
  create_user : create_user,
  key : process.env.SECRET,
}
