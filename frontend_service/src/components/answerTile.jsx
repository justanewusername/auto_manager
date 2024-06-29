import './answersTile.css'
import React from "react";

const AnswerTile = (props) => {
    return (
        <div className="answers-tile">
            <div className='answer-title'>
                {props.title}
            </div>
            <div className='answer-text'>
                {props.answer}
            </div>
            <a className="tile_source" target="_blank" rel="noreferrer" href={props.url}>view source</a>
        </div>
    );
}

export default AnswerTile;