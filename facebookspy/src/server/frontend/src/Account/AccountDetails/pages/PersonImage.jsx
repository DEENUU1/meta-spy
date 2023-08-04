import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/Image.css';
import ImageCard from '../components/ImageCard';

const PersonImage = () => {
  const { id } = useParams();
  return (
    <div className="page-video">
      <div className="content">
        <div className='card-container'>

            <ImageCard personId={id}/>

        </div>
      </div>
    </div>
  );
};

export default PersonImage;
