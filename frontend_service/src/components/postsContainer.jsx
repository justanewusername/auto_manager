import React, { useState, useEffect, forwardRef, useImperativeHandle } from "react";
import Tile from "./tile";
import './postContainer.css';
import axios from "axios";

const PostsContainer = forwardRef((props, ref) => {
    const [posts, setPosts] = useState([]);
    // const [tiles, setTiles] = useState();
    let tiles = [ ];

    const getPosts = () => {
      axios.get(props.url) //get("http://localhost:8811/all")
      .then(response => {
        setPosts(response.data);
      })
      .catch(error => {
        console.error("Error fetching posts:", error);
      });
    }

    useImperativeHandle(ref, () => ({
      getPosts: getPosts
    }));

    const handleTileDelete = (tileId) => {
        getPosts();
      };

    useEffect(() => {
        // Fetch posts from the external API
        getPosts()
    }, [props.url]);
    
    tiles = posts.map((post, index) => (
      <Tile key={index}
            tileId={post.id}
            post={post.article}
            onDelete={handleTileDelete}
            refresh={getPosts}
            title={post.title}
            url={post.url}
            in_favorite={post.in_favorites} />
    ));
  
    return (
        <div>
            <p className="container__name">Сгенерированные посты:</p>
            <div className="container" style={{ columnCount: 3 }}>
                {tiles}
            </div>
        </div>
    );
  });

export default PostsContainer;
