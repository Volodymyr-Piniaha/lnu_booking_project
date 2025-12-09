import { useParams, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "./HallSchedule.css";

export default function HallSchedule() {
  const { hallId } = useParams();
  const [schedule, setSchedule] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  const date = searchParams.get("date") || new Date().toISOString().split("T")[0];

  useEffect(() => {
    fetch(`http://<IP_BACKEND>:8000/api/schedule/${hallId}?date=${date}`)
      .then(res => res.json())
      .then(data => {
        setSchedule(data);
        setLoading(false);
      })
      .catch(err => console.error(err));
  }, [hallId, date]);

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
          {schedule.map(slot => (
            <tr key={slot.TimeSlotID}>
              <td>{slot.SlotName} ({slot.StartTime} - {slot.EndTime})</td>
              <td>{slot.UserFullName || "-"}</td>
              <td>
                {slot.UserFullName
                  ? "Booked"
                  : <button onClick={() => alert(`Book slot ${slot.TimeSlotID}`)}>Book</button>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
