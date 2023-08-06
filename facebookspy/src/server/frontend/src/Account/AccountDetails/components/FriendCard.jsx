import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../Home/components/Loading';
import '../styles/FriendCard.css'; 

const FriendCard = ({ personId }) => {
  const [friends, setFriends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);

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

  useEffect(() => {
    if (searchTerm) {
      axios.get(`http://localhost:8000/friends/search/?search_term=${searchTerm}`)
        .then(response => {
          setSearchResults(response.data);
        })
        .catch(error => {
          console.error('Error searching friends:', error);
        });
    } else {
      setSearchResults([]);
    }
  }, [searchTerm]);

  return (
      <div className="friends-card">
      <h2>Friends</h2>
      <div className="search-form">
        <input
          type="text"
          placeholder="Search friends..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
        />
      </div>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul className="friend-grid">
          {(searchTerm ? searchResults : friends).map(item => (
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
