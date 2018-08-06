const mongoose = require('mongoose');

module.exports.connect = (uri) => {
    mongoose.connect('mongodb://yanhan:lyh19970409@ds249415.mlab.com:49415/minileetcode', { useNewUrlParser: true });

    mongoose.connection.on('error', (err) => {
        console.error(`Mongoose connection error: ${err}`);
        process.exit(1);
    });

    require('./user');
};