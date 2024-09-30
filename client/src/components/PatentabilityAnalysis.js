// src/PatentabilityAnalysis.js
import React, { useState } from 'react';
import axios from 'axios';

function PatentabilityAnalysis() {
    const [idea, setIdea] = useState('');
    const [analysis, setAnalysis] = useState({});
    const [priorArt, setPriorArt] = useState([]);
    const [utility, setUtility] = useState({});
    const [novelty, setNovelty] = useState({});

    const handleSubmitIdea = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post('http://127.0.0.1:5000/api/patentability_analysis', { idea }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setAnalysis(response.data.analysis);
            setPriorArt(response.data.analysis.prior_art);
        } catch (error) {
            alert('Failed to analyze idea');
        }
    };

    const handleSubmitUtility = async () => {
        // Implement utility submission logic
    };

    const handleSubmitNovelty = async () => {
        // Implement novelty submission logic
    };

    return (
        <div>
            <h2>Patentability Analysis</h2>
            <textarea value={idea} onChange={(e) => setIdea(e.target.value)} />
            <button onClick={handleSubmitIdea}>Submit</button>
            <div>
                <h3>Utility Questions</h3>
                <form>
                    <label>Prototype Built</label>
                    <input type="checkbox" onChange={(e) => setUtility({ ...utility, operability: e.target.checked })} />
                    <label>Prototype Works</label>
                    <input type="checkbox" onChange={(e) => setUtility({ ...utility, beneficial: e.target.checked })} />
                    <label>Practical Applications</label>
                    <textarea onChange={(e) => setUtility({ ...utility, practical: e.target.value })} />
                    <button onClick={handleSubmitUtility}>Submit Utility</button>
                </form>
            </div>
            <div>
                <h3>Novelty Questions</h3>
                <form>
                    <label>Published</label>
                    <input type="checkbox" onChange={(e) => setNovelty({ ...novelty, printed_pub: e.target.checked })} />
                    <label>On Sale</label>
                    <input type="checkbox" onChange={(e) => setNovelty({ ...novelty, on_sale: e.target.checked })} />
                    <label>Publicly Available</label>
                    <input type="checkbox" onChange={(e) => setNovelty({ ...novelty, publicly_available: e.target.checked })} />
                    <button onClick={handleSubmitNovelty}>Submit Novelty</button>
                </form>
            </div>
            <div>
                <h3>Analysis</h3>
                <p>Novelty: {analysis.novelty}</p>
                <p>Non-obviousness: {analysis.non_obviousness}</p>
                <p>Utility: {analysis.utility}</p>
                <p>Overall Score: {analysis.overall_score}</p>
                <h4>Relevant Precedents</h4>
                <ul>
                    {priorArt.map((art, index) => (
                        <li key={index}>{art.title}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default PatentabilityAnalysis;
