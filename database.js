const fs = require('fs');

const db = JSON.parse(fs.readFileSync("database.alpha.json"));
const save_point = 0;
process.env.CHANGES = process.env.CHANGES | 10;

function password_of(name) {
  return db.users[name].pass;
}

function create_user(username,email,password_hash) {
  if ( save_point >= process.env.CHANGES) save();
  if (db.users.hasOwnProperty(username)) res.redirect('/register');
  db.users[username] = {
    'pass'      : password_hash,
    'email'     : email,
    'content'   : []
  }
}

// All process.env.CHANGES || 100, save the state
function save() {
  // Save the db in json
  db_string = JSON.stringify ( db );
  fs.writeFile("database.alpha.json", db_string, ( error ) => {
    if ( error ) console.error(`Error: Writing to File:\n${ error }`);
    console.log("Saved state");
  });
}

module.exports = {
  password_of : password_of,
  create_user : create_user,
  key : process.env.SECRET,
}
