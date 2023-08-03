import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import HomePage from './components/Home';
import PersonDetail from './components/PersonDetail';
// import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <div className="content-container">
        <Routes>  
          <Route element={<HomePage/>} path="/"/>
          <Route element={<PersonDetail/>} path="/detail"/>
        </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
