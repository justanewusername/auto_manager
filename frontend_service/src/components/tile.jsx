import React, {useState, useEffect, useRef} from "react";
import './tile.css';
import Popup from "./popup.jsx";
import { deletePostById } from "../api.js";

function Tile(props) {
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const popupRef = useRef(null);

    const handleDelete = () => {
        props.onDelete(props.tileId);
    };

    useEffect(() => {
        // Функция-обработчик события клика за пределами div
        const handleClickOutside = (event) => {
            if (popupRef == null) {
                return
            }
            else if (popupRef.current && !popupRef.current.contains(event.target)) {
                console.log('Клик за пределами div');
                setIsPopupOpen(false);
            }
        };
    
        document.addEventListener('mousedown', handleClickOutside);
    
        return () => {
          document.removeEventListener('mousedown', handleClickOutside);
        };
      }, []);

    const deletePost = async () => {
        await deletePostById(props.tileId)
            .then(result => {
                handleDelete();
            });
    }

    const generatePost = () => {
        setIsPopupOpen(!isPopupOpen);
    }

    return (
        <div className="tile">
            <div className="close-btn" onClick={deletePost}>x</div>
            {isPopupOpen ? <Popup ref={popupRef}
                                  url={props.url}
                                  postId={props.tileId} 
                                  title={props.title}
                                  inFavorites={props.inFavorites}/> : null}
            <h3 className="tile_title">{props.title}</h3>
            <div className="button_container">
                <a className="tile_source" target="_blank" rel="noreferrer" href={props.url}>view source</a>
                <button className="secondary-btn" onClick={generatePost}>generate post</button>
                <button className="secondary-btn" onClick={generatePost}>summarize</button>
            </div>
        </div>
    );
}

export default Tile;
