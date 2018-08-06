import './Panel.css'
import Auth from '../../auth/Authentication';
import React from 'react'
import Card from '../Card/Card'
import _ from 'lodash'
const BUFFER = 60;


// const test =  [
//     {'url':'http://us.cnn.com/2017/02/15/politics/andrew-puzder-failed-nomination/index.html',
//      'title':"Inside Andrew Puzder's failed nomination",
//      'description':"In the end, Andrew Puzder had too much baggage -- both personal and professional -- to be confirmed as President Donald Trump's Cabinet.",
//      'source':'cnn',
//      'urlToImage':'http://i2.cdn.cnn.com/cnnnext/dam/assets/170215162504-puzder-trump-file-super-tease.jpg',
//      'digest':'3RjuEomJo26O1syZbU7OHA==\n',
//      'reason':'Recommend'
//     },
//     {'title': 'Zero Motorcycles CTO Abe Askenazi on the future of two-wheeled EVs',
//      'description': "Electric cars and buses have already begun to take over the world, but the motorcycle industry has been much slower to put out all-electric and hybrid models...",
//      'url': "https://techcrunch.com/2017/03/23/zero-motorcycles-cto-abe-askenazi-on-the-future-of-two-wheeled-evs/",
//      'urlToImage': "https://tctechcrunch2011.files.wordpress.com/2017/03/screen-shot-2017-03-23-at-14-04-01.png?w=764&h=400&crop=1",
//      'source': 'techcrunch',
//      'digest':"3RjuEomJo26O1syZbUdOHA==\n",
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

class Panel extends React.Component{
    constructor(){
        super();
        this.state = {
            availableNews: null
        };
        console.log('hi');
        this.scrollHandler = this.scrollHandler.bind(this);
    };

    componentDidMount() {
        console.log('hi');
        this.loadNews();
        this.loadNews = _.debounce(this.loadNews, 500);
        console.log(this.state.availableNews);
        window.addEventListener('scroll', this.scrollHandler);
    };

    loadNews(e) {
        let request = new Request('http://localhost:3000/news', {
            method: 'GET',
            headers:{
                'cache': false,
                'Authorization': 'bearer '+ Auth.getToken()
            },
        });

        fetch(request).then(res => res.json()).then(news => {
            this.setState({
                availableNews: this.state.availableNews ? this.state.availableNews.concat(news): news,
            });
        });
    }
    scrollHandler(){
        var y = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
        if (window.innerHeight + y > document.body.offsetHeight - BUFFER){
            this.loadNews();
        }

    }

    renderNews() {
        let newsList = this.state.availableNews.map(function(news) {
            return (
                <a className='list-group-item' key={news.digest} href='#'>
                    <Card news={news}/>
                </a>
            );
        });
        return (
            <div className = "container-fluid">
                <div className = 'list-group'>
                    {newsList}
                </div>
            </div>
        );
    };

    render() {
        if (this.state.availableNews) {
            return (
                <div>
                    {this.renderNews()}
                </div>
            );
        } else {
            return (
                <div>
                    Loading
                </div>
            );
        }

    }
}

export default Panel;