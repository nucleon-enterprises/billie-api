const mongoose = require('mongoose');

const BillieSchema = new mongoose.Schema({
    ownerId: {
        type: String,
        required: true,
    },
    name: {
        type: String,
        default: "Billie",
    },
}, {timestamps: true});

mongoose.model('Billie', BillieSchema);