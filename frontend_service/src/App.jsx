import './variables.css';
import './palette.css';
import './App.css';
import Control from './components/header.jsx';
import Favorites from './components/favorites';
import PostsContainer from './components/postsContainer';
import React, { useState, useRef, useCallback, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NotFound from './components/notFound';
import SignUp from './components/signup';
import LogIn from './components/login';
import config from './config.js';
import Cookies from 'js-cookie'
import Filters from './components/filters.jsx';
import AnswersContainer from './components/answersContainer.jsx';


function App() {
  const postContainerRef = useRef(null);
  const [postContainerUrl, setPostContainerUrl] = useState(config.apiUrl + "/posts/titles");
  const [resourcefilter, setResourcefilter] =  useState("all");
  const [token, setToken] = useState(Cookies.get('token'));
  const [currentPage, setCurrentPage] = useState('articles');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [resourceFilter, setResourceFilter] = useState('all');

  const changeResource = (resourse) => {
    setResourceFilter(resourse);
  };

  const changeCategorie = (category) => {
    setCategoryFilter(category);
  }

  const articlesPage = (<>
    <Filters changeResource={changeResource} changeCategorie={changeCategorie}/>
    <PostsContainer categoryFilter={categoryFilter} resourceFilter={resourceFilter} url={postContainerUrl} filter ={resourcefilter} ref={postContainerRef}/>
  </>)

  const answersPage = (<AnswersContainer/>);


  const [currentElment, setCurrentElement] = useState(articlesPage);



  const refresh = useCallback(() => {
    postContainerRef.current.getPosts();
  }, []);

  const setFilter = (filter) => {
    setResourcefilter(filter);
  }

  const changeToken = () => {
    setToken(Cookies.get('token'));
  }

  const changeCurrentPage = (page) => {
    setCurrentPage(page);
  }

  useEffect(() => {
    console.log("2234556666");
    console.log(currentPage);
    if(currentPage === 'articles') {
      setCurrentElement(articlesPage);
    } else if (currentPage === 'answers') {
      setCurrentElement(answersPage);
    }
  }, [currentPage]);


  return (
    <div className="App">
      <Control onRefreshClick={refresh} 
               setFilter={setFilter} 
               token={token}
               changeCurrentPage={changeCurrentPage}/>
      <Routes>
        <Route exact path="/" element={currentElment} />
        <Route exact path="/signup" element={<SignUp changeToken={changeToken}/>} />
        <Route exact path="/login" element={<LogIn changeToken={changeToken}/>} />
        <Route component={NotFound} />
      </Routes>
    </div>
  );
}

export default App;
