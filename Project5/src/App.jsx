import React, { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "Login";
import MainPage from "MainPage";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
   
    fetch("/check_session").then((r) => {
      if (r.ok) {
        r.json().then((user) => setUser(user));
      }
    });
  }, []);

  return (
    <>
    <div>
     
  
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login onLogin={setUser}/>}/>
        <Route path="/main-page" element={<MainPage/>}/>
      </Routes>
    </BrowserRouter>
    </div>
    </>
  )
  }

export default App;
