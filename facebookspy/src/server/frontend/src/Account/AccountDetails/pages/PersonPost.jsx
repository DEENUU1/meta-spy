import React from 'react';
import { useParams } from 'react-router-dom';
import PostCard from '../components/PostCard';

const PersonPost = () => {
  const { id } = useParams();
  return (
    <div className="page-post">
      <div className="content-post">
        <div className='card-post-container'>

            <PostCard personId={id}/>

        </div>
      </div>
    </div>
  );
};

export default PersonPost;
