import React, { useState, useEffect } from 'react';
import axios from 'axios';
import NoteCard from './NoteCard';
import ViewNoteModal from '../Account/AccountDetails/components/ViewNoteModal';
import './NotePage.css';

const NotesPage = () => {
  const [notes, setNotes] = useState([]);
  const [selectedNote, setSelectedNote] = useState(null);
  const [showViewNoteModal, setShowViewNoteModal] = useState(false);

  useEffect(() => {
    fetchNotes();
  }, []);

  const fetchNotes = async () => {
    try {
      const response = await axios.get('http://localhost:8000/note/');
      setNotes(response.data);
    } catch (error) {
      console.error('Error fetching notes:', error);
    }
  };

  const openViewNoteModal = (note) => {
    setSelectedNote(note);
    setShowViewNoteModal(true);
  };

  const closeViewNoteModal = () => {
    setSelectedNote(null);
    setShowViewNoteModal(false);
  };

  return (
    <div className="grid-container">
      {notes.map((note) => (
        <NoteCard key={note.id} note={note} onClick={() => openViewNoteModal(note)} />
      ))}

      {showViewNoteModal && (
        <ViewNoteModal
          note={selectedNote}
          onClose={closeViewNoteModal}
        />
      )}
    </div>
  );
};

export default NotesPage;
