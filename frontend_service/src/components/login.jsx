import React, {useState} from "react";
import './login.css';
import { useNavigate } from 'react-router-dom';
import { login } from "../api";

const LogIn = (props) => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
  
    const handleSubmit = async (event) => {
      event.preventDefault();
      const userData = {
        "username": email, 
        "password": password
      };

      console.log('i send: ', userData);

      await login(userData).then(result => {
        props.changeToken();
        navigate('/');
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
