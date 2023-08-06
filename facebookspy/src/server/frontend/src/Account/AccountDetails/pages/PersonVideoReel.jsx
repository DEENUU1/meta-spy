import React from 'react';
import { useParams } from 'react-router-dom';
import VideoCard from '../components/VideoCard';
import ReelCard from '../components/ReelCard';
import '../styles/VideoReel.css';

const PersonVideoReel = () => {
  const { id } = useParams();
  return (
    <div className="page-video">
      <div className="content">
        <div className='card-container'>
          <VideoCard personId={id} />
          <ReelCard personId={id} />
        </div>
      </div>
    </div>
  );
};

export default PersonVideoReel;
