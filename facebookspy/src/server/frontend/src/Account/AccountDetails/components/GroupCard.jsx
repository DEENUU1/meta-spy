import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../../Home/components/Loading';

const GroupCard = ({ personId }) => {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);  

  useEffect(() => {
    axios.get(`http://localhost:8000/person/group/${personId}`)
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
    <div className="card groups-card">
      <h2>Groups</h2>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul>
          {groups.map(item => (
            <li key={item.id}>
              {item.name}
              {item.url}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default GroupCard;
