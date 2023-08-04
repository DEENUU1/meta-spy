import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from './Loading';

const WorkAndEducationCard = ({ personId }) => {
  const [workAndEducation, setWorkAndEducation] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/work_and_education/${personId}`)
      .then(response => {
        setWorkAndEducation(response.data);
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
          {workAndEducation.map(item => (
            <li key={item.id}>
              {item.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default WorkAndEducationCard;
