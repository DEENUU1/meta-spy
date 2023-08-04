import React from 'react';
import { useParams } from 'react-router-dom';
import FriendCard from '../components/FriendCard';

const PersonFriendList = () => {
  const { id } = useParams();
  return (
    <div className="page-friends">
      <div className="content-friend">
        <div className='card-friend-container'>

            <FriendCard personId={id}/>

        </div>
      </div>
    </div>
  );
};

export default PersonFriendList;
