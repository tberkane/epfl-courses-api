var createError = require('http-errors');
const mongoose = require('mongoose');

var template = require('../models/course');

const models = new Map();

exports.all_courses = async function (req, res, next) {
  if (!models.has(req.params.section)) {
    models.set(
      req.params.section,
      mongoose.model(
        'courses.' + req.params.section,
        new mongoose.Schema(
          { template },
          { collection: 'courses.' + req.params.section }
        )
      )
    );
  }

  const courses = await models.get(req.params.section).find();
  if (!courses) {
    return next(createError(404));
  }
  res.send(courses);
};
