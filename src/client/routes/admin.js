var express = require('express');
var router = express.Router();
var { requireAuth } = require('express-openid-connect');

router.get('/admin', function (req, res, next) {
    res.render('login', { dest: 'http://localhost:3000/server/login' })
});

module.exports = router;