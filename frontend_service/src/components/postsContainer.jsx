import React, { useState, useEffect, useCallback, forwardRef, useImperativeHandle } from "react";
import Tile from "./tile";
import './postContainer.css';
import axios from "axios";
import config from "../config.js";

const PostsContainer = forwardRef((props, ref) => {
    const [posts, setPosts] = useState([]);
    // const [tiles, setTiles] = useState();
    let tiles = [ ];    

    const getPosts = useCallback(() => {
      console.log("get posts!!!!")
      console.log(props.url)
      axios.get(props.url)
      .then(response => {
        console.log("####")
        console.log(response.data)
        response.data.forEach(x => console.log(x.resource));

        if(props.url === config.apiUrl + "/favorites") {
          let temp = response.data
          temp = temp.filter(obj => obj['in_favorites'] === true)
          setPosts(temp);
          console.log(temp)
        } else {
          setPosts(response.data);
        }

      })
      .catch(error => {
        console.error("Error fetching posts:", error);
      });
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

    // useEffect(() => {
    //     // Fetch posts from the external API
    //     getPosts()
    // }, [props.url, getPosts]);
    
    tiles = posts.map((post, index) => (
      <Tile key={index}
            tileId={post.id}
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
