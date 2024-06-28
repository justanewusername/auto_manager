import './filters.css';
import React, {useState} from 'react';

const Filters = (props) => {
    const [selectedResourceOption, setSelectedResourceOption] = useState("all");
    const [selectedTypeOption, setSelectedTypeOption] = useState("all");

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


    return(
        <div className='filters'>
            <div className='filters-info'>
                <p><span>Last update:</span> {props.lastUpdate}</p>
                <p><span>Period:</span> {props.period}</p>
            </div>
            <div className='filters-settings'>
                <div className='filters-settings__left'>
                    <div className='option-container'>
                        <p><span>Set period (days):</span></p>
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
                    <button className='secondary-btn update_btn'>Update</button>
                </div>
            </div>
        </div>
    )
}

export default Filters;