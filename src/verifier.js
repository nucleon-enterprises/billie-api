const mongoose = require('mongoose');
const cModules = mongoose.model('cModules');
const aModules = mongoose.model('aModules');
const axios = require('axios');

const info = require('./info.json');
const allowedCommandTypes = info.allowedCommandTypes;

module.exports = (req, res) => {
    let accessToken = req.body.accessToken;
    let moduleTryingToAccess = cModules.findOne({ accessToken }).name;
    if (!accessToken || !moduleTryingToAccess) {
        let responseText = "wrong credentials";
        console.log("response: \n".concat(responseText));
        res.send(responseText);
    } else {
        let command = req.body.command;
        let type = req.body.type;
        if (!command || !type) {
            let responseText = "missing parameters";
            console.log("response: \n".concat(responseText));
            res.send(responseText);
        } else if (!allowedCommandTypes.includes(type)) {
            let responseText = "type isn't allowed";
            console.log("response: \n".concat(responseText));
            res.send(responseText);
        } else if (type == 'pure') {
            let moduleName = command.module;
            let func = command.func;
            let args = command.args;
            let chosenModule = aModules.findOne({ name: moduleName });
            if (!chosenModule.name) {
                let responseText = "module doesn't exist";
                console.log("response: \n".concat(responseText));
                res.send(responseText);
            } else {
                let modulePort = chosenModule.port;
                let accessToken = chosenModule.accessToken;
                let query = { accessToken, command: { func, args }};
                axios.post('localhost:'.concat(modulePort), query)
                .then(function (response) {
                    let responseText = JSON.stringify(response, null, 4);
                    console.log("response: \n".concat(responseText));
                    res.send(responseText);
                });
            }
        } else {
            let responseText = "Billie for now only receive pure commands";
            console.log("response: \n".concat(responseText));
            res.send(responseText);
        }
    }
};