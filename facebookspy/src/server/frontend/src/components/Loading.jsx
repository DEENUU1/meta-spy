import React, { useState, useEffect } from 'react';

const LoadingDots = () => {
  const [dots, setDots] = useState('');

  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prevDots => (prevDots.length === 3 ? '' : prevDots + '.'));
    }, 500);

    return () => {
      clearInterval(interval);
    };
  }, []);

  return <div className="loading">Loading{dots}</div>;
};

export default LoadingDots;
