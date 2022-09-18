import  { Routes, Route, Link } from "react-router-dom";
import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

import { Home } from "./pages/Home";
import { Time } from "./pages/Time";
import { NotFound } from "./pages/NotFound";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <>
        <div>
        <Link className="App-Link" to="/">Home</Link> | <Link className="App-Link" to="/time">Time</Link>
        </div>
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <Routes>
          <Route path='*' element={<NotFound />} />
          <Route path='/' element={<Home />} />
          <Route path='/time' element={<Time />} />
        </Routes>
        </>
      </header>
    </div>
  );
}

export default App;
