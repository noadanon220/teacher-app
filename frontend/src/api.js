const API_URL = "http://127.0.0.1:8000";

export const getToken = () => localStorage.getItem("token");
export const setToken = (token) => localStorage.setItem("token", token);
export const clearToken = () => localStorage.removeItem("token");

// Sends a request to the server and adds the token when the user is logged in
export async function request(path, options = {}) {
  const token = getToken();
  const res = await fetch(API_URL + path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });

  const data = await res.json().catch(() => null);

  if (res.status === 401 && token) {
    // Token expired or invalid: log out
    clearToken();
    window.location.reload();
  }

  if (!res.ok) {
    const detail = data && data.detail;
    throw new Error(
      res.status === 401
        ? "Incorrect name or ID number"
        : typeof detail === "string"
        ? detail
        : "The data you entered is not valid"
    );
  }
  return data;
}
