import Container from './container/Container';
import App from './app/App';
import LoginPage from './login/LonginPage';
import SignupPage from './signup/SignupPage';
import Authentication from './/auth/Authentication';
const routes = {
  component: Container,
  childRoutes: [
    {
        path: '/',
        getComponent: (location, callback) => {
            if (Authentication.isAuthenticated()) {
                callback(null, App);
            } else {
                callback(null, SignupPage);
            }
        }
    },
    {
        path: '/login',
        component: LoginPage
    },
    {
        path: '/signup',
        component: SignupPage
    },
    {
        path: '/logout',
        onEnter: (nextState, replace) => {
            Authentication.logout();
            // change the current URL to /
            replace('/');
        }
    }]
}

export default routes;
