const User = require('mongoose').model('User');
const jwt = require('jsonwebtoken');
const config = require('../config.json');
module.exports = (req, res, next) => {
    console.log(req.headers);
    if (!req.headers.authorization) {
        return res.status(401).end();
    }
    const token = req.headers.authorization.split(' ')[1];
    console.log('token: ' + token);
    return jwt.verify(token, config.jwtSecret, (err, decoded) => {
        if (err) {
            return res.status(401).end();
        }
        const email = decoded.sub;
        return User.findById(email, (userErr, user) => {
            if (userErr || !user) {
                return res.status(401).end();
            }
            return next();
        });
    });
};