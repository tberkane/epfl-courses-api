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
  teachers: [String],
  teacher_links: [String],
  section: {
    type: String,
    required: true,
    uppercase: true,
    trim: true,
  },
  specializations: [String],
  hours: [Number],
  credits: { type: Number, required: true },
  semester: { type: String, required: true, enum: ['Fall', 'Spring'] },
  exam_type: { type: String, enum: ['Written', 'Oral', 'Semester'] },
  group: { type: String, required: true },
  language: { type: String, enum: ['EN', 'FR', 'DE'] },
  remark: {
    type: String,
    trim: true,
  },
});

//Export model
module.exports = mongoose.model('Course', CourseSchema);
