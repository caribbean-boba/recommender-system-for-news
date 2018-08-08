import React, {PropTypes} from 'react';
import './Login.css';
import { Link } from 'react-router'
const Login = ({
  onSubmit,
  onChange,
  errors,
  user,
}) => (
  <div className="container">
    <div className="card-panel login-panel">
      <form className="col s12" action="/" onSubmit={onSubmit}>
        <h4 className="center-align">Login</h4>
        {errors.summary && <div className="row"><p className="error-message">{errors.summary}</p></div>}
        <div className="row">
          <div className="input-field col s12">
            <input className="validate" id="email" type="email" name="email" onChange={onChange}/>
            <label htmlFor='email'>Email</label>
          </div>
        </div>
        {errors.email && <div className="row"><p className="error-message">{errors.email}</p></div>}
        <div className="row">
          <div className="input-field col s12">
            <input className="validate" id="password" type="password" name="password" onChange={onChange}/>
            <label htmlFor='password'>Password</label>
          </div>
</div>
        {errors.password && <div className="row"><p className="error-message">{errors.password}</p></div>}
        <div className="row center-align">
          <input type="submit" className="btn btn-primary" value='Log in'/>
        </div>
        <div className="row center-align">
          <p className="right-align"> Not have account yet?  <Link to="/signup">Sign Up</Link></p>
        </div>
      </form>
    </div>
</div> );


Login.propTypes = {
    onSubmit: PropTypes.func.isRequired,
    onChange: PropTypes.func.isRequired,
     errors: PropTypes.object.isRequired,
     user: PropTypes.object.isRequired
};
export default Login;