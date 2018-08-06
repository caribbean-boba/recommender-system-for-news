const passport = require('passport');
const express = require('express');
const router = express.Router();
const validator = require('validator');

router.post('/signup', (req, res, next) => {
    const result = validateSignup(req.body);
    if (!result.success) {
        console.log('validationResult failed');
        return res.status(400).json({
        success: false,
        message: result.message,
        errors: result.errors
        });
    }

    return passport.authenticate('signup', (err) => {
        if (err) {
        console.log(err);
        if (err.name === 'MongoError' && err.code === 11000) {
            return res.status(409).json({
            success: false,
            message: 'Check the form for errors.',
            errors: {
                email: 'This email is already taken.'
            }
            });
        }

        return res.status(400).json({
            success: false,
            message: 'Could not process the form.'
        });
        }

        return res.status(200).json({
        success: true,
        message: 'You have successfully signed up! Now you should be able to log in.'
        });
    })(req, res, next);
});

router.post('/login', (req, res, next) => {
    const result = validateLogin(req.body);
    if (!result.success) {
        return res.status(400).json({
        success: false,
        message: result.message,
        errors: result.errors
        });
    }

    return passport.authenticate('login', (err, token, userData) => {
        if (err) {
            return res.status(400).json({
                success: false,
                message: 'Login Failed' + err.message
            });
        }
        return res.json({
        success: true,
        token,
        user: userData
        });
    })(req, res, next);
});

function validateSignup(payload) {
    console.log(payload);
    const errors = {};
    let isValid = true;
    let message = '';

    if (!payload || typeof payload.email !== 'string' || !validator.isEmail(payload.email)) {
        isValid = false;
        errors.email = 'Please enter valid email address';
    }
    if (!isValid) {
        message = 'From has error';
    }

    return {
        success: isFormValid,
        message,
        errors
    };
}

function validateLogin(payload) {
    const errors = {};
    let isValid = true;
    let message = '';

    if (!payload || typeof payload.email !== 'string' || payload.email.trim().length === 0) {
        isValid = false;
        errors.email = 'Email Address not Valid. Please Reenter.';
    }

    if (!payload || typeof payload.password !== 'string' || payload.password.trim().length === 0) {
        isValid = false;
        errors.password = 'Password Address not Valid. Please Reenter.';
    }

    if (!isValid) {
        message = 'From has error';
    }

    return {
        success: isValid,
        message,
        errors
    };
}

module.exports = router;