import { Link } from "react-router-dom";
import "./Halls.css";
import { useEffect, useState } from "react";

export default function Halls() {
  const [halls, setHalls] = useState([]);

  useEffect(() => {
    fetch("http://<IP_BACKEND>:8000/api/halls/")
      .then(res => res.json())
      .then(data => setHalls(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="page">
      <h1>Available Halls</h1>
      <ul className="hall-list">
        {halls.map(h => (
          <li key={h.HallID}>
            <Link className="hall-item" to={`/schedule/${h.HallID}`}>
              {h.Name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
