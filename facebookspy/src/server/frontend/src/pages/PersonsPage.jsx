import React from 'react';
import Navbar from '../components/Navbar';

const PersonsPage = () => {
  return (
    <div className="page">
      <Navbar />
      <div className="content">
        <h1>Scraped persons</h1>
      </div>
    </div>
  );
};

export default PersonsPage;
