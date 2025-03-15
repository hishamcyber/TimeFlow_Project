import { useState } from "react";

function App() {
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Send password to backend
    const response = await fetch("http://127.0.0.1:5000/verify-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });

    const data = await response.json();
    setMessage(data.message); // Show success or error message
  };

  return (
    <div>
      <h1>Password Verification</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          placeholder="Enter password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Submit</button>
      </form>
      <p>{message}</p>
    </div>
  );
}

export default App;
