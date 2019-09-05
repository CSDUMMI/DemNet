const fs = require('fs');

const db = JSON.parse( fs.readFileSync( "database.alpha.json" ) );
const save_point = 0;
process.env.CHANGES = process.env.CHANGES ? process.env.CHANGES : 10;

function password_of( name ) {
  return db.users[name].pass;
}

function create_user( username, email, password_hash ) {
  if (db.users.hasOwnProperty(username)) res.redirect('/register');
  db.users[username] = {
    'pass'      : password_hash,
    'email'     : email,
    'content'   : [],
    'followed'  : [],
    'feed'      : []
  }
  save();
}

/*
add_content created by username.
After content has been added,
all followers feeds gets a reference
to the content.
*/
function add_content( username, content ) {
  if( db.users.hasOwnProperty( username ) ) {
    content_id = {
      'author'     : username,
      'index'      : db.users[username].length
    }

    db.users[username].content.push( content );

    for( follower in db.users[username].followed ) {
      db.users[follower].feed.push( content_id );
    }
  }
}

/*
get_feed:
Return string array of all contents, relevant
for the username.
It returns max contents
*/
function get_feed( username, max=256 ) {
  raw_feed = [];
  for ( let i = 0; i < max; i++ ) {
    content = db.users[ username ].feed[ i ];
    raw_feed.push( db.users[ content.author ].content[ content.index ] );
  }
  return raw_feed;
}

/*
get_field:
Get simple fields, without parsing
*/
function get_field( field, username ) {
  const fields = {
    'email'     : 'email',
    'feed'      : 'feed',
    'followed'  : 'followed',
    'content'   : 'content'
  };
  field = fields[ field ] ? field : "ERROR";
  const field_values = db.users[ username ][ field ];
  return field_values;
}

// All process.env.CHANGES || 100, save the state
function save() {
  // Save the db in json
  if ( save_point > process.env.CHANGES ) {
    db_string = JSON.stringify ( db );
    fs.writeFile( "database.alpha.json", db_string, ( error ) => {
      if ( error ) {
        console.error( `ERROR Writing to File:\n${ error }` );
      }
      console.log( "SAVED state" );
    } );
  }
}

module.exports = {
  password_of : password_of,
  create_user : create_user,
  add_content : add_content,
  get_feed    : get_feed,
  get_field   : get_field,
  key         : process.env.SECRET,
}
