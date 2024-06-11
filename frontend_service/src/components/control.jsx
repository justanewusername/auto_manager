import React, { useState } from "react";
import axios from "axios";
import './control.css';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import config from "../config.js";

function Control({ changePage, onRefreshClick, setFilter }) {
    const [selectedResourceOption, setSelectedResourceOption] = useState("all");
    const [selectedTypeOption, setSelectedTypeOption] = useState("all");
    const [response, setResponse] = useState(null);

    const resourcesOptions = [
        "all", 
        "scientificamerican", 
        "MIT", 
        "extremetech", 
        'gizmodo', 
        'venturebeat', 
        'synced',
    ];
    const typeOptions = ["all", "AI", "Tech"];

    const handleResourceOptionChange = (event) => {
        setSelectedResourceOption(event.target.value);
    };

    const handleTypeOptionChange = (event) => {
        setSelectedTypeOption(event.target.value);
    };

    const applyFilters = () => {
        setFilter(selectedResourceOption);
    }

    const postData = async () => {
        try {
          console.log('@@@@@@@@@@@@@@@@@');
          console.log(selectedResourceOption);
          const response = await axios.post(
            config.apiUrl + '/posts/titles/test',
            {
              resources: [selectedResourceOption],
              urls: [],
              period_days: 10,
            }
          );
    
          // Set the response in the state
          setResponse(response.data);
        } catch (error) {
          console.error("Error:", error);
        }
    };

    const onMainPageSet = () => {
        changePage("main");
    };

    const onFavoritesPageSet = () => {
        changePage("favorites");
    };

    return (
        <div className="control">
            <div className="panel__left">
                <button className="button-primary" onClick={onMainPageSet}>Главная</button>
                <button className="button-primary" onClick={onFavoritesPageSet}>Избранное</button>
                {/* <Link className="link__button" to="/">Главная</Link>
                <Link className="link__button" to="/favorites">Избранное</Link> */}
            </div>


            <div className="panel__center">
                <button className="button-primary" onClick={onRefreshClick} >Обновить</button>
                <div className="panel__list">
                    <p>Выбрать категорию</p>
                    <select value={selectedTypeOption} onChange={handleTypeOptionChange}>
                        {typeOptions.map((option) => (
                            <option key={option} value={option}>
                                {option}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="panel__list">
                    <p>Выбрать ресурс</p>
                    <select value={selectedResourceOption} onChange={handleResourceOptionChange}>
                        {resourcesOptions.map((option) => (
                            <option key={option} value={option}>
                                {option}
                            </option>
                        ))}
                    </select>
                </div>
                <button className="button-primary" onClick={applyFilters}>Применить</button>
                <button className="button-primary" onClick={postData}>Запустить парсер</button>
                <div className="button-login" onClick={applyFilters}>Log In</div>
                <div className="button-signin" onClick={applyFilters}>Sign In</div>
            </div>

            <div className="panel__right">
                <a target="_blank" rel="noreferrer" href={config.apiUrl + '/download/all'}>Скачать файл</a>
            </div>
        </div>
    );
}

export default Control;
