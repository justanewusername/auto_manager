import { runTitleParser } from '../api';
import './filters.css';
import React, {useState, useEffect} from 'react';

const Filters = (props) => {
    const [selectedResourceOption, setSelectedResourceOption] = useState("all");
    const [selectedTypeOption, setSelectedTypeOption] = useState("all");
    const [lastUpdate, setLastUpdate] = useState('')
    const [period, setPeriod] = useState('');
    const [updatePeriod, setUpdatePeriod] = useState(10);

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
        props.changeResource(event.target.value.toUpperCase());
        setSelectedResourceOption(event.target.value);
    };

    const handleTypeOptionChange = (event) => {
        props.changeCategorie(event.target.value);
        setSelectedTypeOption(event.target.value);
    };

    const postData = async () => {
        runTitleParser('all');
    };

    useEffect(() => {
        const timer = setTimeout(() => {
            setPeriod('10');
            setLastUpdate('28.06.2024');
        }, 2000);

        return () => clearTimeout(timer);
    }, []);

    const handlePeriodChange = (event) => {
        const newValue = event.target.value;
        if (newValue >= 3 && newValue <= 30) {
            setUpdatePeriod(newValue);
        }
    };

    return(
        <div className='filters'>
            <div className='filters-info'>
                <p><span>Last update:</span> {lastUpdate}</p>
                <p><span>Period:</span> {period}</p>
            </div>
            <div className='filters-settings'>
                <div className='filters-settings__left'>
                    <div className='option-container'>
                        <p><span>Set period (days):</span></p>
                        <div className='custom-input'>
                            <input type="number" value={updatePeriod} onChange={handlePeriodChange} min="3" max="30" className='period-input'/>
                        </div>
                    </div>

                    <div className='option-container'>
                        <p><span>Set resource:</span></p>
                        <div className='custom-select'>
                            <select value={selectedResourceOption} onChange={handleResourceOptionChange}>
                                {resourcesOptions.map((option) => (
                                    <option key={option} value={option}>
                                        {option}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>


                    <div className='option-container'>
                        <p><span>Set category:</span></p>
                        <div className='custom-select'>
                            <select value={selectedTypeOption} onChange={handleTypeOptionChange}>
                                {typeOptions.map((option) => (
                                    <option key={option} value={option}>
                                        {option}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>


                </div>
                <div className='filters-settings__right'>
                    <button className='secondary-btn update_btn' onClick={postData}>Update</button>
                </div>
            </div>
        </div>
    )
}

export default Filters;