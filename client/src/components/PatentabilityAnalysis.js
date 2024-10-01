// src/PatentabilityAnalysis.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const PatentabilityAnalysis = () => {
  const { id } = useParams();
  const [analysis, setAnalysis] = useState({});

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await axios.get(`/api/patents/${id}/analysis`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        setAnalysis(response.data);
      } catch (error) {
        console.error('Error fetching analysis', error);
      }
    };

    fetchAnalysis();
  }, [id]);

  return (
    <div>
      <h1>Patentability Analysis</h1>
      <p>Novelty Score: {analysis.novelty_score}</p>
      <p>Utility Score: {analysis.utility_score}</p>
      <p>Obviousness Score: {analysis.obviousness_score}</p>
      <p>Patentability Score: {analysis.patentability_score}</p>
    </div>
  );
};

export default PatentabilityAnalysis;

