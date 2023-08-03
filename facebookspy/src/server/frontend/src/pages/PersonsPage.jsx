import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios'; 
import '../styles/PersonsPage.css';

const PersonsPage = () => {
  const [persons, setPersons] = useState([]);
  const [loading, setLoading] = useState(true); 
  const [dots, setDots] = useState(''); 

  useEffect(() => {
    const interval = setInterval(() => {
      setDots(dots => (dots.length === 3 ? '' : dots + '.')); 
    }, 500); 

    setTimeout(() => {
      axios.get('http://127.0.0.1:8000/person/')
        .then(response => {
          setPersons(response.data);
          setLoading(false); 
        })
        .catch(error => {
          console.error('Error fetching data:', error);
          setLoading(false); 
        });
    }, 5000); 

    return () => {
      clearInterval(interval); 
    };
  }, []);

  return (
    <div className="page">
      <div className="content">
        <h1>Scraped persons</h1>
        {loading ? ( 
          <div className="loading">Loading{dots}</div> 
        ) : (
          <ul className="person-list">
            {persons.map(person => (
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
          ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default PersonsPage;
