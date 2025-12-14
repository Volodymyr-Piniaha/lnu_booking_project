import { useParams, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "./HallSchedule.css";

export default function HallSchedule() {
  const { hallId } = useParams();
  const [timeslots, setTimeslots] = useState([]);
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  const date = searchParams.get("date") || new Date().toISOString().split("T")[0];

  // Завантажуємо тайм-слоти і бронювання
  const fetchData = async () => {
    setLoading(true);
    try {
      // 1. Отримуємо всі тайм-слоти
      const tsRes = await fetch("http://localhost:8000/api/timeslots/");
      const tsData = await tsRes.json();
      setTimeslots(tsData);

      // 2. Отримуємо бронювання для конкретного залу та дати
      const resRes = await fetch(`http://localhost:8000/api/reservations/?hall=${hallId}&reservation_date=${date}`);
      const resData = await resRes.json();
      setReservations(resData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [hallId, date]);

  // Бронювання слоту
  const bookSlot = async (slotId) => {
    try {
      const res = await fetch("http://localhost:8000/api/reservations/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          hall: hallId,
          timeslot: slotId,
          reservation_date: date
        })
      });

      if (!res.ok) {
        const errData = await res.json();
        alert("Error booking slot: " + JSON.stringify(errData));
        return;
      }

      const data = await res.json();
      alert("Booking successful!");
      // Додаємо нове бронювання в стан
      setReservations(prev => [...prev, data]);
    } catch (err) {
      console.error(err);
      alert("Error booking slot");
    }
  };

  if (loading) return <div className="page"><p>Loading schedule...</p></div>;

  return (
    <div className="page">
      <h1>Schedule for Hall #{hallId} on {date}</h1>
      <table className="schedule-table">
        <thead>
          <tr>
            <th>Time Slot</th>
            <th>Reserved By</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {timeslots.map(slot => {
            // Шукаємо бронювання для цього слоту
            const reservation = reservations.find(r => r.timeslot === slot.id && r.status === "confirmed");

            // Визначаємо відображуване ім’я
            let reservedBy = "-";
            if (reservation) {
              reservedBy = reservation.user_full_name || reservation.user || "Booked";
            }

            return (
              <tr key={slot.id}>
                <td>{slot.slot_name} ({slot.start_time} - {slot.end_time})</td>
                <td>{reservedBy}</td>
                <td>
                  {reservation
                    ? "Booked"
                    : <button onClick={() => bookSlot(slot.id)}>Book</button>
                  }
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
