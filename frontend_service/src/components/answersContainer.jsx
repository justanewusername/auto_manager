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
            }
        })
    }

    const getAllSummary = async () => {
        await getAllTitles().then(result => {
            if (result != null) {
                setAnswers(result);
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
        <AnswerTile answer={answer.answer} key={index}/>
    ))

    return (
        <div className="answers-container">
            {tiles}
        </div>
    );
}

export default AnswersContainer;