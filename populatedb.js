#! /usr/bin/env node

// Get arguments passed on command line
var userArgs = process.argv.slice(2);

var async = require('async');
var Course = require('./models/course');

var mongoose = require('mongoose');
var mongoDB = userArgs[0];
mongoose.connect(mongoDB, { useNewUrlParser: true, useUnifiedTopology: true });
mongoose.Promise = global.Promise;
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

var courses = [];

function courseCreate(
  code,
  name,
  given,
  teachers,
  sections,
  specializations,
  lecture_hours,
  exercise_hours,
  practice_hours,
  credits,
  places,
  semester,
  exam_period,
  exam_type,
  droppable,
  group,
  biannual_year,
  cb
) {
  var course = new Course({
    code: code,
    name: name,
    given: given,
    teachers: teachers,
    sections: sections,
    specializations: specializations,
    lecture_hours: lecture_hours,
    exercise_hours: exercise_hours,
    practice_hours: practice_hours,
    credits: credits,
    places: places,
    semester: semester,
    exam_period: exam_period,
    exam_type: exam_type,
    droppable: droppable,
    group: group,
    biannual_year: biannual_year,
  });

  course.save(function (err) {
    if (err) {
      cb(err, null);
      return;
    }
    console.log('New Course: ' + course);
    courses.push(course);
    cb(null, course);
  });
}

function createCourses(cb) {
  async.series(
    [
      function (callback) {
        courseCreate(
          'CS-108',
          'POO',
          true,
          ['Schinz'],
          ['IN'],
          ['A', 'B'],
          4,
          2,
          2,
          9,
          500,
          'S',
          'Period',
          'W',
          true,
          1,
          '',
          callback
        );
      },
      function (callback) {
        courseCreate(
          'MATH-101',
          'AICC',
          true,
          ['Lenstra', 'Kapra'],
          ['SC'],
          ['A', 'D'],
          4,
          2,
          0,
          8,
          700,
          'F',
          'Period',
          'W',
          false,
          1,
          '',
          callback
        );
      },
    ],
    // optional callback
    cb
  );
}

async.series(
  [createCourses],
  // Optional callback
  function (err, results) {
    if (err) {
      console.log('FINAL ERR: ' + err);
    }
    // All done, disconnect from database
    mongoose.connection.close();
  }
);
