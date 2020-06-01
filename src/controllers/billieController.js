const mongoose = require('mongoose');
const Billie = mongoose.model('Billie');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const authConfig = require('../config/auth.json');

module.exports = {
    async show(req, res) {
        const billies = await Billie.find();
        return res.json(billies);
    }
}