import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../Home/components/Loading';

const ImageCard = ({ personId }) => {
  const [image, setImage] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/image/${personId}`)
      .then(response => {
        setImage(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [personId]);

  return (
    <div className="card video-card">
      <h2>Images</h2>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul>
          {image.map(item => (
            <li key={item.id}>
              <img src={item.path}/>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ImageCard;
