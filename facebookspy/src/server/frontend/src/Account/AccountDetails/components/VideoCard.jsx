import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../Home/components/Loading';

const VideoCard = ({ personId }) => {
  const [video, setVideo] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/video/${personId}`)
      .then(response => {
        setVideo(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [personId]);

  return (
    <div className="card video-card">
      <h2>Videos</h2>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul>
          {video.map(item => (
            <li key={item.id}>
              <a href={item.url}>Video</a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default VideoCard;
