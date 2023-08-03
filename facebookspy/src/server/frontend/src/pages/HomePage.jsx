import React from "react";
import { Link } from "react-router-dom";
import "../styles/HomePage.css";
import illustration from "/public/home.png/";
// import Navbar from "../components/Navbar";

export default function Home() {
  return (
    <div className="page">
      {/* <Navbar /> */}

      <div className="main-content">
        <div className="content">
          <h1 className="content-heading">Welcome to Facebook SPY</h1>
          <p className="content-text">
            Explore the secrets of social media monitoring.
          </p>
          <div className="links">
            <Link to="https://github.com/DEENUU1/" className="home-links">
              GitHub
            </Link>
            <Link to="https://github.com/DEENUU1/facebook-spy/blob/main/README.md" className="home-links">
              Docs
            </Link>
            <Link to="https://www.linkedin.com/in/kacper-wlodarczyk/" className="home-links">
              LinkedIn
            </Link>
          </div>
        </div>
        <div className="image-container">
          <img src={illustration} alt="Illustration" />
        </div>
      </div>
    </div>
  );
}
