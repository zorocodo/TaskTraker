import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";

export default function AddTaskMorph({ onSave }) {
  const [open, setOpen] = useState(false);
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

  const handleSave = async () => {
    const errs = validate();
    if (Object.keys(errs).length) {
      setErrors(errs);
      return;
    }

    try {
      await onSave(form);
      setOpen(false);
    } catch {
      alert("Failed to save task");
    }
  };


  return (
    <motion.div
      layout
      className={`morph-container ${open ? "open" : ""}`}
      onClick={!open ? () => setOpen(true) : undefined}
    >
      <AnimatePresence mode="wait">
        {!open ? (
          <motion.button
            key="btn"
            layout
            className="floating-btn"
            initial={{ scale: 1 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0 }}
          >
            +
          </motion.button>
        ) : (
          <motion.div
            key="card"
            layout
            className="add-task-card"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <h3>Add Task</h3>

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
                  setForm({ ...form, target_min: +e.target.value })
                }
              />
              <input
                type="number"
                value={form.target_max}
                onChange={(e) =>
                  setForm({ ...form, target_max: +e.target.value })
                }
              />
            </div>
            {errors.range && <span>{errors.range}</span>}

            <div className="actions">
              <button onClick={handleSave}>Save</button>
              <button onClick={() => setOpen(false)}>Cancel</button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
