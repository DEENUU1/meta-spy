import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios'; 

const PersonsPage = () => {
  const [persons, setPersons] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/person/')
      .then(response => setPersons(response.data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="page">
      <div className="content">
        <h1>Scraped persons</h1>
        <ul>
          {persons.map(person => (
            <li key={person.id}>
              <Link to={`/person/${person.id}`}>
                {person.id} - {person.full_name && person.full_name + ' '} 
                {person.facebook_id && person.facebook_id}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default PersonsPage;
