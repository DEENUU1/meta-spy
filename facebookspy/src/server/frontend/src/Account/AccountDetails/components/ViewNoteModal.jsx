import React from 'react';
import "../styles/ModalContainer.css";


const ViewNoteModal = ({ note, setShowViewNoteModal, setShowUpdateNoteModal }) => {
  const handleCloseModal = () => {
    setShowViewNoteModal(false);
  };

  const handleUpdateNote = () => {
    setShowViewNoteModal(false);
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
            <button onClick={handleCloseModal}>Close</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ViewNoteModal;
