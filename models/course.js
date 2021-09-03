var mongoose = require('mongoose');

var Schema = mongoose.Schema;

var CourseSchema = new Schema({
  code: {
    type: String,
    required: true,
    uppercase: true,
    trim: true,
  },
  name: {
    type: String,
    required: true,
    trim: true,
  },
  link: {
    type: String,
    required: true,
  },
  given: { type: Boolean, required: true },
  teachers: [String],
  teacher_links : [String],
  section: {
    type: String,
    required: true,
    uppercase: true,
    trim: true,
  },
  specializations: [String],
  hours: [Number],
  credits: { type: Number, required: true },
  places: { type: Number },
  semester: { type: String, required: true, enum: ['Fall', 'Spring'] },
  exam_period: {
    type: String,
    required: true,
    enum: ['Semester', 'Period'],
  },
  exam_type: { type: String, enum: ['Written', 'Oral', 'During the semester'] },
  droppable: { type: Boolean },
  group: { type: Number, required: true, enum: [1, 2] },
  year_given: { type: String, trim: true },
  language: { type: String, enum: ['EN', 'FR', 'DE'] },
});

//Export model
module.exports = mongoose.model('Course', CourseSchema);