import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../../Home/components/Loading';

const GroupCard = ({ personId }) => {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    axios.get(`http://localhost:8000/groups/${personId}`)
      .then(response => {
        setGroups(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [personId]);

  
  return (
      <div className="group-card">
      <h2>Events</h2>
      
      {loading ? (
        <LoadingDots />
      ) : (
        <ul className="group-grid">
          {(searchTerm ? searchResults : groups).map(item => (
            <li className="group-card" key={item.id}> 
              <strong>{item.name}</strong> <br />
              <a href={item.url}>Facebook link</a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default GroupCard;
