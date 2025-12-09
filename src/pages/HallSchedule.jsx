import { useParams } from "react-router-dom";

export default function HallSchedule() {
  const { hallId } = useParams();

  return (
    <div className="page">
      <h1>Schedule for Hall #{hallId}</h1>

      <p>Here will be schedule grid and booking buttons.</p>
    </div>
  );
}
