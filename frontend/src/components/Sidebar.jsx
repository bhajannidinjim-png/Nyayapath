import { CheckCircle2, FileCheck2, LayoutDashboard, Scale, Upload, UserCheck } from "lucide-react";
import { NavLink } from "react-router-dom";

const items = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/upload", label: "Upload Judgment", icon: Upload },
  { to: "/verify", label: "Human Verification", icon: UserCheck },
  { to: "/approved", label: "Approved Actions", icon: CheckCircle2 }
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark"><Scale size={22} /></div>
        <div>
          <strong>NyayPath</strong>
          <span>AI for Bharat</span>
        </div>
      </div>
      <nav>
        {items.map(({ to, label, icon: Icon }) => (
          <NavLink key={to} to={to} className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}>
            <Icon size={18} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="sidebar-note">
        <FileCheck2 size={18} />
        <span>Only human-approved records are published.</span>
      </div>
    </aside>
  );
}

