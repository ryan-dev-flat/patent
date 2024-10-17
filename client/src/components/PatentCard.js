import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';
import UpdatePatentForm from './UpdatePatentForm';

const PatentCard = ({ patent, onDelete }) => {
    const [users, setUsers] = useState([]);
    const [priorArt, setPriorArt] = useState([]);
    const [loadingPriorArt, setLoadingPriorArt] = useState(true);
    const [errorPriorArt, setErrorPriorArt] = useState(null);
    const [showUpdateForm, setShowUpdateForm] = useState(false);

    // States for utility, novelty, obviousness, and patentability scores
    const [utility, setUtility] = useState({});
    const [novelty, setNovelty] = useState({});
    const [obviousness, setObviousness] = useState({});
    const [patentability, setPatentability] = useState({});

    // State to toggle prior art visibility
    const [showPriorArt, setShowPriorArt] = useState(false);

    // Toggle state for score details
    const [showUtilityDetails, setShowUtilityDetails] = useState(false);
    const [showNoveltyDetails, setShowNoveltyDetails] = useState(false);
    const [showObviousnessDetails, setShowObviousnessDetails] = useState(false);
    const [showPatentabilityDetails, setShowPatentabilityDetails] = useState(false);

    const navigate = useNavigate();

    useEffect(() => {
        if (patent && patent.users) {
            setUsers(patent.users);
        }

        const fetchAdditionalData = async () => {
            try {
                // Fetch prior art
                const priorArtResponse = await axiosInstance.get(`/patents/${patent.id}/prior_art`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    }
                });
                
                if (priorArtResponse.data.prior_art && priorArtResponse.data.prior_art.length > 0) {
                    setPriorArt(priorArtResponse.data.prior_art);
                } else {
                    const searchResponse = await axiosInstance.post(`/patents/${patent.id}/prior_art`, null, {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                    setPriorArt(searchResponse.data.prior_art);
                }
            } catch (error) {
                console.error('Error fetching additional data', error);
                setErrorPriorArt('Error fetching additional data');
            } finally {
                setLoadingPriorArt(false);
            }
            
            // Fetch utility, novelty, obviousness, and patentability scores
            try {
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
            } catch (error) {
                console.error('Error fetching analysis data', error);
            }
        };

        fetchAdditionalData();
    }, [patent.id, patent.users]);

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

    const togglePriorArt = () => {
        setShowPriorArt(prevState => !prevState);
    };

    // Calculate patentability likelihood based on score
    const getPatentabilityLikelihood = (score) => {
        if (score >= 0.8) return "Highly Likely";
        if (score >= 0.5) return "Moderately Likely";
        if (score >= 0.3) return "Uncertain";
        return "Not Likely";
    };

    if (showUpdateForm) {
        return <UpdatePatentForm patentId={patent.id} />;
    }

    return (
        <div className="patent-card">
            <h2>{patent.title}</h2>
            <p>{patent.description}</p>
            <p>Status: {patent.status}</p>
            <p>Patent ID: {patent.id}</p>
            <p>Created by: {patent.created_by}</p>
            <p>Users: {users.length > 0 ? users.join(', ') : 'No users assigned'}</p>

            {/* Display utility, novelty, obviousness, and patentability scores with conditional rendering */}
            <p>
                <Link to="#" onClick={() => setShowUtilityDetails(!showUtilityDetails)}>Utility Score:</Link> {utility.utility_score || 'N/A'}
                {showUtilityDetails && (
                    <div>
                        <p><strong>Operable:</strong> {utility.operable ? 'Yes' : 'No'}</p>
                        <p><strong>Useful:</strong> {utility.useful ? 'Yes' : 'No'}</p>
                        <p><strong>Practical:</strong> {utility.practical ? 'Yes' : 'No'}</p>
                    </div>
                )}
            </p>
            <p>
                <Link to="#" onClick={() => setShowNoveltyDetails(!showNoveltyDetails)}>Novelty Score:</Link> {novelty.novelty_score || 'N/A'}
                {showNoveltyDetails && (
                    <div>
                        <p><strong>New Invention:</strong> {novelty.new_invention ? 'Yes' : 'No'}</p>
                        <p><strong>Not Publicly Disclosed:</strong> {novelty.not_publicly_disclosed ? 'Yes' : 'No'}</p>
                        <p><strong>Not Described in Printed Publication:</strong> {novelty.not_described_in_printed_publication ? 'Yes' : 'No'}</p>
                        <p><strong>Not in Public Use:</strong> {novelty.not_in_public_use ? 'Yes' : 'No'}</p>
                        <p><strong>Not on Sale:</strong> {novelty.not_on_sale ? 'Yes' : 'No'}</p>
                    </div>
                )}
            </p>
            <p>
                <Link to="#" onClick={() => setShowObviousnessDetails(!showObviousnessDetails)}>Obviousness Score:</Link> {obviousness.obviousness_score || 'N/A'}
                {showObviousnessDetails && (
                    <div>
                        <p><strong>Scope of Prior Art:</strong> {obviousness.scope_of_prior_art}</p>
                        <p><strong>Differences from Prior Art:</strong> {obviousness.differences_from_prior_art}</p>
                        <p><strong>Level of Ordinary Skill:</strong> {obviousness.level_of_ordinary_skill}</p>
                    </div>
                )}
            </p>
            <p>
                <Link to="#" onClick={() => setShowPatentabilityDetails(!showPatentabilityDetails)}>Patentability Score:</Link> {patentability.patentability_score || 'N/A'}
                {showPatentabilityDetails && (
                    <div>
                        <p><strong>Patentability Likelihood:</strong> {getPatentabilityLikelihood(patentability.patentability_score)}</p>
                    </div>
                )}
            </p>

            <div>
                <Link to={`/patents/${patent.id}/update`}>
                    <button>Update</button>
                </Link>
                <Link to={`/patents/${patent.id}/analysis`}>Deep Analysis</Link>
                <button onClick={() => handleDelete(patent.id)}>Delete</button>
            </div>

            <div>
                <button onClick={togglePriorArt}>
                    {showPriorArt ? 'Hide Prior Art' : 'Show Prior Art'}
                </button>

                {showPriorArt && (
                    <div>
                        <h3>Prior Art</h3>
                        {loadingPriorArt ? (
                            <p>Loading prior art...</p>
                        ) : errorPriorArt ? (
                            <p>{errorPriorArt}</p>
                        ) : priorArt && priorArt.length > 0 ? (
                            <ul>
                                {priorArt.map((art, index) => (
                                    <li key={index}>
                                        <p><strong>Title:</strong> {art.title}</p>
                                        <p><strong>Abstract:</strong> {art.abstract}</p>
                                        <p><strong>Patent Number:</strong> {art.patent_number}</p>
                                        {art.url && (
                                            <a href={art.url} target="_blank" rel="noopener noreferrer">
                                                View Full Patent
                                            </a>
                                        )}
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p>No prior art found.</p>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default PatentCard;
