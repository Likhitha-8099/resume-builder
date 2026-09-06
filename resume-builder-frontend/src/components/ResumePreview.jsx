import DownloadButtons from "./DownloadButton";

function formatLines(text) {
  if (!text) return [];

  return text
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0);
}

function ResumePreview({ resume = {} }) {
  const educationLines = formatLines(resume.education);
  const experienceLines = formatLines(resume.experience);
  const projectLines = formatLines(resume.projects);
  const skillLines = formatLines(resume.skills);

  return (
    <section className="preview-section">
      <div className="preview-top">
        <div>
          <h2>Professional Preview</h2>
          <p className="section-subtitle">ATS-friendly one-page resume format</p>
        </div>

        <DownloadButtons resume={resume} />
      </div>

      <div className="resume-paper" id="resume-preview-download">
        <div className="resume-main-header">
          <h1>{resume.fullName || "Your Name"}</h1>

          <p className="contact-line">
            {resume.phone || "+91-XXXXXXXXXX"} |{" "}
            {resume.email || "email@example.com"}
          </p>

          <p className="contact-line">
            {resume.linkedin || "LinkedIn"}{" "}
            {resume.github ? `| ${resume.github}` : "| GitHub"}
          </p>
        </div>

        <ResumeSection title="Objective">
          <p>
            {resume.summary ||
              "Write a concise professional objective highlighting your skills, learning mindset, and career goals."}
          </p>
        </ResumeSection>

        <ResumeSection title="Education">
          {educationLines.length > 0 ? (
            educationLines.map((line, index) => (
              <p key={index} className="resume-line">
                {line}
              </p>
            ))
          ) : (
            <p className="muted-text">Add your education details here.</p>
          )}
        </ResumeSection>

        <ResumeSection title="Experience">
          {experienceLines.length > 0 ? (
            experienceLines.map((line, index) => (
              <p
                key={index}
                className={line.startsWith("•") ? "bullet-line" : "resume-line"}
              >
                {line}
              </p>
            ))
          ) : (
            <p className="muted-text">Add your internship or work experience.</p>
          )}
        </ResumeSection>

        <ResumeSection title="Projects">
          {projectLines.length > 0 ? (
            projectLines.map((line, index) => (
              <p
                key={index}
                className={line.startsWith("•") ? "bullet-line" : "resume-line"}
              >
                {line}
              </p>
            ))
          ) : (
            <p className="muted-text">Add your project details here.</p>
          )}
        </ResumeSection>

        <ResumeSection title="Technical Skills and Interests">
          {skillLines.length > 0 ? (
            <p>
              <strong>Skills:</strong> {resume.skills}
            </p>
          ) : (
            <p className="muted-text">Add your technical skills.</p>
          )}
        </ResumeSection>

        <ResumeSection title="Certifications">
          <p className="muted-text">
            Add certifications field in backend later for full professional format.
          </p>
        </ResumeSection>
      </div>
    </section>
  );
}

function ResumeSection({ title, children }) {
  return (
    <div className="resume-block">
      <h3>{title}</h3>
      {children}
    </div>
  );
}

export default ResumePreview;