import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../../Home/components/Loading';

const ReelCard = ({ personId }) => {
  const [reel, setReel] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/person/reel/${personId}`)
      .then(response => {
        setReel(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [personId]);

  return (
    <div className="card video-card">
      <h2>Reels</h2>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul>
          {reel.map(item => (
            <li key={item.id}>
              <a href={item.url}>Reel</a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ReelCard;
