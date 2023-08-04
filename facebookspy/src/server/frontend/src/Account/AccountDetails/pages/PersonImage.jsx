import React from 'react';
import { useParams } from 'react-router-dom';
import ImageCard from '../components/ImageCard';

const PersonImage = () => {
  const { id } = useParams();
  return (
    <div className="page-image">
      <div className="content-image">
        <div className='card-image-container'>

            <ImageCard personId={id}/>

        </div>
      </div>
    </div>
  );
};

export default PersonImage;
