import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { TaskAPI } from "../api/tasks.api";
import { useEffect, useState } from "react";

export function useTasks() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    TaskAPI.getTasks()
      .then((res) => setTasks(res.data))
      .catch(() => setTasks([]));
  }, []);

  const extractErrorMessage = (err) => {
    if (!err.response) return "Network error";

    const data = err.response.data;

    if (typeof data === "string") return data;

    if (data.detail) return data.detail;

    // Handle DRF validation errors
    return Object.values(data).flat().join(" ");
  };

  const createTask = async (payload) => {
    const tempId = Date.now();

    const optimisticTask = {
      id: tempId,
      ...payload,
      progress_entries: [
        {
          id: Date.now(),
          progress_value: 0,
          created_at: new Date().toISOString(),
          optimistic: true,
        },
      ],
      optimistic: true,
    };

    setTasks((prev) => [...prev, optimisticTask]);

    try {
      const res = await TaskAPI.createTask(payload);

      setTasks((prev) =>
        prev.map((t) => (t.id === tempId ? res.data : t))
      );
    } catch (err) {
      setTasks((prev) => prev.filter((t) => t.id !== tempId));
      toast.error(extractErrorMessage(err));
    }
  };

  // const addProgress = async (taskId, delta) => {
  //   let tempEntry;

  //   setTasks((prev) =>
  //     prev.map((task) => {
  //       if (task.id !== taskId) return task;

  //       const latest =
  //         task.progress_entries?.length > 0
  //           ? task.progress_entries[task.progress_entries.length - 1]
  //             .progress_value
  //           : 0;

  //       const newValue = latest + delta;

  //       tempEntry = {
  //         id: Date.now(),
  //         progress_value: newValue,
  //         created_at: new Date().toISOString(),
  //         optimistic: true,
  //       };

  //       return {
  //         ...task,
  //         progress_entries: [...task.progress_entries, tempEntry],
  //       };
  //     })
  //   );

  //   try {
  //     const res = await TaskAPI.addProgress({
  //       task: taskId,
  //       progress_value: tempEntry.progress_value,
  //       percentage: tempEntry.progress_value,
  //     });

  //     setTasks((prev) =>
  //       prev.map((task) =>
  //         task.id === taskId
  //           ? {
  //             ...task,
  //             progress_entries: task.progress_entries.map((p) =>
  //               p.id === tempEntry.id ? res.data : p
  //             ),
  //           }
  //           : task
  //       )
  //     );
  //   } catch (err) {
  //     setTasks((prev) =>
  //       prev.map((task) =>
  //         task.id === taskId
  //           ? {
  //             ...task,
  //             progress_entries: task.progress_entries.filter(
  //               (p) => p.id !== tempEntry.id
  //             ),
  //           }
  //           : task
  //       )
  //     );
  //     toast.error(extractErrorMessage(err));
  //   }
  // };

  const addProgress = async (taskId, delta) => {
    // Step 1: generate a unique temp entry
    const tempEntry = {
      id: Date.now(),
      progress_value: null, // we will calculate
      created_at: new Date().toISOString(),
      optimistic: true,
    };

    // Step 2: update task with optimistic entry
    setTasks((prev) =>
      prev.map((task) => {
        if (task.id !== taskId) return task;

        const latest =
          task.progress_entries?.length > 0
            ? task.progress_entries[task.progress_entries.length - 1].progress_value
            : 0;

        const newValue = latest + delta;

        tempEntry.progress_value = newValue; // set value for optimistic entry

        return {
          ...task,
          progress_entries: [...task.progress_entries, tempEntry],
        };
      })
    );

    try {
      // Step 3: call API
      const res = await TaskAPI.addProgress({
        task: taskId,
        progress_value: tempEntry.progress_value,
        percentage: tempEntry.progress_value,
      });

      // Step 4: replace the optimistic entry with actual API response
      setTasks((prev) =>
        prev.map((task) =>
          task.id === taskId
            ? {
              ...task,
              progress_entries: task.progress_entries.map((p) =>
                p.id === tempEntry.id ? res.data : p
              ),
            }
            : task
        )
      );
    } catch (err) {
      // Step 5: rollback on error
      setTasks((prev) =>
        prev.map((task) =>
          task.id === taskId
            ? {
              ...task,
              progress_entries: task.progress_entries.filter(
                (p) => p.id !== tempEntry.id
              ),
            }
            : task
        )
      );

      // Show backend error
      const errorMessage =
        err.response?.data?.detail ||
        JSON.stringify(err.response?.data) ||
        "Something went wrong";
      toast.error(errorMessage);
    }
  };
  return {
    tasks,
    createTask,
    addProgress,
  };
}