import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";

export default function AddTaskCard({ isOpen, onClose, onSave }) {
  const [form, setForm] = useState({
    title: "",
    description: "",
    target_min: 1,
    target_max: 5,
  });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const errs = {};
    if (!form.title.trim()) errs.title = "Title is required";
    if (!form.description.trim()) errs.description = "Description is required";
    if (form.target_min >= form.target_max)
      errs.range = "Min must be less than Max";
    return errs;
  };

  const handleSave = () => {
    const errs = validate();
    if (Object.keys(errs).length) {
      setErrors(errs);
      return;
    }

    // 🔥 PLACEHOLDER FOR API CALL
    // await api.createTask(form)

    onSave({
      id: Date.now(),
      ...form,
      created_at: new Date().toISOString(),
      progress_entries: [],
    });

    setForm({ title: "", description: "", target_min: 1, target_max: 5 });
    setErrors({});
    onClose();
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ scale: 0, opacity: 0, bottom: 30, right: 30 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0, opacity: 0 }}
          className="add-task-card"
        >
          <h3>Add New Task</h3>

          <input
            placeholder="Title"
            value={form.title}
            onChange={(e) =>
              setForm({ ...form, title: e.target.value })
            }
          />
          {errors.title && <span>{errors.title}</span>}

          <textarea
            placeholder="Description"
            value={form.description}
            onChange={(e) =>
              setForm({ ...form, description: e.target.value })
            }
          />
          {errors.description && <span>{errors.description}</span>}

          <div className="range">
            <input
              type="number"
              value={form.target_min}
              onChange={(e) =>
                setForm({ ...form, target_min: Number(e.target.value) })
              }
            />
            <input
              type="number"
              value={form.target_max}
              onChange={(e) =>
                setForm({ ...form, target_max: Number(e.target.value) })
              }
            />
          </div>
          {errors.range && <span>{errors.range}</span>}

          <div className="actions">
            <button onClick={handleSave}>Save</button>
            <button onClick={onClose}>Cancel</button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
