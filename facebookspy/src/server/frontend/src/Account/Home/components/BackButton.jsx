import React from 'react';
import { useHistory } from 'react-router-dom';

const BackButton = () => {
  const history = useHistory();

  const handleGoBack = () => {
    history.goBack();
  };

  return (
    <div className="back-button">
      <button onClick={handleGoBack}>Powrót</button>
    </div>
  );
};

export default BackButton;
