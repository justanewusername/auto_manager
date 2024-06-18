import React, {useState} from "react";
import './signup.css';
import axios from "axios";
import config from "../config";
import { useNavigate } from 'react-router-dom';

const SignUp = (props) => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirmPassword: ''
      });
    
      const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
          ...prevState,
          [name]: value
        }));
      };
    
      const handleSubmit = (e) => {
        e.preventDefault();
        const userData = {
          "email": formData.email, 
          "password": formData.password
        };

        console.log('i send: ', userData);

        axios.post(config.apiUrl + "/auth/signup", userData)
        .then(response => {
          console.log("auth done")
          console.log(response.data)
          navigate('/');
        })
        .catch(error => {
          console.error("Error signup:", error);
        });
        console.log(formData);
      };

    return (
      <div className="registration-form">
        <h2>Registration</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="email">Email:</label>
            <input 
              type="email" 
              id="email" 
              name="email" 
              value={formData.email} 
              onChange={handleChange} 
              required 
            />
          </div>
          <div>
            <label htmlFor="password">Password:</label>
            <input 
              type="password" 
              id="password" 
              name="password" 
              value={formData.password} 
              onChange={handleChange} 
              required 
            />
          </div>
          <div>
            <label htmlFor="confirmPassword">Confirm Password:</label>
            <input 
              type="password" 
              id="confirmPassword" 
              name="confirmPassword" 
              value={formData.confirmPassword} 
              onChange={handleChange} 
              required 
            />
          </div>
          <button type="submit">Register</button>
        </form>
      </div>
    );
}

export default SignUp;
