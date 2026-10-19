import { useState } from "react";
import Login from "./Login";
import Students from "./Students";
import { getToken, clearToken } from "./api";

export default function App() {
  // The user counts as logged in if a token is saved in the browser
  const [loggedIn, setLoggedIn] = useState(!!getToken());

  function logout() {
    clearToken();
    setLoggedIn(false);
  }

  return loggedIn ? (
    <Students onLogout={logout} />
  ) : (
    <Login onLogin={() => setLoggedIn(true)} />
  );
}
