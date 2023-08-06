import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/PersonsPage.css';
import LoadingDots from '../../Home/components/Loading';
import PersonCard from '../components/PersonCard';

const PersonsPage = () => {
  const [persons, setPersons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);

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

  useEffect(() => {
    if (searchTerm) {
      axios.get(`http://127.0.0.1:8000/person/search/?search_term=${searchTerm}`)
        .then(response => {
          setSearchResults(response.data);
        })
        .catch(error => {
          console.error('Error searching persons:', error);
        });
    } else {
      setSearchResults([]);
    }
  }, [searchTerm]);

  return (
    <div className="page">
      <div className="content">
        <h1>Scraped people</h1>
        <div className="search-form">
          <input
            type="text"
            placeholder="Search persons..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
          />
        </div>
        {loading ? (
          <LoadingDots />
        ) : (
          <ul className="person-list">
            {(searchTerm ? searchResults : persons).map(person => (
              <PersonCard key={person.id} person={person} />
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default PersonsPage;
