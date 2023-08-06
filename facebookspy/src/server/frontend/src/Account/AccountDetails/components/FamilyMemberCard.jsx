import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../../Home/components/Loading';
import '../styles/Card.css';

const FamilyMemberCard = ({ personId }) => {
  const [familyMember, setFamilyMember] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/person/family_member/${personId}`)
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
    <div className="card family-member-card">
      <h2>Family members</h2>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul>
          {familyMember.map(item => (
            <li key={item.id}>
              <a href={item.url} target="_blank" rel="noopener noreferrer">
              <strong>{item.full_name}</strong> </a> - {item.role}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default FamilyMemberCard;
