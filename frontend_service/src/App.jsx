import './variables.css';
import './palette.css';
import './App.css';
import Control from './components/header.jsx';
import Favorites from './components/favorites';
import PostsContainer from './components/postsContainer';
import React, { useState, useRef, useCallback } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NotFound from './components/notFound';
import SignUp from './components/signup';
import LogIn from './components/login';
import config from './config.js';
import Cookies from 'js-cookie'
import Filters from './components/filters.jsx';


function App() {
  const postContainerRef = useRef(null);
  const [postContainerUrl, setPostContainerUrl] = useState(config.apiUrl + "/posts/titles");
  const [resourcefilter, setResourcefilter] =  useState("all");
  const [token, setToken] = useState(Cookies.get('token'));
  const [currentPage, setCurrentPage] = useState('articles');


  const refresh = useCallback(() => {
    postContainerRef.current.getPosts();
  }, []);

  const setFilter = (filter) => {
    setResourcefilter(filter);
  }

  // const changePage = (currentPage) => {
  //   if(currentPage === "main") {
  //     setPostContainerUrl(config.apiUrl + "/all")
  //   } else {
  //     setPostContainerUrl(config.apiUrl + "/favorites")
  //   }
  // };

  const changeToken = () => {
    setToken(Cookies.get('token'));
  }

  const changeCurrentPage = (page) => {
    setCurrentPage(page);
  }

  const articlesPage = (<>
    <Filters/>
    <PostsContainer url={postContainerUrl} filter ={resourcefilter} ref={postContainerRef}/>
  </>)

  return (
    <div className="App">
      <Control onRefreshClick={refresh} 
               setFilter={setFilter} 
               token={token}
               changeCurrentPage={changeCurrentPage}/>
      <Routes>
        <Route exact path="/" element={articlesPage} />
        <Route exact path="/signup" element={<SignUp changeToken={changeToken}/>} />
        <Route exact path="/login" element={<LogIn changeToken={changeToken}/>} />
        <Route component={NotFound} />
      </Routes>
    </div>
  );
}

export default App;
