var express = require('express');
var fetch = require('node-fetch');
var router = express.Router();
var userController = require('../users/users');
var { requiresAuth } = require('express-openid-connect');

var multer = require('multer');
var upload = multer();
var FormData = require('form-data');

router.use(requiresAuth());

/* GET users listing. */
router.get('/new', function (req, res, next) {
    const localUser = userController.getUser(req.oidc.user.name);
    if (localUser.info.hasPass) return res.redirect('/pass/view');
    res.render('new/newPass');
});

router.post('/new/callback', upload.any(), function (req, res, next) {
    const form = new FormData();
    const vaccineCard = req.files.filter(file => file.fieldname === 'vaccine-card')[0];
    const ouId = req.files.filter(file => file.fieldname === 'ou-id')[0];

    form.append('name', req.body.name);
    form.append('email', req.body.email);
    form.append('phone', req.body.phone);
    form.append('month', req.body.month);
    form.append('day', req.body.day);
    form.append('year', req.body.year);
    form.append('vaccine-one-type', req.body['vaccine-one-type']);
    form.append('vaccine-one-date', req.body['vaccine-one-date']);
    form.append('vaccine-two-type', req.body['vaccine-two-type']);
    form.append('vaccine-two-date', req.body['vaccine-two-date']);
    form.append('vaccine-three-type', req.body['vaccine-three-type']);
    form.append('vaccine-three-date', req.body['vaccine-three-date']);
    form.append('vaccine-card', vaccineCard.buffer, {
        contentType: vaccineCard.mimetype,
        name: 'vaccine-card',
        filename: vaccineCard.originalname
    });
    form.append('ou-id', ouId.buffer, {
        contentType: ouId.mimetype,
        name: 'ou-id',
        filename: ouId.originalname
    });

    
    fetch('http://localhost:5000/user/new', {
        method: 'POST',
        body: form
    })
        .then(response => response.text())
        .then(body => {
            const localUser = userController.getUser(req.oidc.user.name);
            localUser.id = body;
            localUser.info.hasPass = true;
            userController.setUser(localUser);
            res.render('new/submitted');
        })
});

router.get('/view', function (req, res, next) {
    const localUser = userController.getUser(req.oidc.user.name);

    const form = new FormData();
    form.append('id', localUser.id);
    
    fetch('http://localhost:5000/user/info', { method: 'POST', body: form })
        .then(response => response.json())
        .then(json => {
            if (json.status === 'PENDING') {
                res.render('pass/pending', { name: json.info.name, phone: json.info.phone });
            } else if (json.status === 'VALID') {
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

                res.render('pass/accepted', { status: status, img: json.qrb64, name: json.info.name, dob: json.info.DOB });
            } else if (json.status === 'INVALID') {
                localUser.info.hasPass = false;
                userController.setUser(localUser);
                res.render('pass/rejected');
            } else {
                // in theory, unreachable state
                res.send('pass not found')
            }
        })
});

module.exports = router;
