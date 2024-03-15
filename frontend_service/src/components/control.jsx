import React, { useState } from "react";
import axios from "axios";
import './control.css';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

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
          const response = await axios.post(
            "http://185.233.81.221:8811/run",
            {
              name: selectedResourceOption,
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
                <button onClick={onMainPageSet}>Главная</button>
                <button onClick={onFavoritesPageSet}>Избранное</button>
                {/* <Link className="link__button" to="/">Главная</Link>
                <Link className="link__button" to="/favorites">Избранное</Link> */}
            </div>


            <div className="panel__center">
                <button onClick={onRefreshClick} >Обновить</button>
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
                <button onClick={applyFilters}>Применить</button>
                <button onClick={postData}>Запустить парсер</button>
            </div>

            <div className="panel__right">
                <a target="_blank" rel="noreferrer" href='http://185.233.81.221:8811/download/all'>Скачать файл</a>
            </div>
        </div>
    );
}

export default Control;
