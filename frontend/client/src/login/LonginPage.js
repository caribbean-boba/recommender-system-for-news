import React, {PropTypes} from 'react';
import Authentication from '../auth/Authentication';
import Login from './Login';

class LoginPage extends React.Component {
    constructor(props, context){
        super(props, context);
        this.state = {
            user: {
                email: '',
                password: ''
            },
            errors: {
                summary:''
            }
        }
        this.validateForm = this.validateForm.bind(this);
        this.changeUser = this.changeUser.bind(this);
    }
    changeUser(event) {
        const field = event.target.name;
        const user = this.state.user;
        user[field] = event.target.value;
        this.setState({
          user
    });
}


    validateForm(event) {
        event.preventDefault();
        const email = this.state.user.email;
        const password = this.state.user.password;
        console.log('email:', email);
        console.log('password:', password);

        fetch('http://localhost:3000/auth/login', {
          method: 'POST',
          headers: {
            'cache': false,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: this.state.user.email,
            password: this.state.user.password
          })
        }).then(response => {
            if (response.status === 200) {
                this.setState({
                  errors: {}
                });
                response.json().then(function(json) {
                  console.log(json);
                  Authentication.login(json.token, email);
                  this.context.router.replace('/');
                }.bind(this));
              } else {
                console.log('Login failed');
                response.json().then(function(json) {
                  const errors = json.errors ? json.errors : {};
                  errors.summary = json.message;
                  this.setState({errors});
                }.bind(this));
              }
        });
    }
    render() {
        return (
          <Login
            onSubmit={this.validateForm}
            onChange={this.changeUser}
            errors={this.state.errors}
            user={this.state.user}
    /> );
    }
}

LoginPage.contextTypes = {
    router: PropTypes.object.isRequired
};

export default LoginPage;