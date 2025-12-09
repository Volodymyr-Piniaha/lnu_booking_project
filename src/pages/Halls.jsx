import { Link } from "react-router-dom";

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

      <ul>
        {halls.map((h) => (
          <li key={h.id}>
            <Link to={`/schedule/${h.id}`}>{h.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
