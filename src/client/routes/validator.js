var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('validator/scan');
});

router.post('/submit', function (req, res, next) {
  res.send(req.body.data)
})

module.exports = router;
