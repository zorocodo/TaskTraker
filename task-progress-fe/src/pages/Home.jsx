import { useState } from "react";
import TaskCard from "../components/TaskCard";
import FloatingAddButton from "../components/FloatingAddButton";
import AddTaskCard from "../components/AddTaskCard";
import AnimatedBackground from "../components/AnimatedBackground";
import EmptyState from "../components/EmptyState";
import { mockTasks } from "../mock/mockTasks";
import AddTaskMorph from "../components/AddTaskMorph";
import { useTasks } from "../hooks/useTasks";


// export default function Home() {
//   const [tasks, setTasks] = useState(mockTasks);
//   const [showAdd, setShowAdd] = useState(false);

//   const handleSaveTask = (task) => {
//     setTasks((prev) => [...prev, task]);
//   };

//   return (
//     <div className="home">
//       <AnimatedBackground />

//       {tasks.length === 0 ? (
//         <EmptyState onAdd={() => setShowAdd(true)} />
//       ) : (
//         <div className="task-grid">
//           {tasks.map((task) => (
//             <TaskCard key={task.id} task={task} />
//           ))}
//         </div>
//       )}

//       <AddTaskMorph onSave={handleSaveTask} />

//       <AddTaskCard
//         isOpen={showAdd}
//         onClose={() => setShowAdd(false)}
//         onSave={handleSaveTask}
//       />
//     </div>
//   );
// }


export default function Home() {
  const { tasks, createTask, addProgress } = useTasks();
  return (
    <div className="home">
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
