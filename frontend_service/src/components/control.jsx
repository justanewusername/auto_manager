import React, { useState, useEffect } from "react";
import axios from "axios";
import './control.css';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import config from "../config.js";
import Cookies from 'js-cookie'

function Control({ changePage, onRefreshClick, setFilter }) {
    const [selectedResourceOption, setSelectedResourceOption] = useState("all");
    const [selectedTypeOption, setSelectedTypeOption] = useState("all");
    const [response, setResponse] = useState(null);
    const [counter, setCounter] = useState(0);

    const resourcesOptions = [
        "all", 
        "scientificamerican", 
        "MIT", 
        "extremetech", 
        'gizmodo', 
        'venturebeat', 
        'synced',
    ];
    const typeOptions = ["all", "AI", "Tech"];

    const handleResourceOptionChange = (event) => {
        setSelectedResourceOption(event.target.value);
    };

    const handleTypeOptionChange = (event) => {
        setSelectedTypeOption(event.target.value);
    };

    const applyFilters = () => {
        setFilter(selectedResourceOption);
    }

    // websockets
    const [messages, setMessages] = useState([]);
  
    useEffect(() => {
        console.log("hello");
        // Create WebSocket connection.
        const socket = new WebSocket(config.apiWS + '/posts/progress/ws');
        socket.onopen = () => {
            console.log("sending message...");
            socket.send(JSON.stringify({ 
                token: Cookies.get('token')
            }));
            console.log("message sended");
        };

        // Connection opened
        socket.addEventListener('open', (event) => {
            console.log('Connected to WebSocket server');
        });
  
        // Listen for messages
        socket.addEventListener('message', (event) => {
            console.log('Message from server ', event.data);
            setMessages([event.data]);
        });

        // Handle connection close
        socket.addEventListener('close', (event) => {
            console.log('WebSocket is closed now.');
            const reconnect = () => {
                setCounter(counter + 1);
            }
            setTimeout(reconnect, 5000);
        });
  
        // Handle errors
        socket.addEventListener('error', (event) => {
            console.error('WebSocket error observed:', event);
        });
    
        // Clean up the socket connection when the component unmounts
        return () => {
            socket.close();
        };
    }, [counter]);


    const postData = async () => {
        try {
          console.log('@@@@@@@@@@@@@@@@@');
          console.log(selectedResourceOption);
          const token = 'Bearer ' + Cookies.get('token');
          console.log(token);
          const response = await axios.post(
            config.apiUrl + '/posts/titles/test',
            {
                resources: [selectedResourceOption],
                urls: [],
                period_days: 10,
            },
            {
                headers: {
                    'Authorization': token
                }
            }
          ).then(response => {
            console.log(response.data);
            setResponse(response.data);
          })
          .catch(error => {
            console.error("Pars error!!!:", error);
          });
          // Set the response in the state
        } catch (error) {
          console.error("Error:", error);
        }
    };

    const onMainPageSet = () => {
        changePage("main");
    };

    const onFavoritesPageSet = () => {
        changePage("favorites");
    };

    const logout = () => {
        Cookies.set('token', '');
    }

    return (
        <div className="control">
            <div className="panel__left">
                <button className="button-primary" onClick={onMainPageSet}>Главная</button>
                <button className="button-primary" onClick={onFavoritesPageSet}>Избранное</button>
                {/* <Link className="link__button" to="/">Главная</Link>
                <Link className="link__button" to="/favorites">Избранное</Link> */}
            </div>


            <div className="panel__center">
                <button className="button-primary" onClick={onRefreshClick} >Обновить</button>
                <div className="panel__list">
                    <p>Выбрать категорию</p>
                    <select value={selectedTypeOption} onChange={handleTypeOptionChange}>
                        {typeOptions.map((option) => (
                            <option key={option} value={option}>
                                {option}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="panel__list">
                    <p>Выбрать ресурс</p>
                    <select value={selectedResourceOption} onChange={handleResourceOptionChange}>
                        {resourcesOptions.map((option) => (
                            <option key={option} value={option}>
                                {option}
                            </option>
                        ))}
                    </select>
                </div>
                <button className="button-primary" onClick={applyFilters}>Применить</button>
                <button className="button-primary" onClick={postData}>Запустить парсер</button>
                <div className="button-login">
                    <Link to="/login">Log In</Link>
                </div>
                <div className="button-signin">
                    <Link to="/signup">Sign In</Link>
                </div>
                <div className="button-logout" onClick={logout}>Log Out</div>
            </div>

            <div className="panel__right">
                <a target="_blank" rel="noreferrer" href={config.apiUrl + '/download/all'}>Скачать файл</a>
            </div>
        </div>
    );
}

export default Control;
