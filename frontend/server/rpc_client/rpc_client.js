var jayson = require('jayson');

var client = jayson.client.http({
    port: 4040,
    hostname: 'localhost'
});

function add(a, b, callback) {
    client.request('add', [a, b], function(err, error, response) {
        if (err) throw err;
        callback(response);
    });
}

function getNewsSummariesForUser(user_id, page, cb){
    client.request('getNewsSummariesForUser', [user_id, page], function (err, error, res){
        if (err) throw err;
        // console.log(user_id)
        // console.log(page)
        console.log(res);
        cb(res);
    });
}

module.exports = {
    add: add,
    getNewsSummariesForUser: getNewsSummariesForUser
}