import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import HomePage from './components/HomePage';
import DetailPage from './components/DetailPage';
// import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <div className="content-container">
          <Route path="/" exact component={HomePage} />
          <Route path="/about" component={DetailPage} />
        </div>
      </div>
    </Router>
  );
}

export default App;
