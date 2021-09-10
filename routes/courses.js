var express = require('express');
var router = express.Router();

var course_controller = require('../controllers/courseController');

router.get('/:section', course_controller.all_courses);

module.exports = router;
