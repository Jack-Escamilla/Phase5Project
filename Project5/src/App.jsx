import React, { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./Login.jsx";
import MainPage from "./MainPage";
import Header from "./Header"
import Library from "./Library"


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
      <Header/>
      <Routes>
        <Route path="/" element={<Login onLogin={setUser}/>}/>
        <Route path="/main-page" element={<MainPage/>}/>
        <Route path="/library" element={<Library/>}/>
      </Routes>
    </BrowserRouter>
    </div>
    </>
  )
  }

export default App;
