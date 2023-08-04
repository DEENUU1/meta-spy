import React from 'react';
import { Link } from 'react-router-dom';

const PersonCard = ({ person }) => (
  <li key={person.id} className="person-card">
    <Link to={`/person/${person.id}`}>
      <div className="person-info">
        <div className="facebook-id">{person.facebook_id}</div>
        <div className="other-info">
          {person.full_name && <div className="full-name">{person.full_name}</div>}
        </div>
      </div>
    </Link>
  </li>
);

export default PersonCard;
