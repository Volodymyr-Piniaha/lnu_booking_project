import { Link } from "react-router-dom";
import "./Halls.css";

export default function Halls() {
  // Mock data before backend
  const halls = [
    { id: 1, name: "Main Sports Hall" },
    { id: 2, name: "Gym #1" },
    { id: 3, name: "Aerobic Room" }
  ];

  return (
    <div className="page">
      <h1>Available Halls</h1>

      <ul className="hall-list">
        {halls.map((h) => (
          <li key={h.id}>
            <Link className="hall-item" to={`/schedule/${h.id}`}>
              {h.name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
