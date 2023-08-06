import React, { useState } from 'react';
import axios from 'axios';

const UpdateNoteModal = ({ note, setShowUpdateNoteModal, setNote }) => {
  const [content, setContent] = useState(note.content);

  const handleUpdateNote = () => {
    axios
      .put(`http://localhost:8000/note/${note.id}`, { content })
      .then(response => {
        setNote(response.data);
        setShowUpdateNoteModal(false);
      })
      .catch(error => {
        console.error('Error updating note:', error);
      });
  };

  const handleCloseModal = () => {
    setShowUpdateNoteModal(false);
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <h2>Update Note</h2>
        <textarea
          value={content}
          onChange={event => setContent(event.target.value)}
        />
        <div className="modal-buttons">
          <button onClick={handleUpdateNote}>Update</button>
          <button onClick={handleCloseModal}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default UpdateNoteModal;
