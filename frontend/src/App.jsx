import { Navigate, Route, Routes } from "react-router-dom";
import AppLayout from "./layouts/AppLayout.jsx";
import ApprovedActions from "./pages/ApprovedActions.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import ActionDetails from "./pages/ActionDetails.jsx";
import ExtractionReview from "./pages/ExtractionReview.jsx";
import HumanVerification from "./pages/HumanVerification.jsx";
import UploadJudgment from "./pages/UploadJudgment.jsx";

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/upload" element={<UploadJudgment />} />
        <Route path="/review/:judgmentId" element={<ExtractionReview />} />
        <Route path="/verify" element={<HumanVerification />} />
        <Route path="/approved" element={<ApprovedActions />} />
        <Route path="/actions/:actionId" element={<ActionDetails />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}

