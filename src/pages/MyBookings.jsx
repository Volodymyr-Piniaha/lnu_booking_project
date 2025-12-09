import "./MyBookings.css";

export default function MyBookings() {

  // Mocked data
  const bookings = [
    { id: 1, hall: "Main Hall", date: "2025-01-10", time: "10:00" },
    { id: 2, hall: "Gym #1", date: "2025-01-12", time: "14:00" }
  ];

  return (
    <div className="page">
      <h1>My Bookings</h1>

      <ul>
        {bookings.map((b) => (
          <li key={b.id}>
            {b.hall} — {b.date} at {b.time}
          </li>
        ))}
      </ul>
    </div>
  );
}
