import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

export default function ProgressChart({ data }) {
  return (
    <LineChart width={250} height={180} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="progress_value" stroke="#8884d8" />
    </LineChart>
  );
}
