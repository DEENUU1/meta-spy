import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/PersonsPage.css';
import LoadingDots from '../components/Loading';
import PersonCard from '../components/PersonCard';

const PersonsPage = () => {
  const [persons, setPersons] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      axios
        .get('http://127.0.0.1:8000/person/')
        .then(response => {
          setPersons(response.data);
          setLoading(false);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
          setLoading(false);
        });
    });
  }, []);

  return (
    <div className="page">
      <div className="content">
        <h1>Scraped people</h1>
        {loading ? (
          <LoadingDots />
        ) : (
          <ul className="person-list">
            {persons.map(person => (
              <PersonCard key={person.id} person={person} />
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default PersonsPage;
