import React, { useState } from "react";
import LoginForm from "./LoginForm";
import SignUpForm from "./SignUpForm";

function Login({ onLogin }) {
    const [showLogin, setShowLogin] = useState(true);
  
    return (
      <div className="Wrapper">
        {showLogin ? (
          <>
            <LoginForm onLogin={onLogin} />
            <hr className="Divider" />
            <p>
              Don't have an account? &nbsp;
              <button onClick={() => setShowLogin(false)}>
                Sign Up
              </button>
            </p>
          </>
        ) : (
          <>
            <SignUpForm onLogin={onLogin} />
            <hr className="Divider" />
            <p>
              Already have an account? &nbsp;
              <button onClick={() => {setShowLogin(true)
            }}>
                Log In
              </button>
            </p>
          </>
        )}
      </div>
    );
  }
  
  export default Login;