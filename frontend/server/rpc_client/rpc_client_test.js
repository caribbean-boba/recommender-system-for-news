var client = require('./rpc_client');

// client.add(1,2,function(response){
//     console.assert(response);
// });

client.getNewsSummariesForUser('test', 1, function(res) {
    console.log(res);
    console.assert(res != null);
})