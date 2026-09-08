import { useState } from "react";
import { analyzeJobFitUpload } from "../api/resumeApi";

function JobFitAnalyzer() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jdMode, setJdMode] = useState("file"); // "file" or "text"
  const [jdFile, setJdFile] = useState(null);
  const [jdText, setJdText] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const handleResumeChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (!file.name.toLowerCase().endsWith(".pdf")) {
        setError("Resume must be a PDF file.");
        setResumeFile(null);
        return;
      }
      setError("");
      setResumeFile(file);
    }
  };

  const handleJdFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (!file.name.toLowerCase().endsWith(".pdf")) {
        setError("Job Description file must be a PDF.");
        setJdFile(null);
        return;
      }
      setError("");
      setJdFile(file);
    }
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return "0 KB";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!resumeFile) {
      setError("Please upload your Resume PDF file.");
      return;
    }

    if (jdMode === "file" && !jdFile) {
      setError("Please upload a Job Description PDF file or switch to Paste text mode.");
      return;
    }

    if (jdMode === "text" && (!jdText || !jdText.trim())) {
      setError("Please paste the Job Description text.");
      return;
    }

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("resumeFile", resumeFile);

    if (jdMode === "file" && jdFile) {
      formData.append("jobDescriptionFile", jdFile);
    } else if (jdMode === "text" && jdText) {
      formData.append("jobDescriptionText", jdText.trim());
    }

    try {
      const data = await analyzeJobFitUpload(formData);
      setResult(data);
    } catch (err) {
      console.error("Job Fit Analysis error:", err);
      const serverMessage = err?.response?.data?.message || err?.message || "Failed to analyze Job Fit. Please try again.";
      setError(serverMessage);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 75) return "#059669"; // Green
    if (score >= 50) return "#d97706"; // Amber
    return "#dc2626"; // Red
  };

  return (
    <div className="job-fit-container">
      <header className="job-fit-header">
        <h2>AI Job Fit Analyzer</h2>
        <p>Evaluate your Resume against any Job Description with Groq AI semantic analysis & weighted scoring</p>
      </header>

      <form onSubmit={handleSubmit} className="job-fit-form-card">
        {error && <div className="job-fit-error-banner">{error}</div>}

        <div className="job-fit-inputs-grid">
          {/* Resume Upload Card */}
          <div className="upload-box">
            <div className="box-title">
              <span className="step-number">1</span>
              <h3>Upload Resume PDF</h3>
            </div>
            <p className="box-desc">Select your formatted resume in PDF format</p>

            <label className="file-drop-zone">
              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={handleResumeChange}
                disabled={loading}
              />
              <div className="drop-content">
                <svg className="upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <span className="drop-text">{resumeFile ? "Change Resume PDF" : "Choose Resume PDF"}</span>
              </div>
            </label>

            {resumeFile && (
              <div className="file-info-badge">
                <span className="file-name">📄 {resumeFile.name}</span>
                <span className="file-size">({formatFileSize(resumeFile.size)})</span>
                <span className="ready-tag">Ready</span>
              </div>
            )}
          </div>

          {/* Job Description Card */}
          <div className="upload-box">
            <div className="box-title">
              <span className="step-number">2</span>
              <h3>Job Description</h3>
            </div>

            <div className="jd-toggle-bar">
              <button
                type="button"
                className={`toggle-btn ${jdMode === "file" ? "active" : ""}`}
                onClick={() => setJdMode("file")}
                disabled={loading}
              >
                Upload JD PDF
              </button>
              <button
                type="button"
                className={`toggle-btn ${jdMode === "text" ? "active" : ""}`}
                onClick={() => setJdMode("text")}
                disabled={loading}
              >
                Paste JD Text
              </button>
            </div>

            {jdMode === "file" ? (
              <>
                <label className="file-drop-zone">
                  <input
                    type="file"
                    accept=".pdf,application/pdf"
                    onChange={handleJdFileChange}
                    disabled={loading}
                  />
                  <div className="drop-content">
                    <svg className="upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <span className="drop-text">{jdFile ? "Change JD PDF" : "Choose Job Description PDF"}</span>
                  </div>
                </label>

                {jdFile && (
                  <div className="file-info-badge">
                    <span className="file-name">📋 {jdFile.name}</span>
                    <span className="file-size">({formatFileSize(jdFile.size)})</span>
                    <span className="ready-tag">Ready</span>
                  </div>
                )}
              </>
            ) : (
              <textarea
                className="jd-textarea"
                placeholder="Paste the target job description requirements, responsibilities, and required skills here..."
                value={jdText}
                onChange={(e) => setJdText(e.target.value)}
                disabled={loading}
              />
            )}
          </div>
        </div>

        <div className="submit-action-row">
          <button type="submit" className="analyze-submit-btn" disabled={loading}>
            {loading ? (
              <span className="loading-spinner-wrapper">
                <span className="spinner-dot"></span>
                Analyzing Resume & Requirements...
              </span>
            ) : (
              "⚡ Analyze Job Fit"
            )}
          </button>
        </div>
      </form>

      {/* Results Dashboard */}
      {result && (
        <div className="job-fit-results-card">
          <div className="score-summary-banner">
            <div className="overall-score-circle" style={{ borderColor: getScoreColor(result.matchScore) }}>
              <span className="score-number" style={{ color: getScoreColor(result.matchScore) }}>
                {result.matchScore}
              </span>
              <span className="score-max">/ 100</span>
            </div>

            <div className="score-meta">
              <h3 className="score-title">AI Job Fit Score</h3>
              <p className="summary-paragraph">{result.matchSummary}</p>
              {result.calculationExplanation && (
                <div className="calc-explanation-badge">
                  <span>ℹ️ {result.calculationExplanation}</span>
                </div>
              )}
            </div>
          </div>

          {/* 5-Tier Score Breakdown */}
          {result.scoreBreakdown && (
            <div className="breakdown-section">
              <h4>Score Breakdown</h4>
              <div className="breakdown-grid">
                <ScoreBar label="Skills Match" score={result.scoreBreakdown.skillsScore} weight="40%" />
                <ScoreBar label="Keyword Match" score={result.scoreBreakdown.keywordScore} weight="25%" />
                <ScoreBar label="Experience Match" score={result.scoreBreakdown.experienceScore} weight="15%" />
                <ScoreBar label="Education Match" score={result.scoreBreakdown.educationScore} weight="10%" />
                <ScoreBar label="Project Relevance" score={result.scoreBreakdown.projectScore} weight="10%" />
              </div>
            </div>
          )}

          {/* Skills Categorization Lists */}
          <div className="skills-analysis-grid">
            {/* Matched Skills */}
            <div className="skills-card matched-card">
              <h4>✅ Matched Skills ({result.matchedSkills?.length || 0})</h4>
              <div className="tag-cloud">
                {result.matchedSkills && result.matchedSkills.length > 0 ? (
                  result.matchedSkills.map((skill, idx) => (
                    <span key={idx} className="tag tag-matched">{skill}</span>
                  ))
                ) : (
                  <p className="no-items">No exact skill matches identified.</p>
                )}
              </div>
            </div>

            {/* Partial Matches */}
            <div className="skills-card partial-card">
              <h4>⚡ Partial / Transferable Matches ({result.partialMatches?.length || 0})</h4>
              <div className="tag-cloud">
                {result.partialMatches && result.partialMatches.length > 0 ? (
                  result.partialMatches.map((skill, idx) => (
                    <span key={idx} className="tag tag-partial">{skill}</span>
                  ))
                ) : (
                  <p className="no-items">No partial matches identified.</p>
                )}
              </div>
            </div>

            {/* Missing Skills */}
            <div className="skills-card missing-card">
              <h4>⚠️ Missing Skills ({result.missingSkills?.length || 0})</h4>
              <div className="tag-cloud">
                {result.missingSkills && result.missingSkills.length > 0 ? (
                  result.missingSkills.map((skill, idx) => (
                    <span key={idx} className="tag tag-missing">{skill}</span>
                  ))
                ) : (
                  <p className="no-items">No critical missing skills detected.</p>
                )}
              </div>
            </div>
          </div>

          {/* Strengths & Recommendations */}
          <div className="feedback-grid">
            <div className="feedback-card strengths-box">
              <h4>💪 Resume Strengths</h4>
              <ul>
                {result.resumeStrengths && result.resumeStrengths.length > 0 ? (
                  result.resumeStrengths.map((item, idx) => <li key={idx}>{item}</li>)
                ) : (
                  <li>No specific strengths highlighted.</li>
                )}
              </ul>
            </div>

            <div className="feedback-card recommendations-box">
              <h4>🚀 Recommendations to Improve Fit</h4>
              <ul>
                {result.recommendations && result.recommendations.length > 0 ? (
                  result.recommendations.map((item, idx) => <li key={idx}>{item}</li>)
                ) : (
                  <li>No specific recommendations needed.</li>
                )}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function ScoreBar({ label, score, weight }) {
  const getBarColor = (val) => {
    if (val >= 75) return "#059669";
    if (val >= 50) return "#d97706";
    return "#dc2626";
  };

  return (
    <div className="score-bar-item">
      <div className="score-bar-header">
        <span className="bar-label">{label} <small>({weight})</small></span>
        <span className="bar-value" style={{ color: getBarColor(score) }}>{score}%</span>
      </div>
      <div className="bar-track">
        <div
          className="bar-fill"
          style={{ width: `${score}%`, backgroundColor: getBarColor(score) }}
        ></div>
      </div>
    </div>
  );
}

export default JobFitAnalyzer;
