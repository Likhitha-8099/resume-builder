import { useEffect, useState } from "react";
import { getAllResumes, generateAiSummary } from "../api/resumeApi";

function ResumeList({ refreshList, onSelectResume }) {
  const [resumes, setResumes] = useState([]);
  const [loadingId, setLoadingId] = useState(null);

  const fetchResumes = async () => {
    try {
      const data = await getAllResumes();

      // Safety: only array set cheyyali
      if (Array.isArray(data)) {
        setResumes(data);
      } else {
        console.error("Expected array but got:", data);
        setResumes([]);
      }
    } catch (error) {
      console.error("Failed to fetch resumes", error);
      setResumes([]);
    }
  };

  useEffect(() => {
    fetchResumes();
  }, [refreshList]);

  const handleGenerateSummary = async (resumeId) => {
    setLoadingId(resumeId);

    try {
      const updatedResume = await generateAiSummary(resumeId);

      setResumes((prevResumes) =>
        Array.isArray(prevResumes)
          ? prevResumes.map((resume) =>
              resume.id === resumeId ? updatedResume : resume
            )
          : []
      );

      onSelectResume(updatedResume);
      alert("AI summary generated successfully!");
    } catch (error) {
      console.error("AI summary generation failed", error);
      alert("AI summary generation failed.");
    } finally {
      setLoadingId(null);
    }
  };

  const safeResumes = Array.isArray(resumes) ? resumes : [];

  return (
    <section className="list-section">
      <h2>Saved Resumes</h2>

      {safeResumes.length === 0 ? (
        <p>No resumes saved yet.</p>
      ) : (
        <div className="resume-list">
          {safeResumes.map((resume) => (
            <div className="resume-card" key={resume.id}>
              <h3>{resume.fullName}</h3>
              <p>{resume.email}</p>
              <p>{resume.skills}</p>

              <div className="card-actions">
                <button onClick={() => onSelectResume(resume)}>
                  View Resume
                </button>

                <button
                  onClick={() => handleGenerateSummary(resume.id)}
                  disabled={loadingId === resume.id}
                >
                  {loadingId === resume.id
                    ? "Generating..."
                    : "Generate AI Summary"}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default ResumeList;