/*
Collection of middlewares to:
- Login a user
- Create a session
- Register a user
- Logout a user
- Authenticate a user using sessions
*/
const crypto = require('crypto');

/*
The db object contains wrapper functions
to access whatever Database we are using.
It should have at least these methods:
- create_user ( username, password )
Create a new user and store what is provided as password
and give it back in the same format to password_of()
- password_of( username )
Returns the password of user as set by create_user()
- key
Secure key used for encryption

The usernames must be used no more than once in the program.
*/


// All usernames : auth keys
let logged_in = {}


// Middleware to parse the users login credentials
/*
Expects the username inside req.params.username
and the password in req.params.passsword.
*/
function login(db,login_page="/login",feed_page="/feed") {
  return (req,res,next) => {
    let password = req.body.password;
    let username = req.body.username;
    const hmac = crypto.createHmac( 'sha256', db.key );

    hmac.update(password);
    password = hmac.digest('hex');
    if( password == db.password_of( username ) ) {
      let auth = crypto.createHmac( 'sha256', db.key).update( Math.random(process.env.SEED).toString() ).digest('hex');
      logged_in[username] = auth;
      res.cookie('auth',auth);
      res.redirect(feed_page);

    } else {
      // no this user didn't provide the right password and cannot proceed
      res.redirect(login_page);
    }
  }
}


// Returns middleware that returns the user to a login_page, if the user doesn't have the right credentials
function authentication(login_page="/login") {
  return (req,res,next) => {
    if ( logged_in[req.params.username] == req.params.auth ) {
      next();
    } else {
      res.redirect(login_page);
    }
  }
}

module.exports = {
  authentication : authentication,
  login : login
}
