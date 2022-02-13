var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var validatorRouter = require('./routes/validator');
var usersRouter = require('./routes/users');
var adminRouter = require('./routes/admin');

var userController = require('./users/users');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/pass', usersRouter);
app.use('/validator', validatorRouter);
app.use('/admin', adminRouter);

const { auth } = require('express-openid-connect');

const config = {
    authRequired: false,
    auth0Logout: true,
    secret: 'a long, randomly-generated string stored in env',
    baseURL: 'http://localhost:3000',
    clientID: 'IH1rDV4TxOsUEsCFgJePKTimT3VU09T8',
    issuerBaseURL: 'https://dev-e8j9xl9z.us.auth0.com'
};

// auth router attaches /login, /logout, and /callback routes to the baseURL
app.use(auth(config));

// give the user object to the views
app.use(function (req, res, next) {
    res.locals.user = req.oidc.user;
    if (req.oidc.isAuthenticated()) {
        if (!(userController.userExists(res.locals.user.name))) {
            userController.addUser(res.locals.user.name);
        }
        const localUser = userController.getUser(res.locals.user.name);
    }
    next();
})

// req.isAuthenticated is provided from the auth router
app.get('/', (req, res) => {
    if (req.oidc.isAuthenticated()) return res.render('index', { localUser: userController.getUser(res.locals.user.name) });
    res.render('login');
});

app.post('/api/user/info', (req, res) => {
    res.send(JSON.stringify(req.body))
})

app.use('/stylesheets/bootstrap', express.static(__dirname + '/node_modules/bootstrap/dist/css'));
app.use('/javascripts/bootstrap', express.static(__dirname + '/node_modules/bootstrap/dist/js'))

// catch 404 and forward to error handler
app.use(function(req, res, next) {
    next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    // render the error page
    res.status(err.status || 500);
    res.render('error');
});

module.exports = app;
