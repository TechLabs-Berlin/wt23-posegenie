import "./modal.css";
function Modal({ isOpen, onClose }) {
  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Modal Window</h2>
          <button onClick={onClose}>Close</button>
        </div>
        <div className="modal-body">
          <p>It's a modal window.</p>
        </div>
      </div>
    </div>
  );
}

export default Modal;
