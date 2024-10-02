import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';

const PatentCard = ({ patent, onDelete }) => {
  const [priorArt, setPriorArt] = useState([]);
  const [utility, setUtility] = useState({});
  const [novelty, setNovelty] = useState({});
  const [obviousness, setObviousness] = useState({});
  const [patentability, setPatentability] = useState({});
  const [users, setUsers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAdditionalData = async () => {
      try {
        const priorArtResponse = await axiosInstance.get(`/patents/${patent.id}/prior_art`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        setPriorArt(priorArtResponse.data.prior_art);

        const utilityResponse = await axiosInstance.get(`/patents/${patent.id}/analysis/utility`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        setUtility(utilityResponse.data);

        const noveltyResponse = await axiosInstance.get(`/patents/${patent.id}/analysis/novelty`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        setNovelty(noveltyResponse.data);

        const obviousnessResponse = await axiosInstance.get(`/patents/${patent.id}/analysis/obviousness`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        setObviousness(obviousnessResponse.data);

        const patentabilityResponse = await axiosInstance.get(`/patents/${patent.id}/analysis/patentability_score`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        setPatentability(patentabilityResponse.data);

        const patentResponse = await axiosInstance.get(`/patents/${patent.id}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        setUsers(patentResponse.data.users);
      } catch (error) {
        console.error('Error fetching additional data', error);
      }
    };

    fetchAdditionalData();
  }, [patent.id]);

  const handleDelete = async (id) => {
    try {
      await axiosInstance.delete(`/patents/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      onDelete(id); // Call the callback function to update the parent component's state
    } catch (error) {
      console.error('Error deleting patent', error);
    }
  };

  return (
    <div className="patent-card">
      <h2>{patent.title}</h2>
      <p>{patent.description}</p>
      <p>Status: {patent.status}</p>
      <p>
        Utility Score: <Link to={`/patents/${patent.id}/analysis/utility`}>{utility.utility_score || 'N/A'}</Link>
      </p>
      <p>
        Novelty Score: <Link to={`/patents/${patent.id}/analysis/novelty`}>{novelty.novelty_score || 'N/A'}</Link>
      </p>
      <p>
        Obviousness Score: <Link to={`/patents/${patent.id}/analysis/obviousness`}>{obviousness.obviousness_score || 'N/A'}</Link>
      </p>
      <p>
        Patentability Score: <Link to={`/patents/${patent.id}/analysis/patentability_score`}>{patentability.patentability_score || 'N/A'}</Link>
      </p>
      <div>
        <Link to={`/patents/${patent.id}/update`}>
          <button>Update</button>
        </Link>
        <Link to={`/patents/${patent.id}/prior_art`}>Show Prior Art</Link>
        <Link to={`/patents/${patent.id}/analysis`}>Analyze</Link>
        <Link to={`/patents/${patent.id}/chart`}>View Chart</Link>
        <button onClick={() => handleDelete(patent.id)}>Delete</button>
      </div>
      <div>
        <h3>Prior Art</h3>
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
    </div>
  );
};

export default PatentCard;
