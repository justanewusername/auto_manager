import React, {useState} from "react";
import './login.css';
import axios from "axios";
import { useNavigate } from 'react-router-dom';
import config from "../config";
import Cookies from 'js-cookie'

const LogIn = (props) => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
  
    const handleSubmit = (event) => {
      event.preventDefault();
      const userData = {
        "username": email, 
        "password": password
      };

      console.log('i send: ', userData);

      axios.post(config.apiUrl + "/auth/login",
        userData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
      .then(response => {
        console.log("login done:")
        console.log(response.data)
        Cookies.set('token', response.data.access_token, { expires: 30 })
        navigate('/');
      })
      .catch(error => {
        console.error("Error login:", error);
      });
      console.log('Submitted:', email, password);
    };

    return (
        <div className="login-form">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label htmlFor="email">Email</label>
                  <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="password">Password</label>
                  <input
                    type="password"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
              <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default LogIn;
