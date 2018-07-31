import React, { Component } from 'react';
import logo from '../logo.png';
import './App.css';

import 'materialize-css/dist/css/materialize.min.css';
import 'materialize-css/dist/js/materialize.min.js';

import Panel from './Panel/Panel'
class App extends Component {
  render() {
    return (
     <div>
       <img className = 'App-logo' src = {logo} alt = 'logo'/>
       <div className = 'container'>
        <Panel> </Panel>
       </div>
     </div>
    );
  }
}

export default App;
