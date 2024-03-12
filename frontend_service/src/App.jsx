import './App.css';
import Control from './components/control';
import Favorites from './components/favorites';
import PostsContainer from './components/postsContainer';
import React, { useState, useRef, useCallback } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

function App() {
  const postContainerRef = useRef(null);
  const [postContainerUrl, setPostContainerUrl] = useState("http://localhost:8811/all");



  const refresh = useCallback(() => {
    postContainerRef.current.getPosts();
  }, []);

  const changePage = (currentPage) => {
    if(currentPage === "main") {
      setPostContainerUrl("http://localhost:8811/all")
    } else {
      setPostContainerUrl("http://localhost:8811/hello")
    }
  };

  return (
    <div className="App">
      <Control changePage={changePage} onRefreshClick={refresh}/>
      <PostsContainer url={postContainerUrl} ref={postContainerRef}/>
      {/* <Routes>
        <Route path="/" element={<PostsContainer url={postContainerUrl} ref={postContainerRef}/>}/>
        <Route path='/favorites' element={<Favorites />}/>
      </Routes> */}
    </div>
  );
}

export default App;
