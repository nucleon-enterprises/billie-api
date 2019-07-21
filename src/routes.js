const express = require('express');
const router = express.Router();
const verifier = require('./verifier');

router.use((req, res, next) => {
    console.log("Someone trying to make connection: ".concat(req.ip));
    console.log("Body request:\n".concat(JSON.stringify(req.body, null, 4)));
    next();
});

router.post('/command', verifier);

module.exports = router;