var bodyParser = require('body-parser');
var express = require('express');
var path = require('path'); 
var cors = require('cors');
var index = require('./routes/index');
var passport = require('passport');
var news = require('./routes/news');
var app = express();
var auth = require('./routes/authentication');
var config = require('./config.json');

app.use(bodyParser.json());
require('./models/main.js').connect(config.mongoDbUri);

// view engine setup
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

app.use(cors());

app.use(passport.initialize());
var login = require('./auth/login');
var signup = require('./auth/signup');
passport.use('signup', signup);
passport.use('login', login);
// console.log('reach here');
const tokenCheck = require('./middleware/pass_check');

app.use('/', index);
app.use('/auth', auth);
app.use('/news', tokenCheck);
app.use('/news', news);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  res.status(404);
});

module.exports = app;