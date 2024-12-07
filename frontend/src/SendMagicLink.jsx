import React, {useState} from "react";
import axios from "axios";

const SendMagicLinkForm = () => {
    const [email, setEmail] = useState("");
    const [status, setStatus] = useState(null);
    const [error, setError] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setStatus(null);
        setError(null);

        try {
            const response = await axios.post("http://localhost:8000/auth/send_magic_link/", {
                email,
            });
            setStatus(response.data.message);
        } catch (err) {
            setError(err.response?.data?.detail || "Hyi");
        }
    };

    return (
        <div>
        <h2>Auth:</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="yourname@edu.hse.ru"
              required
            />
          </div>
          <button type="submit">Send Magic Link</button>
        </form>
        {status && <p style={{ color: "green" }}>{status}</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}
      </div>
    );
  };
  
export default SendMagicLinkForm;