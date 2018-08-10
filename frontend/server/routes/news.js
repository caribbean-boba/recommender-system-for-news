// var express = require('express');
// var router = express.Router();

// /* GET users listing. */
// router.get('/', function(req, res, next) {
//   const news =  [
//     {'url':'http://us.cnn.com/2017/02/15/politics/andrew-puzder-failed-nomination/index.html',
//      'title':"Inside Andrew Puzder's failed nomination",
//      'description':"In the end, Andrew Puzder had too much baggage -- both personal and professional -- to be confirmed as President Donald Trump's Cabinet.",
//      'source':'cnn',
//      'urlToImage':'http://i2.cdn.cnn.com/cnnnext/dam/assets/170215162504-puzder-trump-file-super-tease.jpg',
//      'digest':'1',
//      'reason':'Recommend'
//     },
//     {'title': 'Zero Motorcycles CTO Abe Askenazi on the future of two-wheeled EVs',
//      'description': "Electric cars and buses have already begun to take over the world, but the motorcycle industry has been much slower to put out all-electric and hybrid models...",
//      'url': "https://techcrunch.com/2017/03/23/zero-motorcycles-cto-abe-askenazi-on-the-future-of-two-wheeled-evs/",
//      'urlToImage': "https://tctechcrunch2011.files.wordpress.com/2017/03/screen-shot-2017-03-23-at-14-04-01.png?w=764&h=400&crop=1",
//      'source': 'techcrunch',
//      'digest':"2",
//      'time':"Today",
//      'reason':"Hot"
//    },
//    {'title': "Facebook security chief rants about misguided “algorithm” backlash",
//     'description': "\"I am seeing a ton of coverage of our recent issues driven by stereotypes of our employees and attacks against fantasy, strawman tech cos\" wrote Facebook..",
//     'url': "https://techcrunch.com/2017/10/07/alex-stamos/",
//     'urlToImage': "https://tctechcrunch2011.files.wordpress.com/2017/10/facebook-alex-stamos.png",
//     'source': 'techcrunch',
//     'digest':"3RjuEomJo26O1ZbUdOHA==\n",
//     'reason': 'Today'
//    },
//    {"title": "Benchmarks contradict ‘Apple slowed down my iPhone’ claims",
//     "description": "It's a refrain we all hear every year around September: \"I swear, whenever they release a new iPhone, Apple makes all the old ones run worse to make you..",
//     "url": "https://techcrunch.com/2017/10/06/benchmarks-contradict-apple-slowed-down-my-iphone-claims/",
//     "urlToImage": "https://tctechcrunch2011.files.wordpress.com/2017/06/2014-iphone-6-gettyimages-455672728.jpg",
//     'source': 'techcrunch',
//     'digest':"3RjuJo26O1ZbUdOHA==\n",
//     'reason':"Hot"
//    },
//    {"title": "Square Enix Brings Manga to VR - IGN Access - IGN Video",
//     "description": "Reading isn't something we're used to doing in virtual reality, but it might be soon.",
//     "url": "http://ca.ign.com/videos/2017/10/07/square-enix-brings-manga-to-vr-ign-access",
//     "urlToImage": "https://assets1.ignimgs.com/thumbs/userUploaded/2017/10/7/maxresdefault-1507410780676_1280w.jpg",
//     'source': 'ign',
//     'digest':"3RjuJo26O1ZA==\n",
//     'reason':'Recommend'
//    }
//  ];
//   res.json(news);
// });

// module.exports = router;


var express = require('express');
var rpc_client = require('../rpc_client/rpc_client');
var router = express.Router();

/* GET users listing. */
router.get('/userId/:userId/page/:page', function(req, res, next) {
  console.log('reach here!!');
  user_id = req.params['userId'];
  page_num = req.params['page'];

  rpc_client.getNewsSummariesForUser(user_id, page_num, function(response) {
    console.log('response');
    console.log(response)
    res.json(response);
  });
});

router.post('/userId/:userId/newsId/:newsId', function(req, res, next) {
  console.log('reach here log!!!!');
  user_id = req.params['userId'];
  news_id = req.params['newsId'];
  console.log(news_id);

  rpc_client.recordClickLogForUser(user_id, news_id);
  res.json('success');
});


module.exports = router;

