import React, {useState} from "react";
import './tile.css'
import axios from "axios";

function Tile(props) {
    const {isInFavorites, setIsInFavorites} = useState(props.in_favorite)

    const handleDelete = () => {
        props.onDelete(props.tileId);
    };

    const deletePost = () => {
        axios.post("http://localhost:8811/del", {name: props.tileId})
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
        axios.post("http://localhost:8811/favorites/create/", {name: props.tileId})
        .then(response => {
            setIsInFavorites(true)
        })
        .catch(error => {
          console.error("Error fetching posts:", error);
        });
    }

    const removeFromFavorites = () => {
        axios.post("http://localhost:8811/favorites/del/", {name: props.tileId})
        .then(response => {
            setIsInFavorites(false)
        })
        .catch(error => {
          console.error("Error fetching posts:", error);
        });
    }

    return (
        <div className="tile">
            <h3 className="tile_title">{props.title}</h3>
            <p className="tile_post">
                {props.post}
            </p>
            <button className={isInFavorites ? "button_active" : ""} onClick={onFavoritesClick}>
                {isInFavorites ? "Сохранено в избранном" : "В избранное"}
            </button>
            <a className="tile_source" target="_blank" rel="noreferrer" href={props.url}>source</a>
            <button className="tile__button-red" onClick={deletePost}>удалить</button>
        </div>
    );
}

export default Tile;
