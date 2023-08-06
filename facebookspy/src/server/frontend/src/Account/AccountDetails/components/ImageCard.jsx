import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../../Home/components/Loading';
import "../styles/image.css";

const ImageCard = ({ personId }) => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/person/image/${personId}`)
      .then(response => {
        setImages(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [personId]);

  return (
    <div className="image-card">
      <h2>Images</h2>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul className="image-grid"> 
          {images.map(item => (
            <li key={item.id}>
              <a href={`http://localhost:8000/image/${item.id}/view`} target="_blank" rel="noopener noreferrer">
                <img src={`http://localhost:8000/image/${item.id}/view`} alt={`image ${item.id}`} />
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ImageCard;
