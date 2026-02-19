import { TaskAPI } from "../api/tasks.api";
import { useEffect, useState } from "react";

export function useTasks() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    TaskAPI.getTasks()
      .then((res) => setTasks(res.data))
      .catch(() => setTasks([]));
  }, []);

  const createTask = async (payload) => {
    const tempId = Date.now();

    const optimisticTask = {
      id: tempId,
      ...payload,
      progress_history: [],
      optimistic: true,
    };

    setTasks((prev) => [...prev, optimisticTask]);

    const res = await TaskAPI.createTask(payload);

    setTasks((prev) =>
      prev.map((t) => (t.id === tempId ? res.data : t))
    );
  };

  // 🔥 NEW — Optimistic Progress
  const addProgress = async (taskId, value) => {
    const tempEntry = {
      id: Date.now(),
      progress_value: value,
      created_at: new Date().toISOString(),
      optimistic: true,
    };

    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId
          ? {
              ...task,
              progress_history: [
                ...(task.progress_history || []),
                tempEntry,
              ],
            }
          : task
      )
    );

    try {
      const res = await TaskAPI.addProgress({
        task: taskId,
        progress_value: value,
      });

      setTasks((prev) =>
        prev.map((task) =>
          task.id === taskId
            ? {
                ...task,
                progress_history: task.progress_history.map((p) =>
                  p.id === tempEntry.id ? res.data : p
                ),
              }
            : task
        )
      );
    } catch (err) {
      // rollback
      setTasks((prev) =>
        prev.map((task) =>
          task.id === taskId
            ? {
                ...task,
                progress_history: task.progress_history.filter(
                  (p) => p.id !== tempEntry.id
                ),
              }
            : task
        )
      );
    }
  };

  return {
    tasks,
    createTask,
    addProgress,
  };
}
