import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../Home/components/Loading';

const PlacesCard = ({ personId }) => {
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/place/${personId}`)
      .then(response => {
        setPlaces(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [personId]);

  return (
    <div className="card places-card">
      <h2>Reviews</h2>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul>
          {places.map(item => (
            <li key={item.id}>
              <strong>Place:</strong> {item.name}<br />
              <strong>Date:</strong> {item.date}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default PlacesCard;
