const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const UserSchema = new mongoose.Schema({
    email: {
        type: String, index: { unique: true }
    },
    password: String
});

UserSchema.methods.compare = function compare(password, cb) {
    bcrypt.compare(password, this.password, cb);
};

UserSchema.pre('save', function savePre(next) {
    const user = this;
    console.log('save');
        // if not modified, do nothing
    if (!user.isModified('password')){
        return next();
    };
    return bcrypt.genSalt((error, salt) => {
        if (error) {
            return next(error);
        } else {
            return bcrypt.hash(user.password, salt, (hashError, hash) => {
                if (hashError) {
                    return next(hashError);
                }
                user.password = hash;
                return next();
            });
        };
    });
});

module.exports = mongoose.model('User', UserSchema);
