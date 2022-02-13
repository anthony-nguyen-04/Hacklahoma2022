var express = require('express');
var fetch = require('node-fetch');
var router = express.Router();
var userController = require('../users/users');
var { requiresAuth } = require('express-openid-connect');

router.use(requiresAuth());

/* GET users listing. */
router.get('/new', function (req, res, next) {
    const localUser = userController.getUser(req.oidc.user.name);
    if (localUser.info.hasPass) return res.redirect('/pass/view');
    res.render('newPass');
});

router.post('/new/callback', function (req, res, next) {

});

router.get('/view', function (req, res, next) {
    const localUser = userController.getUser(req.oidc.user.name);

    fetch('/api/user/status', { method: 'POST', body: 'id=' + localUser.id })
        .then(response => response.text())
        .then(body => {
            if (body === 'pending') {
                fetch('/api/user/info', { method: 'POST', body: 'id=' + localUser.id })
                    .then(nextRes => nextRes.json())
                    .then(json => {
                        res.render('pass/pending', { name: json.name, phone: json.phone });
                    })
            } else if (body === 'accepted') {
                fetch('/api/user/info', { method: 'POST', body: 'id=' + localUser.id })
                    .then(nextRes => nextRes.json())
                    .then(json => {
                        fetch('/api/user/code', { method: 'POST', body: 'id=' + localUser.id })
                            .then(nextNextRes => nextNextRes.text())
                            .then(nextBody => {
                                let status;

                                if (json['vaccine-three-type'] !== 'none') {
                                    status = 'boosted';
                                } else if (json['vaccine-two-type'] !== 'none') {
                                    dateArr = json['vaccine-two-date'].split('/');
                                    const lastDate = new Date(dateArr[2] + '-' + dateArr[0] + '-' + dateArr[1]);
                                    const currentDate = new Date();
                                    const daysDifference = Math.ceil((currentDate - lastDate) / (1000 * 60 * 60 * 24));
                                    if (daysDifference >= 14) status = 'full';
                                    else status = 'partial';
                                } else if (json['vaccine-one-type'] !== 'none') {
                                    status = 'partial';
                                } else {
                                    status = 'none';
                                }

                                res.render('pass/accepted', { status: status, img: nextBody, name: json.name, dob: json.DOB });
                            })
                    })
            } else if (body === 'rejected') {
                localUser.info.hasPass = false;
                userController.setUser(localUser);
                res.render('pass/rejected');
            }
        })
});

module.exports = router;
