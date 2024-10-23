import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import useAxios from '../utils/useAxios'; // Import the custom Axios hook
import UpdatePatentForm from './UpdatePatentForm';
import PatentScoreChart from './PatentScoreChart'; 

const PatentCard = ({ patent, onDelete, onUpdate }) => {
    // Log the patent prop to see what is being passed to the card
  
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

    const [chartType, setChartType] = useState('radar');

    const navigate = useNavigate();
    const axiosInstance = useAxios(); // Get the axios instance from the useAxios hook

    useEffect(() => {
        if (patent && patent.users) {
            setUsers(patent.users);
        }

        const fetchAdditionalData = async () => {
            try {
                // Fetch prior art
                const priorArtResponse = await axiosInstance.get(`/patents/${patent.id}/prior_art`);
                
                if (priorArtResponse.data.prior_art && priorArtResponse.data.prior_art.length > 0) {
                    setPriorArt(priorArtResponse.data.prior_art);
                } else {
                    const searchResponse = await axiosInstance.post(`/patents/${patent.id}/prior_art`);
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
                const utilityResponse = await axiosInstance.get(`/patents/${patent.id}/analysis/utility`);
                setUtility(utilityResponse.data);

                const noveltyResponse = await axiosInstance.get(`/patents/${patent.id}/analysis/novelty`);
                setNovelty(noveltyResponse.data);

                const obviousnessResponse = await axiosInstance.get(`/patents/${patent.id}/analysis/obviousness`);
                setObviousness(obviousnessResponse.data);

                const patentabilityResponse = await axiosInstance.get(`/patents/${patent.id}/analysis/patentability_score`);
                setPatentability(patentabilityResponse.data);
            } catch (error) {
                console.error('Error fetching analysis data', error);
            }
        };

        fetchAdditionalData();
    }, [patent.id, patent.users, axiosInstance]);

    const handleDelete = async (id) => {
        try {
            await axiosInstance.delete(`/patents/${id}`);
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

    const handleChartTypeChange = (type) => {
        setChartType(type);
    };

    if (showUpdateForm) {
        return <UpdatePatentForm patentId={patent.id} />;
    }

    return (
        <div className="card mb-4 shadow-sm">
            <div className="card-body">
                <h5 className="card-title">{patent.title}</h5>
                <p className="card-text">{patent.description}</p>

                {/* Patent Metadata */}
                <ul className="list-group list-group-flush mb-3">
                    <li className="list-group-item">Status: {patent.status}</li>
                    <li className="list-group-item">Patent ID: {patent.id}</li>
                    <li className="list-group-item">Created by: {patent.created_by}</li>
                    <li className="list-group-item">
                        Users: {users.length > 0 ? users.join(', ') : 'No users assigned'}
                    </li>
                </ul>

                {/* Utility Score with Expandable Details */}
                <p>
                    <Link to="#" onClick={() => setShowUtilityDetails(!showUtilityDetails)}>
                        Utility Score: {utility.utility_score || 'N/A'}
                    </Link>
                    {showUtilityDetails && (
                        <div className="mt-2">
                            <p><strong>Operable:</strong> {utility.operable ? 'Yes' : 'No'}</p>
                            <p><strong>Useful:</strong> {utility.useful ? 'Yes' : 'No'}</p>
                            <p><strong>Practical:</strong> {utility.practical ? 'Yes' : 'No'}</p>
                        </div>
                    )}
                </p>

                {/* Novelty Score with Expandable Details */}
                <p>
                    <Link to="#" onClick={() => setShowNoveltyDetails(!showNoveltyDetails)}>
                        Novelty Score: {novelty.novelty_score || 'N/A'}
                    </Link>
                    {showNoveltyDetails && (
                        <div className="mt-2">
                            <p><strong>New Invention:</strong> {novelty.new_invention ? 'Yes' : 'No'}</p>
                            <p><strong>Not Publicly Disclosed:</strong> {novelty.not_publicly_disclosed ? 'Yes' : 'No'}</p>
                            <p><strong>Not Described in Printed Publication:</strong> {novelty.not_described_in_printed_publication ? 'Yes' : 'No'}</p>
                            <p><strong>Not in Public Use:</strong> {novelty.not_in_public_use ? 'Yes' : 'No'}</p>
                            <p><strong>Not on Sale:</strong> {novelty.not_on_sale ? 'Yes' : 'No'}</p>
                        </div>
                    )}
                </p>

                {/* Obviousness Score with Expandable Details */}
                <p>
                    <Link to="#" onClick={() => setShowObviousnessDetails(!showObviousnessDetails)}>
                        Obviousness Score: {obviousness.obviousness_score || 'N/A'}
                    </Link>
                    {showObviousnessDetails && (
                        <div className="mt-2">
                            <p><strong>Scope of Prior Art:</strong> {obviousness.scope_of_prior_art}</p>
                            <p><strong>Differences from Prior Art:</strong> {obviousness.differences_from_prior_art}</p>
                            <p><strong>Level of Ordinary Skill:</strong> {obviousness.level_of_ordinary_skill}</p>
                        </div>
                    )}
                </p>

                {/* Patentability Score with Expandable Details */}
                <p>
                    <Link to="#" onClick={() => setShowPatentabilityDetails(!showPatentabilityDetails)}>
                        Weighted Patentability Score: {patentability.patentability_score || 'N/A'}
                    </Link>
                    {showPatentabilityDetails && (
                        <div className="mt-2">
                            <p><strong>Patentability Likelihood:</strong> {getPatentabilityLikelihood(patentability.patentability_score)}</p>
                        </div>
                    )}
                </p>

                {/* Chart Type Selection and Visualization */}
                <div className="mt-4">
                    <h6>Patent Score Visualization</h6>
                    <div className="btn-group mb-3">
                        <button
                            onClick={() => handleChartTypeChange('radar')}
                            className={`btn btn-outline-primary ${chartType === 'radar' ? 'active' : ''}`}
                        >
                            Radar Chart
                        </button>
                        <button
                            onClick={() => handleChartTypeChange('bar')}
                            className={`btn btn-outline-primary ${chartType === 'bar' ? 'active' : ''}`}
                        >
                            Bar Chart
                        </button>
                        <button
                            onClick={() => handleChartTypeChange('pie')}
                            className={`btn btn-outline-primary ${chartType === 'pie' ? 'active' : ''}`}
                        >
                            Pie Chart
                        </button>
                    </div>
                    <PatentScoreChart
                        utility={utility}
                        novelty={novelty}
                        obviousness={obviousness}
                        patentability={patentability}
                        chartType={chartType}
                    />
                </div>

                {/* Action Buttons */}
                <div className="mt-4">
                    <Link to={`/patents/${patent.id}/update`} className="btn btn-warning me-2">
                        Update Patent
                    </Link>
                    <button onClick={() => handleDelete(patent.id)} className="btn btn-danger">
                        Delete Patent
                    </button>
                </div>

                {/* Prior Art Section */}
                <div className="mt-4">
                    <button onClick={togglePriorArt} className="btn btn-outline-secondary">
                        {showPriorArt ? 'Hide Prior Art' : 'Show Prior Art'}
                    </button>

                    {showPriorArt && (
                        <div className="mt-3">
                            <h6>Prior Art</h6>
                            {loadingPriorArt ? (
                                <p>Loading prior art...</p>
                            ) : errorPriorArt ? (
                                <p className="text-danger">{errorPriorArt}</p>
                            ) : priorArt && priorArt.length > 0 ? (
                                <ul className="list-group">
                                    {priorArt.map((art, index) => (
                                        <li key={index} className="list-group-item">
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
        </div>
    );
};

export default PatentCard;