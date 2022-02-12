var express = require('express');
var router = express.Router();

router.get('/user/login', function (req, res, next) {
    res.render('login', { dest: 'http://localhost:3000/server/login' })
});

module.exports = router;