class Authentication {

    static login(token, email) {
      localStorage.setItem('email', email);
      localStorage.setItem('token', token);
  }

    static isAuthenticated() {
      return localStorage.getItem('token') !== null;
  }

    static logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('email');
  }

    static getToken() {
      return localStorage.getItem('token');
  }

     static getEmail() {
       return localStorage.getItem('email');
    }
}

export default Authentication;