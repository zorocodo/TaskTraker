export default function EmptyState({ onAdd }) {
  return (
    <div className="empty-container">
      <button className="main-add-btn" onClick={onAdd}>
        Create Your First Task 🚀
      </button>
    </div>
  );
}
