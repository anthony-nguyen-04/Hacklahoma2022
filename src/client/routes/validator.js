var express = require('express');
var router = express.Router();
var fetch = require('node-fetch');
var userController = require('../users/users');
var FormData = require('form-data');
var { requiresAuth } = require('express-openid-connect');

router.use(requiresAuth());

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('validator/scan');
});

router.post('/submit', function (req, res, next) {
    let image = req.body.data;
    image = image.split('data:image/png;base64,')[1]
    const form = new FormData();
    form.append('data', image)
    fetch('http://localhost:5000/validator/code', {
        method: 'POST',
        body: form
    })
        .then(response => response.text())
        .then(body => {
            res.redirect('/validator/submit/success/' + body);
        })
});

router.get('/submit/success/:id', function (req, res, next) {
    const id = req.params.id;
    const form = new FormData()
    form.append('id', id);
    fetch('http://localhost:5000/user/info', {
        method: 'POST',
        body: form
    }).then(response => response.json())
    .then(json => {
        let status;

        if (json.info['vaccine-three-type'] !== 'none') {
            status = 'boosted';
        } else if (json.info['vaccine-two-type'] !== 'none') {
            dateArr = json.info['vaccine-two-date'].split('/');
            const lastDate = new Date(dateArr[2] + '-' + dateArr[0] + '-' + dateArr[1]);
            const currentDate = new Date();
            const daysDifference = Math.ceil((currentDate - lastDate) / (1000 * 60 * 60 * 24));
            if (daysDifference >= 14) status = 'full';
            else status = 'partial';
        } else if (json.info['vaccine-one-type'] !== 'none') {
            status = 'partial';
        } else {
            status = 'none';
        }
        res.render('validator/results', { name: json.info.name, dob: json.info.DOB, status: status });
    })
})

module.exports = router;
