import React from 'react';
import './NoteCard.css';

const NoteCard = ({ note, onClick }) => {
  return (
    <div className="note-card" onClick={onClick}>
      <p>{note.content}</p>
    </div>
  );
};

export default NoteCard;
