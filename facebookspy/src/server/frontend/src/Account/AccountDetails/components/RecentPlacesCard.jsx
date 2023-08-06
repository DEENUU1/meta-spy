import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../../Home/components/Loading';
import '../styles/RecentPlacesCard.css'; 
import GoogleSearch from '../../../Home/components/GoogleSearch';

const RecentPlacesCard = ({ personId }) => {
  const [recentPlaces, setRecentPlaces] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/person/recent_place/${personId}`)
      .then(response => {
        setRecentPlaces(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [personId]);

  return (
    <div className="recent-places-card">
      <h2>Recent Places</h2>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul className="recent-places-grid">
          {recentPlaces.map(item => (
            <li className="friend-card" key={item.id}> 
              <strong>{item.localization}</strong> <br />
              <p>{item.date}</p>
              <GoogleSearch value={item.localization} />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default RecentPlacesCard;
