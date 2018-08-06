const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;
const config = require('../config.json');

module.exports = new PassportLocalStrategy({
  usernameField: 'email',
  passwordField: 'password',
  session: false,
  passReqToCallback: true
}, (req, email, password, done) => {
  const userData = {
    email: email.trim(),
    password: password
  };

  return User.findOne({ email: userData.email }, (err, user) => {
    if (err) {
        return done(err);
    }

    if (!user) {
      const error = new Error('Authentication failed. Incorrect email or password.');
      error.name = 'AuthenticationError';
      return done(error);
    }
    return user.compare(userData.password, (err, matchValue) => {
        if (err) {
            return done(err);
        }

        if (!matchValue) {
            const error = new Error('Authentication failed. Incorrect email or password');
            error.name = 'AuthenticationError';
            return done(error);
        };
        const payload = {
            sub: user._id
        };
        const token = jwt.sign(payload, config.jwtSecret);
        const data = {
            name: user.email
        };
        return done(null, token, data);
    });
  });
});