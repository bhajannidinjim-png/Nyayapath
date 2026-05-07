import { useState } from "react";
import { ChevronDown } from "lucide-react";

export default function EvidenceAccordion({ sourceText, reason, pageReference }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="accordion">
      <button onClick={() => setOpen((value) => !value)} className="accordion-trigger">
        <span>Source evidence {pageReference ? `- page ${pageReference}` : ""}</span>
        <ChevronDown size={18} className={open ? "rotate" : ""} />
      </button>
      {open && (
        <div className="accordion-body">
          <p>{sourceText}</p>
          {reason && <small>{reason}</small>}
        </div>
      )}
    </div>
  );
}

