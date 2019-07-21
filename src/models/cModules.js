const mongoose = require('mongoose');

function getInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
}

const cModulesSchema = new mongoose.Schema({
    name: String,
    authCode: {
        type: Number,
        default: getInt(1000, 9999)
    },
    accessToken: String,
    connectedAt: {
        type: Date,
        default: Date.now
    }
});

mongoose.model('cModules', cModulesSchema);