import React, { useState, useEffect, useCallback, forwardRef, useImperativeHandle } from "react";
import Tile from "./tile";
import './postContainer.css';
import config from "../config.js";
import { getAllTitles } from "../api.js";

const PostsContainer = forwardRef((props, ref) => {
    const [posts, setPosts] = useState([]);
    let tiles = [ ];    

    const getPosts = useCallback(() => {
      let isFavorites = false;
      if(props.url === config.apiUrl + "/favorites") {
        isFavorites = true;
      }
      console.log("get posts!!!!")
      getAllTitles()
        .then((result) => {
          if(isFavorites === true) {
            let temp = result
            temp = temp.filter(obj => obj['in_favorites'] === true)
            if (result != null) {
              setPosts(temp);
            }
          } else {
            setPosts(result);
          }
        })
    }, [props.url]);

    useEffect(() => {
      if(props.filter !== "all") {
        setPosts(posts.filter(obj => obj['resource'] === props.filter))
      } else {
        getPosts()
      }
  }, [props.filter, getPosts]);


    useImperativeHandle(ref, () => ({
      getPosts: getPosts
    }));

    const handleTileDelete = (tileId) => {
        getPosts();
      };
    
    tiles = posts.map((post, index) => (
      <Tile key={index}
            tileId={post.id}
            onDelete={handleTileDelete}
            refresh={getPosts}
            title={post.title}
            url={post.url}
            inFavorites={post.in_favorites} />
    ));
  
    return (
        <div>
            <div className="container" style={{ columnCount: 3 }}>
                {tiles}
            </div>
        </div>
    );
  });

export default PostsContainer;
