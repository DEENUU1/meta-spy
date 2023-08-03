import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import PersonDetail from './pages/PersonDetail';
import PersonsPage from './pages/PersonsPage';

function App() {
  return (
    <Router>
      <div className="app-container">
        <div className="content-container">
        <Routes>  
          <Route element={<HomePage/>} path="/"/>
          <Route element={<PersonDetail/>} path="/detail"/>
          <Route element={<PersonsPage/>} path="/persons"/>
        </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
