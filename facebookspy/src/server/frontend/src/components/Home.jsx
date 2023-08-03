import React from 'react';
import Sidebar from './Sidebar';
// import './Page.css'; 

const HomePage = () => {
  return (
    <div className="page">
      <Sidebar />
      <div className="content">
        <h1>Home</h1>
      </div>
    </div>
  );
};

export default HomePage;
