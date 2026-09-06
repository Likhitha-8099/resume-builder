import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import { saveAs } from "file-saver";
import {
  Document,
  Packer,
  Paragraph,
  TextRun,
  HeadingLevel,
} from "docx";

export const downloadResumeAsPdf = async (elementId, fileName) => {
  const resumeElement = document.getElementById(elementId);

  if (!resumeElement) {
    alert("Resume preview not found");
    return;
  }

  const canvas = await html2canvas(resumeElement, {
    scale: 3,
    useCORS: true,
    backgroundColor: "#ffffff",
  });

  const imgData = canvas.toDataURL("image/png");

  const pdf = new jsPDF("p", "mm", "a4");

  const pageWidth = pdf.internal.pageSize.getWidth();
  const pageHeight = pdf.internal.pageSize.getHeight();

  const imgWidth = pageWidth;
  const imgHeight = (canvas.height * imgWidth) / canvas.width;

  if (imgHeight <= pageHeight) {
    pdf.addImage(imgData, "PNG", 0, 0, imgWidth, imgHeight);
  } else {
    let position = 0;
    let heightLeft = imgHeight;

    pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
    heightLeft -= pageHeight;

    while (heightLeft > 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;
    }
  }

  pdf.save(`${fileName || "resume"}.pdf`);
};

export const downloadResumeAsDocx = async (resume = {}) => {
  const doc = new Document({
    sections: [
      {
        children: [
          new Paragraph({
            children: [
              new TextRun({
                text: resume.fullName || "Your Name",
                bold: true,
                size: 32,
              }),
            ],
          }),

          new Paragraph({
            children: [
              new TextRun({
                text: `${resume.phone || ""} | ${resume.email || ""}`,
                size: 22,
              }),
            ],
          }),

          new Paragraph({
            children: [
              new TextRun({
                text: `${resume.linkedin || ""} ${
                  resume.github ? "| " + resume.github : ""
                }`,
                size: 22,
              }),
            ],
          }),

          new Paragraph({
            text: "Objective",
            heading: HeadingLevel.HEADING_2,
          }),
          new Paragraph(resume.summary || ""),

          new Paragraph({
            text: "Education",
            heading: HeadingLevel.HEADING_2,
          }),
          new Paragraph(resume.education || ""),

          new Paragraph({
            text: "Experience",
            heading: HeadingLevel.HEADING_2,
          }),
          new Paragraph(resume.experience || ""),

          new Paragraph({
            text: "Projects",
            heading: HeadingLevel.HEADING_2,
          }),
          new Paragraph(resume.projects || ""),

          new Paragraph({
            text: "Technical Skills and Interests",
            heading: HeadingLevel.HEADING_2,
          }),
          new Paragraph(resume.skills || ""),

          new Paragraph({
            text: "Certifications",
            heading: HeadingLevel.HEADING_2,
          }),
          new Paragraph(resume.certifications || ""),
        ],
      },
    ],
  });

  const blob = await Packer.toBlob(doc);
  saveAs(blob, `${resume.fullName || "resume"}.docx`);
};