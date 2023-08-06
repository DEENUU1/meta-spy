import React from 'react';
import './ModalContainer.css';

const ViewNoteModal = ({ note, onClose, setShowUpdateNoteModal }) => { 
  const handleUpdateNote = () => {
    onClose();
    setShowUpdateNoteModal(true);
  };

  return (
    <div className="modal-container">
      <div className="modal">
        <div className="modal-content">
          <h2>Note</h2>
          <p>{note.content}</p>
          <div className="modal-buttons">
            <button onClick={handleUpdateNote}>Update</button>
            <button onClick={onClose}>Close</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ViewNoteModal;
