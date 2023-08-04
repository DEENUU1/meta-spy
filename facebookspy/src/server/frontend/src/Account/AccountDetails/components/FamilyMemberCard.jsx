import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../Home/components/Loading';
import '../styles/Card.css';

const FamilyMemberCard = ({ personId }) => {
  const [familyMember, setFamilyMember] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/family_member/${personId}`)
      .then(response => {
        setFamilyMember(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [personId]);

  return (
    <div className="card">
      <h2>Work and Education History</h2>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul>
          {familyMember.map(item => (
            <li key={item.id}>
              {item.full_name} | {item.role} | {item.url}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default FamilyMemberCard;
