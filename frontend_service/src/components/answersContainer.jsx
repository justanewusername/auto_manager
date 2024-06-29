import { getAllTitles, getAnswers } from '../api';
import AnswerTile from './answerTile';
import './answersContainer.css';
import React, {useEffect, useState} from "react";

const AnswersContainer = (props) => {
    const [answers, setAnswers] = useState([]);
    let tiles = [];

    const getAllAnswers = async () => {
        await getAnswers().then((result) => {
            if (result != null) {
                setAnswers(result);
                console.log(result);
            }
        })
    }

    const getAllSummary = async () => {
        await getAllTitles().then(result => {
            if (result != null) {
                setAnswers(result);
                console.log(result);
            }
        });
    }

    useEffect(() => {
        if(props.isSummary == true) {
            getAllSummary();
        } else {
            getAllAnswers();
        }
      }, []);

    tiles = answers.map((answer, index) => (
        <AnswerTile answer={answer.answer} title={answer.post_title} url={answer.post_url} key={index}/>
    ))

    return (
        <div className="answers-container">
            {tiles}
        </div>
    );
}

export default AnswersContainer;