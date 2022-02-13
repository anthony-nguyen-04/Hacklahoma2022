var express = require('express');
var router = express.Router();
var { requiresAuth } = require('express-openid-connect');
var FormData = require('form-data');
var fetch = require('node-fetch');
var userController = require('../users/users');

router.use(requiresAuth());

router.get('/', function (req, res, next) {
    fetch('http://localhost:5000/admin/pending')
        .then(response => response.json())
        .then(json => {
            res.render('admin/list', { pending: json.pending });
        })
        .catch(err => {
            console.log(err)
            res.render('admin/list', { pending: [] })
        })
});

router.get('/verify/:id', function (req, res, next) {
    const form = new FormData();
    form.append('id', req.params.id);
    fetch('http://localhost:5000/admin/data', {
        method: 'POST',
        body: form
    })
        .then(response => response.json())
        .then(json => {
            res.render('admin/verify', { vaccineCard: json.cardb64, idCard: json.idb64, info: json.info, id: req.params.id })
        });
});

router.get('/verify/success/:id', function (req, res, next) {
    const form = new FormData();
    form.append('id', req.params.id);
    form.append('status', 'true');
    fetch('http://localhost:5000/admin/status', {
        method: 'POST',
        body: form
    });
    res.redirect('/admin');
});

router.get('/verify/failure/:id', function (req, res, next) {
    const form = new FormData();
    form.append('id', req.params.id);
    form.append('status', 'false');
    fetch('http://localhost:5000/admin/status', {
        method: 'POST',
        body: form
    });
    res.redirect('/admin');
});

module.exports = router;