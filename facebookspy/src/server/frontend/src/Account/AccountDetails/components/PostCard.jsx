import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingDots from '../../../Home/components/Loading';

const PostCard = ({ personId }) => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/person/post/${personId}`)
      .then(response => {
        setPosts(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [personId]);

  return (
    <div className="card places-card">
      <h2>Posts</h2>
      {loading ? (
        <LoadingDots />
      ) : (
        <ul>
          {posts.map(item => (
            <li key={item.id}>
              <a href={item.url}>Url</a>  
              <p>{item.content}</p>
              <strong>Likes {item.number_of_likes}</strong>
              <strong>Shares {item.number_of_shares}</strong>
              <strong>Comments {item.number_of_comments}</strong>
              <strong>Source {item.source}</strong>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default PostCard;
