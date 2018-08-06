import React, { PropTypes } from 'react';
import {Link} from 'react-router';
import Authentication from '../auth/Authentication';
import './Container.css';

const Container = ({ children }) => (
    <div className = "container-fluid">
       <nav className="nav-bar navbar-default">
            <div className="nav-wrapper">
                <a href="/" className="brand-logo center">Yanhan's Recommender System for News</a>
                <ul id="nav-mobile" className="right">
                    {Authentication.isAuthenticated() ?
                        (<div>
                        <li>{Authentication.getEmail()}</li>
                        <li><Link to="/logout">Log out</Link></li>
                        </div>)
                        :
                        (<div>
                        <li><Link to="/login">Log in</Link></li>
                        <li><Link to="/signup">Sign up</Link></li>
                        </div>)
                    }
                    </ul>
                </div>
            </nav>
        <br/>
       {children}
    </div>
);
Container.propTypes = {
    children: PropTypes.object.isRequired
};



export default Container;