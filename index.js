const express = require('express');
const mongoose = require('mongoose');
const requiredir = require('require-dir');

const app = express();
app.use(express.json());

mongoose.connect('mongodb://localhost:27017/billie', { useNewUrlParser: true });
requiredir('./src/models');

app.use(require('./src/routes'));
app.listen(1064);