import {
  downloadResumeAsPdf,
  downloadResumeAsDocx,
} from "../utils/downloadUtils";

function DownloadButtons({ resume }) {
  const fileName = resume?.fullName
    ? resume.fullName.replaceAll(" ", "_")
    : "resume";

  return (
    <div className="download-buttons">
      <button
        type="button"
        onClick={() => downloadResumeAsPdf("resume-preview-download", fileName)}
      >
        Download PDF
      </button>

      <button
        type="button"
        className="docx-btn"
        onClick={() => downloadResumeAsDocx(resume)}
      >
        Download DOCX
      </button>
    </div>
  );
}

export default DownloadButtons;