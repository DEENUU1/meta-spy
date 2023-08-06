import React, { useState } from 'react';
import axios from 'axios';
import "../styles/ModalContainer.css";


const UpdateNoteModal = ({ personId, setShowUpdateNoteModal, setNote, note }) => {
  const [content, setContent] = useState(note ? note.content: "");

  const handleUpdateNote = () => {
    axios
      .put(`http://localhost:8000/note/${personId}`, { content })
      .then(response => {
        setNote(response.data);
        setShowUpdateNoteModal(false);
      })
      .catch(error => {
        console.error('Error updating note:', error);
      });
  };

  const handleCloseModal = () => {
    setShowUpdateNoteModal(true);
  };

  return (
    <div className="modal-container">
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
    </div>
  );
};

export default UpdateNoteModal;
