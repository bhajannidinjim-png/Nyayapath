const steps = ["Upload", "Extract", "Review", "Verify", "Publish"];

export default function WorkflowTracker({ current = 1 }) {
  return (
    <div className="workflow">
      {steps.map((step, index) => (
        <div key={step} className={`workflow-step ${index + 1 <= current ? "done" : ""}`}>
          <span>{index + 1}</span>
          <p>{step}</p>
        </div>
      ))}
    </div>
  );
}

