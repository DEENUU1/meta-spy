import React, { useState } from 'react';
import axios from 'axios';

const CreateNoteModal = ({ personId, setShowCreateNoteModal, setNote }) => {
  const [content, setContent] = useState('');

  const handleCreateNote = () => {
    axios
      .post(`http://localhost:8000/note/${personId}`, { content })
      .then(response => {
        setNote(response.data);
        setShowCreateNoteModal(false);
      })
      .catch(error => {
        console.error('Error creating note:', error);
      });
  };

  const handleCloseModal = () => {
    setShowCreateNoteModal(false);
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <h2>Create Note</h2>
        <textarea
          value={content}
          onChange={event => setContent(event.target.value)}
        />
        <div className="modal-buttons">
          <button onClick={handleCreateNote}>Create</button>
          <button onClick={handleCloseModal}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default CreateNoteModal;
