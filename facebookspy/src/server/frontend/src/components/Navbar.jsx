import React, { useState } from "react";
import { IconContext } from "react-icons";
import { Link } from "react-router-dom";
import { SidebarData } from "./SliderbarData";
import "../styles/Navbar.css";

export default function Navbar() {
  const [sidebar, setSidebar] = useState(true);

  const showSidebar = () => setSidebar(true);
  return (
    <>
      <IconContext.Provider value={{ color: "#FFF" }}>
        <nav className={sidebar ? "nav-menu active" : "nav-menu"}>
          <ul className="nav-menu-items" onClick={showSidebar}>
            <li className="navbar-logo">
              <Link to="/" className="navbar-logo-link">
                <h3>Facebook SPY</h3>
              </Link>
            </li>
            {SidebarData.map((item, index) => {
              return (
                <li key={index} className={item.cName}>
                  <Link to={item.path}>
                    {item.icon}
                    <span>{item.title}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      </IconContext.Provider>
    </>
  );
}
