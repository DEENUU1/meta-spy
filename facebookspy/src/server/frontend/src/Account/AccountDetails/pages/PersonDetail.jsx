import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom'; 
import axios from 'axios';
import '../styles/PersonDetail.css';
import LoadingDots from '../../../Home/components/Loading';
import ReviewsCard from '../components/ReviewsCard';
import WorkAndEducationCard from '../components/WorkAndEducationCard';
import FamilyMemberCard from '../components/FamilyMemberCard';
import PlacesCard from '../components/PlacesCard';
import CreateNoteModal from '../components/CreateNoteModal';
import ViewNoteModal from '../components/ViewNoteModal';
import UpdateNoteModal from '../components/UpdateNoteModal';

const PersonDetail = () => {
  const { id } = useParams();
  const [person, setPerson] = useState({});
  const [loading, setLoading] = useState(true);
  const [note, setNote] = useState(null);
  const [showCreateNoteModal, setShowCreateNoteModal] = useState(false);
  const [showViewNoteModal, setShowViewNoteModal] = useState(false);
  const [showUpdateNoteModal, setShowUpdateNoteModal] = useState(false);
  const [noteExists, setNoteExists] = useState(false);

  useEffect(() => {
    axios
      .get(`http://localhost:8000/person/${id}`)
      .then(response => {
        setPerson(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, [id]);

  useEffect(() => {
    axios
      .get(`http://localhost:8000/person/note/${id}`)
      .then(response => {
        setNote(response.data);
        setNoteExists(true); 
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setNoteExists(false);
      });
  }, [id]);

  const handleCreateNote = () => {
    setShowCreateNoteModal(true);
  };

  const handleViewNote = () => {
    setShowViewNoteModal(true);
  };

  const handleUpdateNote = () => {
    setShowUpdateNoteModal(true);
  };

  return (
    <div className="pagex">
      <div className="content">
        {loading ? (
          <LoadingDots />
        ) : (
          <div className="person-details">
            <h1>{person.facebook_id} details</h1>
            <div className="detail-item">
              {person.full_name}
              {noteExists ? ( 
                <button onClick={handleViewNote}>View Note</button>
              ) : (
                <button onClick={handleCreateNote}>Create Note</button>
              )}
              <Link to={`/person/${id}/video`}>Videos & Reels</Link> <br/>
              <Link to={`/person/${id}/image`}>Images</Link> <br/>
              <Link to={`/person/${id}/friend`}>Friends</Link> <br/>
              <Link to={`/person/${id}/place`}>Recent Places</Link> <br/>
              <Link to={`/person/${id}/post`}>Posts</Link> <br/>
            </div>

            <div className='card-container'>
              <FamilyMemberCard personId={id} />
              <WorkAndEducationCard personId={id} />
              <PlacesCard personId={id} />
              <ReviewsCard personId={id} />
            </div>
          </div>
        )}
      </div>
      {showCreateNoteModal && (
        <CreateNoteModal
          personId={id}
          setShowCreateNoteModal={setShowCreateNoteModal}
          setNote={setNote}
        />
      )}
      {showViewNoteModal && (
        <ViewNoteModal
          note={note}
          setShowViewNoteModal={setShowViewNoteModal}
          setShowUpdateNoteModal={setShowUpdateNoteModal}
        />
      )}
      {showUpdateNoteModal && (
        <UpdateNoteModal
          personId={id}
          setShowUpdateNoteModal={setShowUpdateNoteModal}
          setNote={setNote}
          note={note}
        />
      )}
    </div>
  );
};

export default PersonDetail;
