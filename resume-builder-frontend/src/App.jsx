import { useState } from "react";
import ResumeForm from "./components/ResumeForm";
import ResumePreview from "./components/ResumePreview";
import ResumeList from "./components/ResumeList";
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
        <p>Create professional resumes with AI-powered summary generation</p>
      </header>

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
    </div>
  );
}

export default App;