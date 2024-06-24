import React, {useEffect, useState, forwardRef} from "react";
import './popup.css';
import usePostStore from "../postStore";
import { addToFavorites, generatePost, removeFromFavorites, sendPostToTg } from "../api";


const Popup = forwardRef((props, ref) => {
    const post = usePostStore((state) => state.post);
    const [isInFavorites, setIsInFavorites] = useState(props.inFavorites)
    const setPost = usePostStore((state) => state.setPost);

    const getPost = async () => {
        await generatePost(props.url);
    }

    useEffect(() => {
        getPost();

        return () => {
            setPost('');
        }
    }, [])

    useEffect(() => {
    }, [isInFavorites]);

    const edit = () => {
        console.log('edit');
    }

    const save = () => {
        if (isInFavorites) {
            removeFromFavorites(props.postId)
                .then(result => setIsInFavorites(false));
        } else {
            addToFavorites(props.postId)
                .then(result => setIsInFavorites(true));
        }
    }

    const sendToTg = async () => {
        console.log('sendToTg');
        if(post.length > 30) {
            await sendPostToTg(props.postId, props.url, post, props.title);
        }
    }

    return (
        <div ref={ref} className="popup">
            <div className="text_field">
                {post === '' ? 'Please wait...' : post }
            </div>
            <div className="button_panel">
                <button onClick={edit}>edit</button>
                <button onClick={save}>save</button>
                <button onClick={getPost}>generate again</button>
                <button onClick={sendToTg}>send to Tg. bot</button>
            </div>
        </div>
    );
});

export default Popup;
