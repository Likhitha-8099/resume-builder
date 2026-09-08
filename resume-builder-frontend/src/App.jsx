import { useState } from "react";
import ResumeForm from "./components/ResumeForm";
import ResumePreview from "./components/ResumePreview";
import ResumeList from "./components/ResumeList";
import JobFitAnalyzer from "./components/JobFitAnalyzer";
import "./index.css";

function App() {
  const emptyResume = {
    fullName: "",
    email: "",
    phone: "",
    linkedin: "",
    github: "",
    summary: "",
    skills: "",
    technologies: "",
    libraries: "",
    softSkills: "",
    education: "",
    educationInstitution: "",
    experience: "",
    projects: "",
    certifications: "",
  };

  const [activeTab, setActiveTab] = useState("builder"); // "builder" or "jobfit"
  const [formData, setFormData] = useState(emptyResume);
  const [selectedResume, setSelectedResume] = useState(null);
  const [refreshList, setRefreshList] = useState(false);

  const handleResumeSaved = (savedResume) => {
    setSelectedResume(savedResume);
    setFormData(savedResume);
    setRefreshList((prev) => !prev);
  };

  const handleSelectResume = (resume) => {
    setSelectedResume(resume);
    setFormData(resume);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>AI Resume Builder</h1>
        <p>Create professional resumes & analyze job fit alignment with Groq AI</p>

        <nav className="app-nav-tabs">
          <button
            type="button"
            className={`nav-tab-btn ${activeTab === "builder" ? "active" : ""}`}
            onClick={() => setActiveTab("builder")}
          >
            📝 Resume Builder
          </button>
          <button
            type="button"
            className={`nav-tab-btn ${activeTab === "jobfit" ? "active" : ""}`}
            onClick={() => setActiveTab("jobfit")}
          >
            ⚡ AI Job Fit Analyzer
          </button>
        </nav>
      </header>

      {activeTab === "builder" ? (
        <>
          <main className="builder-layout">
            <ResumeForm
              formData={formData}
              setFormData={setFormData}
              onResumeSaved={handleResumeSaved}
            />

            <ResumePreview resume={selectedResume || formData} />
          </main>

          <ResumeList
            refreshList={refreshList}
            onSelectResume={handleSelectResume}
          />
        </>
      ) : (
        <JobFitAnalyzer />
      )}
    </div>
  );
}

export default App;