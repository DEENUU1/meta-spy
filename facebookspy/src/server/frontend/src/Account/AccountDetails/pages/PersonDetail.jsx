import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom'; 
import axios from 'axios';
import '../styles/PersonDetail.css';
import LoadingDots from '../../Home/components/Loading';
import ReviewsCard from '../components/ReviewsCard';
import WorkAndEducationCard from '../components/WorkAndEducationCard';
import FamilyMemberCard from '../components/FamilyMemberCard';
import PlacesCard from '../components/PlacesCard';

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
        {loading ? (
          <LoadingDots />
        ) : (
          <div className="person-details">
            <h1>{person.facebook_id} details</h1>
            <div className="detail-item">
              {person.full_name}
              <Link to={`/person/${id}/video`}>Videos & Reels</Link> <br/>
              <Link to={`/person/${id}/image`}>Images</Link> <br/>
              <Link to={`/person/${id}/friend`}>Friends</Link> <br/>
              <Link to={`/person/${id}/place`}>Recent Places</Link>
            </div>

            <div className='card-container'>

              <FamilyMemberCard personId={id} />
              <WorkAndEducationCard personId={id} />
              <PlacesCard personId={id} />
              <ReviewsCard personId={id} />

            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PersonDetail;
