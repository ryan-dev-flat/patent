import React from 'react';

const PriorArtComponent = ({ priorArt }) => {
    if (!priorArt || priorArt.length === 0) {
        return <p>No prior art found.</p>;
    }

    return (
        <div>
            <h2>Prior Art</h2>
            <ul>
                {priorArt.map((art, index) => (
                    <li key={index}>
                        <p><strong>Title:</strong> {art.title}</p>
                        <p><strong>Abstract:</strong> {art.abstract}</p>
                        <p><strong>Patent Number:</strong> {art.patent_number}</p>
                        {/* Link to view the full patent */}
                        {art.url && (
                            <a href={art.url} target="_blank" rel="noopener noreferrer">
                                View Full Patent
                            </a>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default PriorArtComponent;