import React from 'react';
import { useParams } from 'react-router-dom';
import RecentPlacesCard from '../components/RecentPlacesCard';


const PersonRecentPlaces = () => {
  const { id } = useParams();
  return (
    <div className="page-recent-places">
      <div className="content-recent-places">
        <div className='card-recent-places-container'>

            <RecentPlacesCard personId={id}/>

        </div>
      </div>
    </div>
  );
};

export default PersonRecentPlaces;
