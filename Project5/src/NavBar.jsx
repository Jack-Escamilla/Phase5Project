import React from "react";
import { useNavigate,Link } from "react-router-dom";

function NavBar({ user, setUser }) {
const navigate = useNavigate()

function handleLogoutClick () {
    fetch("/logout", { method: "DELETE" }).then((r) => {
      if (r.ok) {
        setUser(null);
      }
    });
  }

  return (
    <nav className="Navbar">
      <div>
        <Link to="/">Logout</Link>
      </div>
      <div>
        {user && (
          <button className="Logout" onClick={handleLogoutClick}>
            Logout
          </button>
        )}
        <button onClick={() => navigate("/main-page")}>Home</button>
        <button onClick={() => navigate("/library")}>Library</button>  
      </div>
    </nav>
  );
}

export default NavBar;





// import React from 'react';
// import MainPage from './MainPage'
// import Library from './Library'
// import Login from './Login'
// import { useNavigate, Router } from 'react-router-dom';


// function NavBar() {
// const navigate = useNavigate()

// const handleLogoutClick = () => {
//         fetch("/logout", { method: "DELETE" }).then((r) => {
//           if (r.ok) {
//             setUser(null);
//           }
//         });
//       }
//   return (
//     <Router>
//     <nav>
//         <button onClick={() => navigate("/main-page")}>Home</button>
//         <button variant="outline" onClick={handleLogoutClick}>Logout</button>
//         <button onClick={() => navigate("/library")}>Library</button>     
//     </nav>
//     </Router>
//   );
  
// }

// export default NavBar;
{/* <div>
        <Link to="/">Logout</Link>
      </div>
      <div>
        {user && (
          <button className="Logout" onClick={handleLogoutClick}>
            Logout
          </button>
        )}

export default NavBar; */}


// import React from 'react';
// import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
// import NavBar from './NavBar';
// import MainPage from './MainPage';
// import LoginPage from './LoginPage';
// import LibraryPage from './LibraryPage';

// function App() {
//   return (
//     <Router>
//       <div className="App">
//         <NavBar />
//         <Switch>
//           <Route path="/main-page" component={MainPage} />
//           <Route path="/login" component={LoginPage} />
//           <Route path="/library" component={LibraryPage} />
//           {/* Other routes */}
//         </Switch>
//       </div>
//     </Router>
//   );
// }

// export default App;

