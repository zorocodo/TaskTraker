import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function ProgressChart({ data }) {
  if (!data || data.length === 0) {
    return <p className="empty-chart">No progress yet</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={200}>
      <LineChart data={data}>
        <XAxis
          dataKey="x"
          tickFormatter={(value) =>
            new Date(value).toLocaleDateString()
          }
        />
        <YAxis allowDecimals={false} />
        <Tooltip
          labelFormatter={(value) =>
            new Date(value).toLocaleString()
          }
        />
        <Line
          type="monotone"
          dataKey="y"
          stroke="#4f46e5"
          strokeWidth={2}
          dot
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
