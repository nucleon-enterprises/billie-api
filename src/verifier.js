const mongoose = require('mongoose');
const cModules = mongoose.model('cModules'); // client modules
const aModules = mongoose.model('aModules'); // action modules
const axios = require('axios');

const info = require('./info.json');
const allowedCommandTypes = info.allowedCommandTypes;

module.exports = (req, res) => {

    const logIt = (text) => {
        console.log("response: \n".concat(text));
        res.send(text);
    }

    let accessToken = req.body.accessToken;
    let clientModule = cModules.findOne({ accessToken }).name;
    if (!accessToken || !clientModule) {
        logIt("wrong credentials");
    } else {
        let command = req.body.command;
        let type = req.body.type;
        if (!command || !type) {
            logIt("missing parameters");
        } else if (!allowedCommandTypes.includes(type)) {
            logIt("type isn't allowed");
        } else if (type == 'pure') {
            let moduleName = command.module;
            let func = command.func;
            let args = command.args;
            let chosenModule = aModules.findOne({ name: moduleName });
            if (!chosenModule.name) {
                logIt("module doesn't exist");
            } else {
                let modulePort = chosenModule.port;
                let accessToken = chosenModule.accessToken;
                let address = chosenModule.address;
                let query = { accessToken, command: { func, args }};
                axios.post(`${address}:${modulePort}`, query)
                .then((response) => {
                    logIt(JSON.stringify(response, null, 4));
                });
            }
        } else {
            logIt("Billie for now only receive pure commands");
        }
    }
};