import React, {useState, useEffect} from "react";
import './tile.css'
import axios from "axios";
import config from "../config.js";

function Tile(props) {
    console.log("hello", props.in_favorite)
    const [isInFavorites, setIsInFavorites] = useState(props.in_favorite)

    const handleDelete = () => {
        props.onDelete(props.tileId);
    };

    useEffect(() => {
      }, [isInFavorites]);
  
    useEffect(() => {
        setIsInFavorites(props.in_favorite);
    }, [props.in_favorite]);

    const deletePost = () => {
        axios.post(config.apiUrl + "/del", {"number": props.tileId})
        .then(response => {
            handleDelete();
        })
        .catch(error => {
          console.error("Error fetching posts:", error);
        });
    }

    const onFavoritesClick = () => {
        if (isInFavorites) {
            removeFromFavorites();
        }
        else {
            addToFavorites();
        }
    }

    const addToFavorites = () => {
        axios.post(config.apiUrl + "/favorites/create/", {number: props.tileId})
        .then(response => {
            setIsInFavorites(true)
        })
        .catch(error => {
          console.error("Error fetching posts:", error);
        });
    }

    const removeFromFavorites = () => {
        axios.post(config.apiUrl + "/favorites/del/", {number: props.tileId})
        .then(response => {
            setIsInFavorites(false)
        })
        .catch(error => {
          console.error("Error fetching posts:", error);
        });
    }

    const generatePost = () => {
        
    }

    return (
        <div className="tile">
            <h3 className="tile_title">{props.title}</h3>
            <div className="button_container">
                <a className="tile_source" target="_blank" rel="noreferrer" href={props.url}>view source</a>
                {/* <button className={isInFavorites ? "button_active" : ""} onClick={onFavoritesClick}>
                    {isInFavorites ? "Сохранено в избранном" : "В избранное"}
                </button> */}
                <button className="tile__button" onclick={generatePost}>generate post</button>
                <button className="tile__button" onClick={deletePost}>summarize</button>
            </div>
        </div>
    );
}

export default Tile;
