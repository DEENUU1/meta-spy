import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './Account/Home/pages/HomePage';
import PersonDetail from './Account/AccountDetails/pages/PersonDetail';
import PersonsPage from './Account/AccountList/pages/PersonsPage';
import Navbar from "./Account/Home/components/Navbar";
import PersonVideoReel from './Account/AccountDetails/pages/PersonVideoReel';
import PersonImage from './Account/AccountDetails/pages/PersonImage';
import PersonFriendList from './Account/AccountDetails/pages/PersonFriendList';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navbar/>
        <div className="content-container">
        <Routes>  
          <Route element={<HomePage/>} path="/"/>
          <Route element={<PersonDetail/>} path="/person/:id"/>
          <Route element={<PersonsPage/>} path="/person/"/>
          <Route element={<PersonVideoReel/>} path="/person/:id/video"/>
          <Route element={<PersonImage/>} path="/person/:id/image"/>
          <Route element={<PersonFriendList/>} path="/person/:id/friend"/>
          
        </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
