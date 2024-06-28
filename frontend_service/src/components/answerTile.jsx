import './answersTile.css'
import React from "react";

const AnswerTile = (props) => {
    return (
        <div className="answers-tile">
            {props.answer}
        </div>
    );
}

export default AnswerTile;