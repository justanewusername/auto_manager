import React, { useState, useEffect } from "react";
import './control.css';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import config from "../config.js";
import Cookies from 'js-cookie'
import usePostStore from "../postStore.js";
import { logout, runTitleParser } from "../api.js";

function Control({ changePage, onRefreshClick, setFilter }) {
    const [selectedResourceOption, setSelectedResourceOption] = useState("all");
    const [selectedTypeOption, setSelectedTypeOption] = useState("all");
    const [response, setResponse] = useState(null);
    const [counter, setCounter] = useState(0);
    const setPost = usePostStore((state) => state.setPost);

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
  
    useEffect(() => {
        // Create WebSocket connection.
        let socket;
        try {
            socket = new WebSocket(config.apiWS + '/posts/progress/ws');

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
                const recivedData = JSON.parse(event.data);
                console.log('****: ', recivedData.type);
                console.log('*******: ', recivedData['type']);
                console.log(typeof recivedData)
                console.log('Message from server: ', recivedData);
                if(recivedData.type === 'post') {
                    console.log("jajajajaja")
                    setPost(recivedData['message']);
                }
                else {
                    console.log("chochochocho")
                }
            });
    
            // Handle connection close
            socket.addEventListener('close', (event) => {
                console.log('WebSocket is closed now.');
                const reconnect = () => {
                    setCounter(counter + 1);
                }
                setTimeout(reconnect, 4000);
            });
      
            // Handle errors
            socket.addEventListener('error', (event) => {
                console.error('WebSocket error observed:', event);
            });
        } catch {
            const reconnect = () => {
                setCounter(counter + 1);
            }
            setTimeout(reconnect, 2000);
            return;
        }

    
        // Clean up the socket connection when the component unmounts
        return () => {
            console.log('ttttt ', socket);
            socket.close();
        };
    }, [counter]);


    const postData = async () => {
        runTitleParser(selectedResourceOption)
            .then(result => setResponse(response.data));
    };

    const onMainPageSet = () => {
        changePage("main");
    };

    const onFavoritesPageSet = () => {
        changePage("favorites");
    };

    const doLogout = () => {
        logout();
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
                <div className="button-logout" onClick={doLogout}>Log Out</div>
            </div>

            <div className="panel__right">
                <a target="_blank" rel="noreferrer" href={config.apiUrl + '/download/all'}>Скачать файл</a>
            </div>
        </div>
    );
}

export default Control;
