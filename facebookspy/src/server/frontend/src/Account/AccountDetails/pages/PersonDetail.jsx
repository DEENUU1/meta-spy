import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import '../styles/PersonDetail.css';
import LoadingDots from '../../Home/components/Loading';
import ReviewsCard from '../components/ReviewsCard';
import WorkAndEducationCard from '../components/WorkAndEducationCard';
import FamilyMemberCard from '../components/FamilyMemberCard';


const PersonDetail = () => {
  const { id } = useParams();
  const [person, setPerson] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get(`http://localhost:8000/person/${id}`)
      .then(response => {
        setPerson(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [id]);

  return (
    <div className="pagex">
      <div className="content">
        <h1>Person Detail</h1>
        {loading ? (
          <LoadingDots />
        ) : (
          <div className="person-details">
            <div className="detail-item">
              <strong>ID:</strong> {person.id}
            </div>
            <div className="detail-item">
              <strong>Full Name:</strong> {person.full_name}
            </div>
            <div className="detail-item">
              <strong>Facebook ID:</strong> {person.facebook_id}
            </div>

            <ReviewsCard personId={id} />
            <WorkAndEducationCard personId={id} />
            <FamilyMemberCard personId={id} />

            
          </div>
        )}
      </div>
    </div>
  );
};

export default PersonDetail;
