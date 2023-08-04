import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from './Loading';

const ReviewsCard = ({ personId }) => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/review/${personId}`)
      .then(response => {
        setReviews(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [personId]);

  return (
    <div className="card">
      <h2>Reviews</h2>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul>
          {reviews.map(review => (
            <li key={review.id}>
              <strong>Company:</strong> {review.company}<br />
              <strong>Review:</strong> {review.review}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ReviewsCard;
