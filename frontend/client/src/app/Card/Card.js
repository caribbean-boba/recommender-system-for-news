import './Card.css'
import Auth from '../../auth/Authentication'

import React from 'react';

class Card extends React.Component{
    sendClick() {
        // console.log('I clicked here');
        // let url = 'http://localhost:3000/news/userId/' + Auth.getEmail() + "/newsId/" + this.props.news.digest;
        // console.log(url);
        let url = `http://localhost:3000/news/userId/${Auth.getEmail()}'/newsId/${this.props.news.digest}`;

    let request = new Request(url, {
      method: 'POST',
      headers: {
        'Authorization': 'bearer ' + Auth.getToken(),
        'cache': false
      },
    });

    console.log(this.props.news.digest)
    console.log(this.props.news.title)
    console.log(url)

    console.log('bearer ' + Auth.getToken());

    fetch(request).then(data => console.log(data));
    }
    render() {
        return (
            <div className='news-container' onClick={() =>  {
                    window.open(this.props.news.url, '_blank')
                    this.sendClick()
                } }>
            <div className='row'>
                <div className='col s4 fill'>
                    <img src={this.props.news.urlToImage} alt='news' />
                </div>
                <div className="col s8">
                    <div className="news-intro-col">
                        <div className="news-intro-panel">
                            <h4>{this.props.news.title}</h4>
                            <div className="news-description">
                                <p>{this.props.news.description}</p>
                                <div>
                                    {this.props.news.source != null && <div className='chip light-blue news-chip'>{this.props.news.source.name}</div>}
                                    {this.props.news.reason != null && <div className='chip light-green news-chip'>{this.props.news.reason}</div>}
                                    {this.props.news.time != null && <div className='chip light-yellow news-chip'>{this.props.news.time}</div>}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        )

    }
}

export default Card;