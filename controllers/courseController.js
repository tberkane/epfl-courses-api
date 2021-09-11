const createError = require('http-errors');
const mongoose = require('mongoose');
const courseTemplate = require('../models/course');

const models = new Map(); // save models here to avoid creating a model for the same section twice

exports.all_courses = async function (req, res, next) {
  if (!models.has(req.params.section)) {
    // create model for section and save it to map if not already created
    models.set(
      req.params.section,
      mongoose.model(
        'courses.' + req.params.section,
        new mongoose.Schema(
          { template: courseTemplate },
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
