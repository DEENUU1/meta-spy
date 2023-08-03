import React from 'react';
import Sidebar from './Sidebar';
// import './Page.css';

const PersonDetail = () => {
  return (
    <div className="page">
      <Sidebar />
      <div className="content">
        <h1>Person detail</h1>
      </div>
    </div>
  );
};

export default PersonDetail;
