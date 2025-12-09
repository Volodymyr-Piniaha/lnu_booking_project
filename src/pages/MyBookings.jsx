import { useEffect, useState } from "react";
import "./MyBookings.css";

export default function MyBookings() {
  const [bookings, setBookings] = useState([]);
  const userId = 1; // тут можна замінити на логін користувача

  useEffect(() => {
    fetch(`http://<IP_BACKEND>:8000/api/mybookings/${userId}`)
      .then(res => res.json())
      .then(data => setBookings(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="page">
      <h1>My Bookings</h1>
      {bookings.length === 0 ? <p>No bookings yet.</p> :
        <ul>
          {bookings.map(b => (
            <li key={b.ReservationID}>
              {b.HallName} — {b.ReservationDate} at {b.StartTime} - {b.EndTime}
            </li>
          ))}
        </ul>
      }
    </div>
  );
}
