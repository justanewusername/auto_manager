import React, {useState} from "react";
import './signup.css';
import { useNavigate } from 'react-router-dom';
import { register } from "../api";

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
    
      const handleSubmit = async (e) => {
        e.preventDefault();
        const userData = {
          "email": formData.email, 
          "password": formData.password
        };

        console.log('i send: ', userData);
        
        await register(userData)
          .then(
            (result) => {
              console.log("auth done")
              console.log(result)
              navigate('/');
          })
          .catch(error => console.log(error))
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
