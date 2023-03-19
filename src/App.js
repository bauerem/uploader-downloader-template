import  { Routes, Route, Link } from "react-router-dom";
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
