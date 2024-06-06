import './palette.css';
import './App.css';
import Control from './components/control';
import Favorites from './components/favorites';
import PostsContainer from './components/postsContainer';
import React, { useState, useRef, useCallback } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import NotFound from './components/notFound';
import SignUp from './components/signup';
import LogIn from './components/login';
import config from './config,js';



function App() {
  const postContainerRef = useRef(null);
  const [postContainerUrl, setPostContainerUrl] = useState(config.apiUrl + "/all");
  const [resourcefilter, setResourcefilter] =  useState("all");



  const refresh = useCallback(() => {
    postContainerRef.current.getPosts();
  }, []);

  const setFilter = (filter) => {
    setResourcefilter(filter);
  }

  const changePage = (currentPage) => {
    if(currentPage === "main") {
      setPostContainerUrl(config.apiUrl + "/all")
    } else {
      setPostContainerUrl(config.apiUrl + "/favorites")
    }
  };

  return (
    <div className="App">
      <Control changePage={changePage} onRefreshClick={refresh} setFilter={setFilter}/>
      <Routes>
        <Route exact path="/" element={<PostsContainer url={postContainerUrl} filter ={resourcefilter} ref={postContainerRef}/>} />
        <Route exact path="/signup" element={<SignUp/>} />
        <Route exact path="/login" element={<LogIn/>} />
        <Route component={NotFound} />

                
      </Routes>
    </div>
  );
}

export default App;
