import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';

const PriorArtComponent = () => {
    const { id } = useParams();
    const [priorArt, setPriorArt] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPriorArt = async () => {
            try {
                const response = await axiosInstance.get(`/patents/${id}/prior_art`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    }
                });
                setPriorArt(response.data.prior_art);
            } catch (err) {
                setError('Error fetching prior art');
            } finally {
                setLoading(false);
            }
        };

        fetchPriorArt();
    }, [id]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div>
            <h2>Prior Art for Patent {id}</h2>
            {priorArt.length > 0 ? (
                <ul>
                    {priorArt.map((art, index) => (
                        <li key={index}>
                            <p>Title: {art.title}</p>
                            <p>Abstract: {art.abstract}</p>
                            <p>Patent Number: {art.patent_number}</p>
                            <a href={art.url} target="_blank" rel="noopener noreferrer">View Patent</a>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No prior art found.</p>
            )}
        </div>
    );
};

export default PriorArtComponent;
