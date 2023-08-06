import React from 'react';
import { FaGoogle } from 'react-icons/fa';

const GoogleSearch = ({ value }) => {
  const handleClick = () => {
    window.location.href = `https://www.google.com/search?q=${value}`;
  };

  return (
    <div>
      <button onClick={handleClick}>
        <FaGoogle />
        Search in google
      </button>
    </div>
  );
};

export default GoogleSearch;
