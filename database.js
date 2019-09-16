const sqlite = require('sqlite3').verbose();

let db = new sqlite.Database( './database.db', print_error );


function print_error( error ) {
  if( error ) {
    console.error( error.message );
  }
}

function password_of( name ) {
  const query = `SELECT password_hash FROM users WHERE name = ?`;
  db.get( query, [name], ( error, row ) => {

    if( error ) { console.error( error ); }

    return row.password_hash;

  });
}

function create_user( username, email, password_hash ) {
  const query =
  `INSERT INTO users ( entry, name, password_hash, email ) VALUES ( ?, ?, ?, ? )`;

  db.run( query, [ Date.now(), username, password_hash, email], print_error);
}

/*
add_content created by username.
After content has been added,
all followers feeds gets a reference
to the content.
*/
function add_content( username, content, type ) {
  const query = `INSERT INTO contents ( name, content, type, date ) VALUES ( ?, ?, ?, ? )`;

  let date = Date.now();

  db.run( query, [ username, content, type, date ], print_error);

}


/*
follow( username ):
follow username
*/
function follow( ) {

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
  field = fields[ field ] ? field : "content";
  const field_values = db.users[ username ][ field ];
  return field_values;
}

module.exports = {
  password_of : password_of,
  create_user : create_user,
  add_content : add_content,
  get_feed    : get_feed,
  get_field   : get_field,
  key         : process.env.SECRET,
}
