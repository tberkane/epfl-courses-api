var express = require('express');
var router = express.Router();

var course_controller = require('../controllers/courseController');

router.get('/', course_controller.all_courses);
router.get('/:courseCode', course_controller.single_course);
module.exports = router;
