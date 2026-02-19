import { useState } from "react";
import { motion } from "framer-motion";
import ProgressChart from "./ProgressChart";

export default function TaskCard({ task, onAddProgress }) {
  const [value, setValue] = useState("");
  const chartData = task.progress_entries.map((entry) => ({
    x: new Date(entry.created_at),
    y: entry.progress_value,
  }));
  return (
    <div className="task-card">
      <h3>{task.title}</h3>

      <ProgressChart data={chartData} />

      <div className="progress-controls">
        <motion.button
          whileTap={{ scale: 0.8 }}
          onClick={() => onAddProgress(task.id, 1)}
        >
          ⬆️
        </motion.button>

        <motion.button
          whileTap={{ scale: 0.8 }}
          onClick={() => onAddProgress(task.id, -1)}
        >
          ⬇️
        </motion.button>
      </div>

      <div className="manual-input">
        <input
          type="number"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Today's Progress"
        />
        <motion.button
          whileHover={{ scale: 1.1 }}
          onClick={() => {
            onAddProgress(task.id, Number(value));
            setValue("");
          }}
        >
          Submit 🎉
        </motion.button>
      </div>
    </div>
  );
}