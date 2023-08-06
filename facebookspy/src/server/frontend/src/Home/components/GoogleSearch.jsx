import React from 'react';

const GoogleSearch = ({ value }) => {
  const handleClick = () => {
    window.location.href = `https://www.google.com/search?q=${value}`;
  };

  return (
    <div>
      <input type="text" value={value} readOnly />
      <button onClick={handleClick}>
        <img src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png" alt="Google" />
      </button>
    </div>
  );
};

export default GoogleSearch;
