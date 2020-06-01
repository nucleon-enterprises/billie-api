const express = require('express');

const routes = express.Router();
const billieRoutes = express.Router();

const billieController = require('./controllers/billieController');

const authMiddleware = require('./middlewares/auth');

billieRoutes.use(authMiddleware);
billieRoutes.get('/show', billieController.show);

routes.use('/billie', billieRoutes);



module.exports = routes;