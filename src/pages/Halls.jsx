import { Link } from "react-router-dom";
import "./Halls.css";

export default function Halls() {
  const halls = [
    { id: 1, name: "Main Sports Hall" },
    { id: 2, name: "Gym #1" },
    { id: 3, name: "Aerobic Room" }
  ];

  return (
    <div className="page">
      <h1>Available Halls</h1>

      <ul className="halls-list">
        {halls.map((h) => (
          <li key={h.id} className="hall-card">
            <Link to={`/schedule/${h.id}`} className="hall-link">
              {h.name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
