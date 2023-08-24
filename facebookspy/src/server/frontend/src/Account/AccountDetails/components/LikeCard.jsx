import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../../Home/components/Loading';

const LikeCard = ({ personId }) => {
  const [likes, setLikes] = useState([]);
  const [loading, setLoading] = useState(true);  

  useEffect(() => {
    axios.get(`http://localhost:8000/like/${personId}`)
      .then(response => {
        setLikes(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [personId]);

  return (
    <div className="card likes-card">
      <h2>Likes</h2>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul>
          {likes.map(item => (
            <li key={item.id}>
              {item.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default LikeCard;
