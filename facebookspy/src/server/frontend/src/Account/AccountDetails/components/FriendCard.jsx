import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../Home/components/Loading';
import '../styles/FriendCard.css'; 

const FriendCard = ({ personId }) => {
  const [friends, setFriends] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/person/friend/${personId}`)
      .then(response => {
        setFriends(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [personId]);

  return (
    <div className="friends-card">
      <h2>Friends</h2>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul className="friend-grid">
          {friends.map(item => (
            <li className="friend-card" key={item.id}> 
              <strong>{item.full_name}</strong> <br />
              <a href={item.url}>Facebook account</a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default FriendCard;
