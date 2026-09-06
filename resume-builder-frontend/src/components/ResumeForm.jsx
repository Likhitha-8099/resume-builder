import { useState } from "react";
import { createResume } from "../api/resumeApi";

function ResumeForm({ formData, setFormData, onResumeSaved }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const savedResume = await createResume(formData);
      onResumeSaved(savedResume);
      alert("Resume saved successfully!");
    } catch (err) {
      setError("Failed to save resume. Please check all required fields.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="form-section">
      <h2>Resume Details</h2>

      {error && <p className="error">{error}</p>}

      <form onSubmit={handleSubmit} className="resume-form">
        <input
          type="text"
          name="fullName"
          placeholder="Full Name"
          value={formData.fullName}
          onChange={handleChange}
          required
        />

        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />

        <input
          type="text"
          name="phone"
          placeholder="Phone Number"
          value={formData.phone}
          onChange={handleChange}
          required
        />

        <input
          type="text"
          name="linkedin"
          placeholder="LinkedIn URL"
          value={formData.linkedin}
          onChange={handleChange}
        />

        <input
          type="text"
          name="github"
          placeholder="GitHub URL"
          value={formData.github}
          onChange={handleChange}
        />

        <textarea
          name="summary"
          placeholder="Professional Summary"
          value={formData.summary}
          onChange={handleChange}
          required
        />

        <textarea
          name="skills"
          placeholder="Skills"
          value={formData.skills}
          onChange={handleChange}
          required
        />

        <textarea
          name="education"
          placeholder="Education"
          value={formData.education}
          onChange={handleChange}
        />

        <textarea
          name="experience"
          placeholder="Experience"
          value={formData.experience}
          onChange={handleChange}
        />

        <textarea
          name="projects"
          placeholder="Projects"
          value={formData.projects}
          onChange={handleChange}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Saving..." : "Save Resume"}
        </button>
      </form>
    </section>
  );
}

export default ResumeForm;