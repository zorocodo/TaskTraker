import { useState } from "react";
import TaskCard from "../components/TaskCard";
import FloatingAddButton from "../components/FloatingAddButton";
import AddTaskCard from "../components/AddTaskCard";
import AnimatedBackground from "../components/AnimatedBackground";
import EmptyState from "../components/EmptyState";
import { mockTasks } from "../mock/mockTasks";
import AddTaskMorph from "../components/AddTaskMorph";
import { useTasks } from "../hooks/useTasks";


export default function Home() {
  const { tasks, createTask, addProgress } = useTasks();
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.href = "/login";
  };
  return (
    <div className="home">
      <button onClick={handleLogout}>Logout</button>
      
      <div className="task-grid">
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onAddProgress={addProgress}
          />
        ))}
      </div>

      <AddTaskMorph onSave={createTask} />
    </div>
  );
}
