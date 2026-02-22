import api from "./axios";

export const TaskAPI = {
  getTasks: () => api.get("/tasks/"),

  createTask: (payload) =>
    api.post("/tasks/create/", payload),

  updateTaskTitle: (id, title) =>
    api.put(`/tasks/${id}/title/`, { title }),

  updateTaskDescription: (id, description) =>
    api.put(`/tasks/${id}/description/`, { description }),

  updateTargetMin: (id, target_min) =>
    api.put(`/tasks/${id}/target-min/`, { target_min }),

  updateTargetMax: (id, target_max) =>
    api.put(`/tasks/${id}/target-max/`, { target_max }),

  updateStatus: (id, status) =>
    api.put(`/tasks/${id}/status/`, { status }),

  addProgress: (payload) =>
    api.post("/progress/set-value/", payload),
};
