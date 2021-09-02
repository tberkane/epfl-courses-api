var createError = require('http-errors');

var Course = require('../models/course');

exports.all_courses = async function (req, res) {
  const courses = await Course.find();
  res.send(courses);
};

exports.single_course = async function (req, res, next) {
  const course = await Course.findOne({
    code: req.params.courseCode,
  });
  if (!course) {
    return next(createError(404));
  }
  res.send(course);
};
