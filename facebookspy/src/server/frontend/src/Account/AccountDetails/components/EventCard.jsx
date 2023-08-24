import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../../Home/components/Loading';

const EventCard = ({ personId }) => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    axios.get(`http://localhost:8000/event/${personId}`)
      .then(response => {
        setEvents(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [personId]);

  
  return (
      <div className="event-card">
      <h2>Events</h2>
      
      {loading ? (
        <LoadingDots />
      ) : (
        <ul className="evnet-grid">
          {(searchTerm ? searchResults : events).map(item => (
            <li className="event-card" key={item.id}> 
              <strong>{item.name}</strong> <br />
              <a href={item.url}>Facebook link</a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default EventCard;
