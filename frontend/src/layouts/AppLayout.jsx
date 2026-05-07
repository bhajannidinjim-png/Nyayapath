import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar.jsx";
import TopHeader from "../components/TopHeader.jsx";

export default function AppLayout() {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-panel">
        <TopHeader />
        <div className="page-container">
          <Outlet />
        </div>
      </main>
    </div>
  );
}

