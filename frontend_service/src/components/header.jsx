import React, { useState, useEffect } from "react";
import './header.css';
import { Link, useLocation, useNavigate } from "react-router-dom";
import config from "../config.js";
import Cookies from 'js-cookie'
import usePostStore from "../postStore.js";
import { logout, runTitleParser } from "../api.js";



function Header({ changeCurrentPage, onRefreshClick, setFilter, token }) {
    const navigate = useNavigate();
    const location = useLocation();
    const [selectedResourceOption, setSelectedResourceOption] = useState("all");
    const [selectedTypeOption, setSelectedTypeOption] = useState("all");
    const [response, setResponse] = useState(null);
    const [counter, setCounter] = useState(0);
    const setPost = usePostStore((state) => state.setPost);
    const [JWTToken, setJWTToken] = useState(token);
    const [currentPage, setCurrentPage] = useState('articles');

    useEffect(() => {
        setJWTToken(token);
    }, [token]);

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

    const changePage = (page) => {
        changeCurrentPage(page);
        setCurrentPage(page);

        if (location.pathname !== '/') {
            navigate('/');
        }
    };

    const doLogout = () => {
        logout();
        setJWTToken('');
    }

    return (
        <div className="control">
            <div className="panel__center">
                <div className="navigation-section">
                    <button className={`primary-btn ${currentPage === 'articles' ? 'primary-btn__selected' : ''}`}
                            onClick={() => changePage('articles')}>articles</button>
                    <button className={`primary-btn ${currentPage === 'savedSummary' ? 'primary-btn__selected' : ''}`}
                            onClick={() => changePage('savedSummary')}>saved summary</button>
                    <button className={`primary-btn ${currentPage === 'answers' ? 'primary-btn__selected' : ''}`}
                            onClick={() => changePage('answers')}>answers</button>
                    <button className={`primary-btn ${currentPage === 'savedPosts' ? 'primary-btn__selected' : ''}`}
                            onClick={() => changePage('savedPosts')}>saved posts</button>
                </div>

                <div className="login-section">
                    {JWTToken === '' ? (
                        <>
                            <div className="button-login">
                                <Link to="/login">Log In</Link>
                            </div>
                            <div className="button-signin">
                                <Link to="/signup">Sign In</Link>
                            </div>
                        </>
                    ) : (
                        <div className="button-logout" onClick={doLogout}>Log Out</div>                    
                    )}
                </div>

            </div>

            {/* <div className="panel__right">
                <a target="_blank" rel="noreferrer" href={config.apiUrl + '/download/all'}>Скачать файл</a>
            </div> */}
        </div>
    );
}

export default Header;
