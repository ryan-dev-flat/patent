// src/PatentabilityAnalysis.js
import React, { useState } from 'react';
import axios from 'axios';

function PatentabilityAnalysis({ token }) {
    const [idea, setIdea] = useState('');
    const [analysis, setAnalysis] = useState({});

    const submitIdea = async () => {
        const res = await axios.post('http://localhost:5000/patentability_analysis', { idea }, {
            headers: { Authorization: `Bearer ${token}` }
        });
        setAnalysis(res.data.analysis);
    };

    return (
        <div>
            <h2>Patentability Analysis</h2>
            <textarea placeholder="Describe your invention idea..." onChange={(e) => setIdea(e.target.value)}></textarea>
            <button onClick={submitIdea}>Submit</button>
            <div>
                <h3>Analysis:</h3>
                <p><strong>Novelty:</strong> {analysis.novelty}</p>
                <p><strong>Non-obviousness:</strong> {analysis.non_obviousness}</p>
                <p><strong>Utility:</strong> {analysis.utility}</p>
                <h4>Relevant Precedents:</h4>
                <ul>
                    {analysis.precedents && analysis.precedents.map((precedent, index) => (
                        <li key={index}>{precedent}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default PatentabilityAnalysis;
