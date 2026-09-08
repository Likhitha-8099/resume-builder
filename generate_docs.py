import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas

# Numbered Canvas for "Page X of Y" and Running Header/Footer
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        # Skip header/footer on cover page, certificate, declaration, acknowledgement (pages 1 to 4)
        if self._pageNumber <= 4:
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0F172A")) # Dark slate text
        
        # Running Header
        self.drawString(54, 750, "AI RESUME BUILDER — COMPLETE ACADEMIC & INDUSTRY PROJECT REPORT")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 742, 612 - 54, 742)

        # Running Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 36, "Confidential — Project & Internship Technical Documentation")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 36, page_str)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 612 - 54, 48)

        self.restoreState()


def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Design System Palette
    primary_color = colors.HexColor("#0F172A")    # Deep slate
    secondary_color = colors.HexColor("#2563EB")  # Accent Royal Blue
    dark_gray = colors.HexColor("#334155")        # Body text
    light_bg = colors.HexColor("#F8FAFC")         # Box backgrounds
    border_color = colors.HexColor("#E2E8F0")     # Structural lines
    code_bg = colors.HexColor("#1E293B")          # Code background

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=primary_color,
        alignment=TA_CENTER,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=17,
        textColor=secondary_color,
        alignment=TA_CENTER,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=dark_gray,
        spaceAfter=6,
        alignment=TA_LEFT
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#F8FAFC"),
        spaceBefore=4,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    )

    tbl_header_style = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    tbl_cell_style = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=dark_gray
    )

    story = []

    def make_callout(text, bg="#F1F5F9", border="#2563EB"):
        p = Paragraph(text, callout_style)
        t = Table([[p]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg)),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor(border)),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    def make_section_header(title):
        p = Paragraph(title.upper(), h1_style)
        hr = HRFlowable(width="100%", thickness=1.5, color=secondary_color, spaceBefore=2, spaceAfter=8)
        return [p, hr]

    def make_code_box(code_text):
        lines = code_text.strip().split('\n')
        p_list = [Paragraph(line.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;'), code_style) for line in lines]
        t = Table([[p_list]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), code_bg),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#334155")),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        return t

    # ==================== 1. COVER PAGE ====================
    story.append(Spacer(1, 20))
    story.append(Paragraph("AI RESUME BUILDER", title_style))
    story.append(Paragraph("Full-Stack Web Application with LLM-Powered Professional Summary Generation", subtitle_style))
    story.append(HRFlowable(width="60%", thickness=2, color=secondary_color, spaceBefore=5, spaceAfter=20))
    
    meta_box_data = [
        [Paragraph("<b>Project Name:</b>", body_style), Paragraph("AI Resume Builder", body_style)],
        [Paragraph("<b>Domain:</b>", body_style), Paragraph("Full-Stack Web Development & Generative AI Integration", body_style)],
        [Paragraph("<b>Duration:</b>", body_style), Paragraph("[TO BE PROVIDED]", body_style)],
        [Paragraph("<b>Organization / Internship:</b>", body_style), Paragraph("[TO BE PROVIDED]", body_style)],
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("[TO BE PROVIDED]", body_style)],
        [Paragraph("<b>College Name:</b>", body_style), Paragraph("[TO BE PROVIDED]", body_style)],
        [Paragraph("<b>Department:</b>", body_style), Paragraph("Computer Science & Engineering", body_style)],
        [Paragraph("<b>Batch:</b>", body_style), Paragraph("[TO BE PROVIDED]", body_style)],
        [Paragraph("<b>Internship Duration:</b>", body_style), Paragraph("[TO BE PROVIDED]", body_style)],
        [Paragraph("<b>Academic Year:</b>", body_style), Paragraph("2025 – 2026", body_style)],
        [Paragraph("<b>Team Size:</b>", body_style), Paragraph("[TO BE PROVIDED]", body_style)],
        [Paragraph("<b>My Role:</b>", body_style), Paragraph("Full-Stack Developer (Java Spring Boot & React)", body_style)],
        [Paragraph("<b>Technologies Used:</b>", body_style), Paragraph("Java 17, Spring Boot 4.0.6, React 19, Vite 8, MySQL, Gemini AI API", body_style)],
    ]
    meta_table = Table(meta_box_data, colWidths=[150, 354])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    
    story.append(Spacer(1, 20))
    story.append(make_callout(
        "<b>Academic & Technical Verification Statement:</b> This project report provides a formal, comprehensive documentation of the AI Resume Builder project. It covers end-to-end system architecture, REST API design, JPA database schemas, Google Gemini LLM API integration, functional testing, and interview preparation questions.",
        bg="#EFF6FF", border="#3B82F6"
    ))
    story.append(PageBreak())

    # ==================== 2. CERTIFICATE ====================
    story.extend(make_section_header("2. CERTIFICATE OF PROJECT COMPLETION"))
    story.append(Spacer(1, 15))
    cert_text = (
        "This is to certify that the project entitled <b>\"AI RESUME BUILDER\"</b> is a bona fide work carried out by "
        "<b>[TO BE PROVIDED]</b> in partial fulfillment of the requirements for the award of the degree of <b>Bachelor of Technology (B.Tech) in Computer Science & Engineering</b> "
        "during the academic year <b>2025–2026</b>.<br/><br/>"
        "The project work has been completed under the mentorship and supervision at <b>[TO BE PROVIDED]</b>. "
        "To the best of our knowledge, the results embodied in this report have not been submitted to any other University or Institution for the award of any degree or diploma."
    )
    story.append(Paragraph(cert_text, body_style))
    story.append(Spacer(1, 40))
    
    sig_data = [
        [Paragraph("______________________<br/><b>Project Mentor / Guide</b><br/>[TO BE PROVIDED]", body_style),
         Paragraph("______________________<br/><b>Head of Department (CSE)</b><br/>[TO BE PROVIDED]", body_style)],
        [Spacer(1, 30), Spacer(1, 30)],
        [Paragraph("______________________<br/><b>External Examiner</b><br/>Date: [TO BE PROVIDED]", body_style),
         Paragraph("______________________<br/><b>Organization Seal</b><br/>[TO BE PROVIDED]", body_style)]
    ]
    sig_table = Table(sig_data, colWidths=[252, 252])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT')
    ]))
    story.append(sig_table)
    story.append(PageBreak())

    # ==================== 3. DECLARATION ====================
    story.extend(make_section_header("3. FORMAL STUDENT DECLARATION"))
    story.append(Spacer(1, 15))
    decl_text = (
        "I, <b>[TO BE PROVIDED]</b>, student of <b>[TO BE PROVIDED]</b>, Department of Computer Science & Engineering, bearing Batch <b>[TO BE PROVIDED]</b>, "
        "hereby declare that the project report entitled <b>\"AI RESUME BUILDER\"</b> submitted by me is an authentic record of my original work "
        "carried out during my internship/project period at <b>[TO BE PROVIDED]</b> under the guidance of my mentor.<br/><br/>"
        "I confirm that:<br/>"
        "1. The work submitted is my own contribution, developed using Java Spring Boot, React, MySQL, and Google Gemini API.<br/>"
        "2. No part of this report has been plagiarized or copied from any other source without proper citation and referencing.<br/>"
        "3. Any technical assistance received during the development has been fully acknowledged."
    )
    story.append(Paragraph(decl_text, body_style))
    story.append(Spacer(1, 50))
    story.append(Paragraph("<b>Place:</b> [TO BE PROVIDED]", body_style))
    story.append(Paragraph("<b>Date:</b> [TO BE PROVIDED]", body_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("________________________________________<br/><b>Signature of Student:</b> [TO BE PROVIDED]", body_style))
    story.append(PageBreak())

    # ==================== 4. ACKNOWLEDGEMENT ====================
    story.extend(make_section_header("4. ACKNOWLEDGEMENT"))
    story.append(Spacer(1, 15))
    ack_text = (
        "I would like to express my deepest gratitude to <b>[TO BE PROVIDED]</b> for providing me with the opportunity to undertake this project and work on real-world industry applications.<br/><br/>"
        "I express my sincere thanks to my project mentor <b>[TO BE PROVIDED]</b> for their continuous guidance, technical insights, and valuable feedback throughout the design, development, and testing phases of the AI Resume Builder project.<br/><br/>"
        "I am immensely grateful to the Head of Department, Computer Science & Engineering, and all faculty members at <b>[TO BE PROVIDED]</b> for providing the academic foundation, infrastructure, and encouragement necessary to complete this project successfully.<br/><br/>"
        "Finally, I thank my team members and family for their unwavering support and motivation during this project journey."
    )
    story.append(Paragraph(ack_text, body_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("<b>Student Name:</b> [TO BE PROVIDED]", body_style))
    story.append(Paragraph("<b>Role:</b> Full-Stack Developer", body_style))
    story.append(PageBreak())

    # ==================== 5. ABSTRACT ====================
    story.extend(make_section_header("5. ABSTRACT"))
    story.append(Paragraph("<b>5.1 What the Project Is</b>", h2_style))
    story.append(Paragraph("The <b>AI Resume Builder</b> is a modern, full-stack web application designed to automate the process of creating, editing, formatting, storing, and exporting professional software engineering resumes. Built on a decoupled architecture featuring a React 19 single-page frontend and a Java 17 / Spring Boot 4 backend REST service with MySQL database persistence, the system incorporates artificial intelligence to generate impact-driven candidate summaries.", body_style))

    story.append(Paragraph("<b>5.2 Problem Solved & Project Necessity</b>", h2_style))
    story.append(Paragraph("Job applicants—especially freshers and junior developers—face significant challenges when drafting resumes: manual layout formatting in desktop software is tedious, non-standard layouts fail Applicant Tracking System (ATS) parsing algorithms, and writing a concise, professional summary without fluff is difficult. The AI Resume Builder addresses these pain points by offering structured input forms, live rendering of an ATS-optimized template, and automated summary synthesis powered by LLMs.", body_style))

    story.append(Paragraph("<b>5.3 Main Technologies & Major Features</b>", h2_style))
    story.append(Paragraph("<b>Technology Stack:</b> Java 17, Spring Boot 4.0.6, Spring Data JPA, Hibernate, MySQL, React 19, Vite 8, Axios, Google Gemini API, jsPDF, html2canvas, docx.<br/>"
                           "<b>Major Features:</b> Full CRUD operations for resume profiles, live split-screen ATS preview rendering, automated 3-line AI summary generation via Google Gemini API, dual client-side export to PDF and DOCX formats, request data validation using Jakarta Validation, and OpenAPI / Swagger UI interactive endpoint documentation.", body_style))

    story.append(Paragraph("<b>5.4 Overall Outcome</b>", h2_style))
    story.append(Paragraph("The application significantly reduces the time required to build a professional resume from hours to minutes while guaranteeing structural consistency, ATS compliance, and high-quality summary phrasing.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 6. INTRODUCTION ====================
    story.extend(make_section_header("6. INTRODUCTION"))
    story.append(Paragraph("<b>6.1 Background & Domain Context</b>", h2_style))
    story.append(Paragraph("In modern recruitment workflows, a candidate's resume serves as the initial screening benchmark. With hiring managers receiving hundreds of applications per job posting, automated Applicant Tracking Systems (ATS) are deployed to filter and parse candidate data. Resumes with complex tables, graphical columns, or inconsistent formatting are frequently rejected automatically by ATS parsers before human review.", body_style))

    story.append(Paragraph("<b>6.2 Digital Transformation in Resume Generation</b>", h2_style))
    story.append(Paragraph("Traditional word processing tools (such as Microsoft Word or manual HTML editors) require manual alignment, font adjustments, and visual tuning. This leads to user frustration and formatting errors. Web-based resume builders solve this by separating candidate data entry from template layout rendering, ensuring consistent styling across all generated documents.", body_style))

    story.append(Paragraph("<b>6.3 The Role of Artificial Intelligence</b>", h2_style))
    story.append(Paragraph("While traditional resume builders assist with visual layout, they leave the task of content creation entirely to the user. Many candidates struggle to articulate their skills, projects, and educational background into a compelling 3-line objective summary. By integrating Google's Gemini Large Language Model (LLM) via a REST API, the AI Resume Builder automates professional summary generation based on candidate input data.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 7. PROBLEM STATEMENT ====================
    story.extend(make_section_header("7. PROBLEM STATEMENT"))
    story.append(Paragraph("<b>7.1 Existing Problems in Resume Creation</b>", h2_style))
    story.append(Paragraph("1. <b>Formatting Friction:</b> Desktop publishing applications require manual pixel-perfect adjustment of margins, fonts, and bullet points.<br/>"
                           "2. <b>ATS Parsing Incompatibility:</b> Non-standard resume designs containing multi-column visual tables or images cannot be parsed correctly by corporate ATS software.<br/>"
                           "3. <b>Writer's Block & Generic Summaries:</b> Freshers frequently write generic or overly wordy summaries that fail to highlight key technical competencies.<br/>"
                           "4. <b>Lack of Centralized Persistence:</b> Storing resumes as loose files on local disks leads to version confusion and lost candidate profiles.<br/>"
                           "5. <b>Inflexible Export Options:</b> Candidates often need both immutable PDF files for online portals and editable Word documents for recruiters.", body_style))

    story.append(Paragraph("<b>7.2 Need for Automation</b>", h2_style))
    story.append(Paragraph("Automating resume creation through a centralized web application eliminates visual formatting overhead, guarantees ATS compatibility, provides instant AI summary generation, and persists candidate profiles reliably in a relational database.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 8. OBJECTIVES ====================
    story.extend(make_section_header("8. OBJECTIVES"))
    story.append(Paragraph("<b>8.1 Primary Objectives</b>", h2_style))
    story.append(Paragraph("• Develop a responsive React 19 single-page frontend with real-time split-screen ATS resume preview.<br/>"
                           "• Build a robust Spring Boot 4 REST API with full CRUD capability for candidate resume management.<br/>"
                           "• Implement MySQL relational database storage using Spring Data JPA and Hibernate ORM.<br/>"
                           "• Integrate Google Gemini API via Spring RestTemplate to automatically generate concise 3-line candidate summaries.<br/>"
                           "• Provide client-side document export capability to both PDF (jsPDF / html2canvas) and DOCX (docx library).", bullet_style))

    story.append(Paragraph("<b>8.2 Secondary Objectives</b>", h2_style))
    story.append(Paragraph("• Enforce data integrity using declarative Jakarta Validation annotations (`@Valid`, `@NotNull`, `@Size`).<br/>"
                           "• Externalize sensitive configuration keys (`ai.api.key`, `ai.api.url`) using Spring environment properties.<br/>"
                           "• Expose interactive API documentation using Springdoc OpenAPI / Swagger UI.<br/>"
                           "• Implement cross-origin resource sharing (CORS) controls to secure API endpoints.", bullet_style))
    story.append(Spacer(1, 10))

    # ==================== 9. EXISTING SYSTEM ====================
    story.extend(make_section_header("9. EXISTING SYSTEM"))
    story.append(Paragraph("<b>9.1 Traditional Approach</b>", h2_style))
    story.append(Paragraph("In traditional workflows, candidates create resumes manually using offline desktop software (e.g., MS Word, Google Docs) or download static graphic templates. The candidate manually types all personal details, skills, experience, and summary text.", body_style))

    story.append(Paragraph("<b>9.2 Detailed Limitations of Existing Systems</b>", h2_style))
    existing_lim_data = [
        [Paragraph("<b>Dimension</b>", tbl_header_style), Paragraph("<b>Traditional / Existing Approach</b>", tbl_header_style), Paragraph("<b>Impact / Drawback</b>", tbl_header_style)],
        [Paragraph("Formatting", tbl_cell_style), Paragraph("Manual drag-and-drop & font styling", tbl_cell_style), Paragraph("High friction; inconsistent alignment & spacing", tbl_cell_style)],
        [Paragraph("ATS Compatibility", tbl_cell_style), Paragraph("Complex tables & multi-column graphics", tbl_cell_style), Paragraph("High rejection rate by automated ATS parsers", tbl_cell_style)],
        [Paragraph("Content Generation", tbl_cell_style), Paragraph("100% manual writing by candidate", tbl_cell_style), Paragraph("Writer's block; generic or wordy summaries", tbl_cell_style)],
        [Paragraph("Data Storage", tbl_cell_style), Paragraph("Unstructured local files (.docx / .pdf)", tbl_cell_style), Paragraph("No database search, version drift, potential data loss", tbl_cell_style)],
        [Paragraph("Export Capability", tbl_cell_style), Paragraph("Static print-to-PDF or single format", tbl_cell_style), Paragraph("Inability to generate both structured DOCX and clean PDF instantly", tbl_cell_style)],
    ]
    t_exist = Table(existing_lim_data, colWidths=[90, 200, 214])
    t_exist.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_exist)
    story.append(Spacer(1, 10))

    # ==================== 10. PROPOSED SYSTEM ====================
    story.extend(make_section_header("10. PROPOSED SYSTEM"))
    story.append(Paragraph("<b>10.1 System Overview & Key Advantages</b>", h2_style))
    story.append(Paragraph("The proposed <b>AI Resume Builder</b> replaces manual formatting and static document storage with a decoupled, web-native architecture. The user inputs structured candidate metadata into a reactive form, which instantly synchronizes with a live ATS-compliant preview.", body_style))

    story.append(Paragraph("<b>10.2 Architectural & Feature Improvements</b>", h2_style))
    story.append(Paragraph("• <b>Decoupled Architecture:</b> Frontend and backend communicate cleanly via JSON REST APIs.<br/>"
                           "• <b>Automated AI Summaries:</b> One-click Gemini LLM integration crafts tailored 3-line candidate summaries.<br/>"
                           "• <b>Relational Data Persistence:</b> Candidate profiles are safely stored in MySQL via Spring Data JPA.<br/>"
                           "• <b>Instant Client-Side Export:</b> Instant PDF and DOCX document generation directly in the browser without server rendering overhead.", bullet_style))
    story.append(Spacer(1, 10))

    # ==================== 11. SCOPE OF THE PROJECT ====================
    story.extend(make_section_header("11. SCOPE OF THE PROJECT"))
    story.append(Paragraph("<b>11.1 Current Implemented Scope (Audited Codebase)</b>", h2_style))
    story.append(Paragraph("1. Complete resume CRUD REST APIs (`POST`, `GET`, `PUT`, `DELETE`).<br/>"
                           "2. Google Gemini LLM API integration via Spring `RestTemplate`.<br/>"
                           "3. Real-time split-screen form entry and ATS template preview in React 19.<br/>"
                           "4. Direct client-side export to PDF (jsPDF / html2canvas) and DOCX (docx / file-saver).<br/>"
                           "5. MySQL database persistence with Spring Data JPA.<br/>"
                           "6. Interactive API documentation using Springdoc OpenAPI (Swagger UI).", body_style))

    story.append(Paragraph("<b>11.2 Future Scope & Enhancement Roadmap</b>", h2_style))
    story.append(Paragraph("1. <b>User Authentication & Authorization:</b> JWT / Spring Security with multi-tenant user isolation.<br/>"
                           "2. <b>Multi-Template Selector:</b> Choice of modern, creative, and academic resume templates.<br/>"
                           "3. <b>ATS Keyword Match Score:</b> Analyzing candidate resume against specific Job Description (JD) text.<br/>"
                           "4. <b>Cloud Deployment:</b> Containerizing via Docker and deploying to AWS / GCP.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 12. SYSTEM REQUIREMENTS ====================
    story.extend(make_section_header("12. SYSTEM REQUIREMENTS"))
    
    story.append(Paragraph("<b>12.1 Hardware Requirements</b>", h2_style))
    hw_data = [
        [Paragraph("<b>Component</b>", tbl_header_style), Paragraph("<b>Minimum Requirement</b>", tbl_header_style), Paragraph("<b>Recommended Requirement</b>", tbl_header_style)],
        [Paragraph("Processor", tbl_cell_style), Paragraph("Dual-Core 2.0 GHz (x86_64 / ARM)", tbl_cell_style), Paragraph("Quad-Core 2.5 GHz or higher", tbl_cell_style)],
        [Paragraph("RAM", tbl_cell_style), Paragraph("4 GB RAM", tbl_cell_style), Paragraph("8 GB RAM or higher", tbl_cell_style)],
        [Paragraph("Storage", tbl_cell_style), Paragraph("500 MB free disk space", tbl_cell_style), Paragraph("2 GB SSD free disk space", tbl_cell_style)],
        [Paragraph("Network", tbl_cell_style), Paragraph("Standard Internet (for Gemini API calls)", tbl_cell_style), Paragraph("High-speed Broadband", tbl_cell_style)]
    ]
    t_hw = Table(hw_data, colWidths=[120, 192, 192])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_hw)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>12.2 Software Requirements</b>", h2_style))
    sw_data = [
        [Paragraph("<b>Layer</b>", tbl_header_style), Paragraph("<b>Software / Tool</b>", tbl_header_style), Paragraph("<b>Version</b>", tbl_header_style)],
        [Paragraph("Operating System", tbl_cell_style), Paragraph("Windows 10/11, macOS, Linux", tbl_cell_style), Paragraph("64-bit OS", tbl_cell_style)],
        [Paragraph("Java Runtime", tbl_cell_style), Paragraph("Java Development Kit (JDK)", tbl_cell_style), Paragraph("Java 17 (LTS)", tbl_cell_style)],
        [Paragraph("Backend Framework", tbl_cell_style), Paragraph("Spring Boot", tbl_cell_style), Paragraph("4.0.6", tbl_cell_style)],
        [Paragraph("Frontend Runtime", tbl_cell_style), Paragraph("Node.js & npm", tbl_cell_style), Paragraph("Node v18+ / npm v9+", tbl_cell_style)],
        [Paragraph("Frontend Library", tbl_cell_style), Paragraph("React", tbl_cell_style), Paragraph("19.2.6 (Vite 8.0.12)", tbl_cell_style)],
        [Paragraph("Database", tbl_cell_style), Paragraph("MySQL Community Server", tbl_cell_style), Paragraph("8.0+", tbl_cell_style)],
        [Paragraph("Web Browser", tbl_cell_style), Paragraph("Google Chrome, Mozilla Firefox, Edge", tbl_cell_style), Paragraph("Latest Stable", tbl_cell_style)]
    ]
    t_sw = Table(sw_data, colWidths=[120, 224, 160])
    t_sw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_sw)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>12.3 Development Environment</b>", h2_style))
    story.append(Paragraph("• <b>IDE:</b> Eclipse IDE / IntelliJ IDEA / VS Code.<br/>"
                           "• <b>Build Automation:</b> Apache Maven 3.8+ (mvnw included).<br/>"
                           "• <b>API Testing & Documentation:</b> Swagger UI (Springdoc 2.8.9) & Postman.<br/>"
                           "• <b>Version Control:</b> Git & GitHub.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 13. TECHNOLOGY STACK ====================
    story.extend(make_section_header("13. TECHNOLOGY STACK & JUSTIFICATION"))
    
    tech_just_data = [
        [Paragraph("<b>Category</b>", tbl_header_style), Paragraph("<b>Technology Chosen</b>", tbl_header_style), Paragraph("<b>Why Selected (Technical Rationale)</b>", tbl_header_style)],
        [Paragraph("Frontend Core", tbl_cell_style), Paragraph("React 19", tbl_cell_style), Paragraph("Component-based architecture, efficient Virtual DOM state updates for live preview.", tbl_cell_style)],
        [Paragraph("Frontend Build Tool", tbl_cell_style), Paragraph("Vite 8", tbl_cell_style), Paragraph("Lightning-fast Hot Module Replacement (HMR) and optimized production bundler.", tbl_cell_style)],
        [Paragraph("HTTP Client", tbl_cell_style), Paragraph("Axios 1.18", tbl_cell_style), Paragraph("Promise-based HTTP client with clean request/response interceptors for REST APIs.", tbl_cell_style)],
        [Paragraph("Document Export", tbl_cell_style), Paragraph("jsPDF, html2canvas, docx", tbl_cell_style), Paragraph("Enables client-side PDF image rendering and native DOCX XML file generation.", tbl_cell_style)],
        [Paragraph("Backend Framework", tbl_cell_style), Paragraph("Spring Boot 4.0.6 (Java 17)", tbl_cell_style), Paragraph("Enterprise-grade REST support, dependency injection, robust ecosystem, LTS stability.", tbl_cell_style)],
        [Paragraph("ORM / Data Layer", tbl_cell_style), Paragraph("Spring Data JPA & Hibernate", tbl_cell_style), Paragraph("Eliminates boilerplate SQL queries; provides automated repository methods & schema management.", tbl_cell_style)],
        [Paragraph("Database", tbl_cell_style), Paragraph("MySQL 8.0", tbl_cell_style), Paragraph("Reliable ACID-compliant relational DB; excellent index support and Spring JPA integration.", tbl_cell_style)],
        [Paragraph("AI / LLM Integration", tbl_cell_style), Paragraph("Google Gemini API", tbl_cell_style), Paragraph("State-of-the-art text synthesis API accessed seamlessly via Spring RestTemplate.", tbl_cell_style)],
        [Paragraph("API Documentation", tbl_cell_style), Paragraph("Springdoc OpenAPI 2.8.9", tbl_cell_style), Paragraph("Generates interactive Swagger UI endpoint documentation directly from Spring code.", tbl_cell_style)]
    ]
    t_tech = Table(tech_just_data, colWidths=[100, 140, 264])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # ==================== 14. SYSTEM ARCHITECTURE ====================
    story.extend(make_section_header("14. SYSTEM ARCHITECTURE"))
    story.append(Paragraph("<b>14.1 High-Level Tier Architecture</b>", h2_style))
    story.append(Paragraph("The system follows a standard 3-Tier Layered Client-Server Architecture:", body_style))

    arch_box = (
        "+-----------------------------------------------------------------------------------+\n"
        "|                             USER / BROWSER INTERFACE                              |\n"
        "+-----------------------------------------------------------------------------------+\n"
        "                                          |\n"
        "                                  HTTP / JSON (REST)\n"
        "                                          v\n"
        "+-----------------------------------------------------------------------------------+\n"
        "|                        FRONTEND TIER (React 19 + Vite 8)                          |\n"
        "|   - Form State (ResumeForm.jsx)            - Live Preview (ResumePreview.jsx)      |\n"
        "|   - Client-side Export (jsPDF/docx)        - Axios API Service                       |\n"
        "+-----------------------------------------------------------------------------------+\n"
        "                                          |\n"
        "                               REST APIs (CORS Enabled)\n"
        "                                          v\n"
        "+-----------------------------------------------------------------------------------+\n"
        "|                     BACKEND TIER (Spring Boot 4.0.6 - Java 17)                    |\n"
        "|   - Controller Layer: ResumeController.java, AiController.java                    |\n"
        "|   - Service Layer: ResumeService.java, AiService.java                             |\n"
        "|   - Data Access Layer: ResumeRepository.java (Spring Data JPA)                    |\n"
        "+-----------------------------------------------------------------------------------+\n"
        "                      /                                       \\\n"
        "            Spring Data JPA / SQL                       RestTemplate / HTTPS\n"
        "                    v                                           v\n"
        "+-------------------------------+               +-----------------------------------+\n"
        "|      DATABASE STORAGE         |               |       EXTERNAL AI SERVICE         |\n"
        "|   MySQL 8.0 (resumes Table)   |               |        Google Gemini API          |\n"
        "+-------------------------------+               +-----------------------------------+\n"
    )
    story.append(make_code_box(arch_box))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>14.2 Detailed Component Responsibilities</b>", h2_style))
    story.append(Paragraph("• <b>Presentation Layer (Frontend):</b> Handles UI state, captures user form input, renders live ATS resume preview, and calls backend REST endpoints using Axios.<br/>"
                           "• <b>Controller Layer:</b> Exposes REST endpoints (`/api/resumes`, `/api/ai`), validates request DTOs (`@Valid`), and maps HTTP requests to service methods.<br/>"
                           "• <b>Service Layer:</b> Contains core business logic, orchestrates data transformations, builds prompts for Gemini API, and manages database transactions.<br/>"
                           "• <b>Persistence Layer:</b> Interacts with MySQL database via `JpaRepository` interface, converting Java entities into relational SQL rows.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 15. USER ROLES AND ACCESS CONTROL ====================
    story.extend(make_section_header("15. USER ROLES AND ACCESS CONTROL"))
    story.append(Paragraph("<b>15.1 System Roles & Matrix</b>", h2_style))
    
    roles_data = [
        [Paragraph("<b>Role Name</b>", tbl_header_style), Paragraph("<b>Responsibilities</b>", tbl_header_style), Paragraph("<b>Permissions</b>", tbl_header_style), Paragraph("<b>Restrictions</b>", tbl_header_style)],
        [Paragraph("Candidate / User", tbl_cell_style), Paragraph("Enter resume details, request AI summaries, export PDF/DOCX", tbl_cell_style), Paragraph("Create, Read, Update, Delete own resumes; trigger AI generation", tbl_cell_style), Paragraph("Cannot access administrative system configurations or other candidate data (planned)", tbl_cell_style)],
        [Paragraph("System Administrator [TO BE PROVIDED]", tbl_cell_style), Paragraph("Manage platform system settings, monitor API quotas, inspect logs", tbl_cell_style), Paragraph("Full system access, view Swagger UI, configure API keys", tbl_cell_style), Paragraph("Must authenticate via admin credentials", tbl_cell_style)]
    ]
    t_roles = Table(roles_data, colWidths=[90, 150, 140, 124])
    t_roles.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_roles)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>15.2 Authentication & Authorization Architecture</b>", h2_style))
    story.append(Paragraph("Currently, the system provides open REST APIs configured with Spring `@CrossOrigin` annotations allowing requests from the frontend development server (`http://localhost:5173`). Production implementations will incorporate Spring Security with JWT tokens for RBAC enforcement.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 16. FUNCTIONAL REQUIREMENTS ====================
    story.extend(make_section_header("16. FUNCTIONAL REQUIREMENTS"))
    
    fn_reqs = [
        ("FR-01: Candidate Profile Creation", "The system shall allow users to input personal details (Name, Email, Phone, LinkedIn, GitHub), education, skills, experience, and projects through a structured web form."),
        ("FR-02: Live ATS Resume Preview", "The system shall dynamically update a live split-screen resume preview in real time as the user types into form fields."),
        ("FR-03: Resume CRUD Management", "The system shall provide backend REST APIs to Create, Read, Update, and Delete candidate resume records in a MySQL database."),
        ("FR-04: AI Professional Summary Generation", "The system shall construct a contextual prompt from candidate skills, experience, and projects, send it to Google Gemini API via RestTemplate, and return a 3-line professional summary."),
        ("FR-05: AI Summary Database Persistence", "The system shall provide a dedicated endpoint (`PUT /api/resumes/{id}/generate-summary`) to generate an AI summary and automatically update the corresponding database record."),
        ("FR-06: Document Export (PDF & DOCX)", "The system shall allow users to download their formatted resume directly as a PDF (via jsPDF/html2canvas) or an editable Word document (via docx library)."),
        ("FR-07: Interactive API Documentation", "The system shall expose OpenAPI 3.0 specification endpoints via Swagger UI at `/swagger-ui.html` for interactive endpoint testing.")
    ]
    for code, desc in fn_reqs:
        story.append(Paragraph(f"• <b>{code}:</b> {desc}", bullet_style))
    story.append(Spacer(1, 10))

    # ==================== 17. NON-FUNCTIONAL REQUIREMENTS ====================
    story.extend(make_section_header("17. NON-FUNCTIONAL REQUIREMENTS"))
    
    nfr_data = [
        [Paragraph("<b>Attribute</b>", tbl_header_style), Paragraph("<b>Requirement Specification</b>", tbl_header_style), Paragraph("<b>Implementation Strategy</b>", tbl_header_style)],
        [Paragraph("Security", tbl_cell_style), Paragraph("Protect API keys, validate request payloads, prevent CORS exploits.", tbl_cell_style), Paragraph("API key externalized in `application.properties`; Jakarta `@Valid` payload checking; `@CrossOrigin` restricted.", tbl_cell_style)],
        [Paragraph("Performance", tbl_cell_style), Paragraph("CRUD API responses < 100ms; AI summary generation < 2.5s.", tbl_cell_style), Paragraph("HikariCP DB connection pooling; optimized RestTemplate HTTP calls; lightweight Vite frontend build.", tbl_cell_style)],
        [Paragraph("Scalability", tbl_cell_style), Paragraph("Stateless Spring Boot application able to scale horizontally.", tbl_cell_style), Paragraph("No server-side HTTP session state; stateless REST endpoints.", tbl_cell_style)],
        [Paragraph("Reliability", tbl_cell_style), Paragraph("Graceful handling of external Gemini API failures or network timeouts.", tbl_cell_style), Paragraph("Try-catch blocks in `AiService` returning fallback user-friendly messages without crashing the server.", tbl_cell_style)],
        [Paragraph("Maintainability", tbl_cell_style), Paragraph("Clean separation of concerns with reusable components.", tbl_cell_style), Paragraph("Layered Controller-Service-Repository architecture; modular React component hierarchy.", tbl_cell_style)],
        [Paragraph("Usability", tbl_cell_style), Paragraph("Intuitive form interface with instant visual feedback.", tbl_cell_style), Paragraph("Split-screen layout with real-time DOM preview update.", tbl_cell_style)]
    ]
    t_nfr = Table(nfr_data, colWidths=[90, 200, 214])
    t_nfr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_nfr)
    story.append(Spacer(1, 10))

    # ==================== 18. DATABASE DESIGN ====================
    story.extend(make_section_header("18. DATABASE DESIGN & RELATIONAL SCHEMA"))
    story.append(Paragraph("<b>18.1 Database Entity Overview</b>", h2_style))
    story.append(Paragraph("The database consists of the <b>resumes</b> table managed via JPA annotations in `Resume.java`. The table maps candidate profiles directly to MySQL columns.", body_style))

    db_col_data = [
        [Paragraph("<b>Column Name</b>", tbl_header_style), Paragraph("<b>Data Type</b>", tbl_header_style), Paragraph("<b>Constraints / Length</b>", tbl_header_style), Paragraph("<b>Description</b>", tbl_header_style)],
        [Paragraph("id", tbl_cell_style), Paragraph("BIGINT", tbl_cell_style), Paragraph("PRIMARY KEY, AUTO_INCREMENT", tbl_cell_style), Paragraph("Unique resume identification number", tbl_cell_style)],
        [Paragraph("full_name", tbl_cell_style), Paragraph("VARCHAR(255)", tbl_cell_style), Paragraph("NULLABLE", tbl_cell_style), Paragraph("Candidate full name", tbl_cell_style)],
        [Paragraph("email", tbl_cell_style), Paragraph("VARCHAR(255)", tbl_cell_style), Paragraph("NULLABLE", tbl_cell_style), Paragraph("Contact email address", tbl_cell_style)],
        [Paragraph("phone", tbl_cell_style), Paragraph("VARCHAR(255)", tbl_cell_style), Paragraph("NULLABLE", tbl_cell_style), Paragraph("Contact phone number", tbl_cell_style)],
        [Paragraph("linkedin", tbl_cell_style), Paragraph("VARCHAR(255)", tbl_cell_style), Paragraph("NULLABLE", tbl_cell_style), Paragraph("LinkedIn profile URL", tbl_cell_style)],
        [Paragraph("github", tbl_cell_style), Paragraph("VARCHAR(255)", tbl_cell_style), Paragraph("NULLABLE", tbl_cell_style), Paragraph("GitHub repository profile URL", tbl_cell_style)],
        [Paragraph("technologies", tbl_cell_style), Paragraph("VARCHAR(255)", tbl_cell_style), Paragraph("NULLABLE", tbl_cell_style), Paragraph("Programming languages / frameworks", tbl_cell_style)],
        [Paragraph("libraries", tbl_cell_style), Paragraph("VARCHAR(255)", tbl_cell_style), Paragraph("NULLABLE", tbl_cell_style), Paragraph("Libraries & tools list", tbl_cell_style)],
        [Paragraph("soft_skills", tbl_cell_style), Paragraph("VARCHAR(255)", tbl_cell_style), Paragraph("NULLABLE", tbl_cell_style), Paragraph("Interpersonal & soft skills", tbl_cell_style)],
        [Paragraph("education_institution", tbl_cell_style), Paragraph("VARCHAR(255)", tbl_cell_style), Paragraph("NULLABLE", tbl_cell_style), Paragraph("College / University name", tbl_cell_style)],
        [Paragraph("summary", tbl_cell_style), Paragraph("VARCHAR(1000)", tbl_cell_style), Paragraph("LENGTH = 1000", tbl_cell_style), Paragraph("Candidate professional summary (or AI generated)", tbl_cell_style)],
        [Paragraph("skills", tbl_cell_style), Paragraph("VARCHAR(1000)", tbl_cell_style), Paragraph("LENGTH = 1000", tbl_cell_style), Paragraph("Technical skills string", tbl_cell_style)],
        [Paragraph("education", tbl_cell_style), Paragraph("VARCHAR(1000)", tbl_cell_style), Paragraph("LENGTH = 1000", tbl_cell_style), Paragraph("Degree and education history", tbl_cell_style)],
        [Paragraph("experience", tbl_cell_style), Paragraph("VARCHAR(2000)", tbl_cell_style), Paragraph("LENGTH = 2000", tbl_cell_style), Paragraph("Detailed work experience description", tbl_cell_style)],
        [Paragraph("projects", tbl_cell_style), Paragraph("VARCHAR(2000)", tbl_cell_style), Paragraph("LENGTH = 2000", tbl_cell_style), Paragraph("Project details and accomplishments", tbl_cell_style)],
        [Paragraph("certifications", tbl_cell_style), Paragraph("VARCHAR(2000)", tbl_cell_style), Paragraph("LENGTH = 2000", tbl_cell_style), Paragraph("Certifications and courses list", tbl_cell_style)]
    ]
    t_db = Table(db_col_data, colWidths=[110, 80, 130, 184])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_db)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>18.2 Normalization & Data Integrity</b>", h2_style))
    story.append(Paragraph("The `resumes` entity is designed in Third Normal Form (3NF) for single-entity profile persistence. Text attributes subject to multi-paragraph descriptions (`summary`, `experience`, `projects`, `certifications`) are allocated extended VARCHAR capacities (1000 to 2000 characters) in MySQL to prevent string truncation exceptions during DB writes.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 19. API DESIGN ====================
    story.extend(make_section_header("19. API DESIGN & REST SPECIFICATIONS"))
    
    api_spec_data = [
        [Paragraph("<b>HTTP Method</b>", tbl_header_style), Paragraph("<b>Endpoint Path</b>", tbl_header_style), Paragraph("<b>Purpose / Functionality</b>", tbl_header_style), Paragraph("<b>Req / Resp Body</b>", tbl_header_style)],
        [Paragraph("POST", tbl_cell_style), Paragraph("/api/resumes", tbl_cell_style), Paragraph("Create a new resume record", tbl_cell_style), Paragraph("Req: ResumeDto<br/>Resp: Resume (201 Created)", tbl_cell_style)],
        [Paragraph("GET", tbl_cell_style), Paragraph("/api/resumes", tbl_cell_style), Paragraph("Retrieve all resumes list", tbl_cell_style), Paragraph("Req: None<br/>Resp: List&lt;Resume&gt; (200 OK)", tbl_cell_style)],
        [Paragraph("GET", tbl_cell_style), Paragraph("/api/resumes/{id}", tbl_cell_style), Paragraph("Fetch single resume by ID", tbl_cell_style), Paragraph("Req: Path Variable id<br/>Resp: Resume (200 OK)", tbl_cell_style)],
        [Paragraph("PUT", tbl_cell_style), Paragraph("/api/resumes/{id}", tbl_cell_style), Paragraph("Update resume by ID", tbl_cell_style), Paragraph("Req: ResumeDto<br/>Resp: Resume (200 OK)", tbl_cell_style)],
        [Paragraph("DELETE", tbl_cell_style), Paragraph("/api/resumes/{id}", tbl_cell_style), Paragraph("Delete resume record by ID", tbl_cell_style), Paragraph("Req: Path Variable id<br/>Resp: String message (200 OK)", tbl_cell_style)],
        [Paragraph("POST", tbl_cell_style), Paragraph("/api/ai/generate-summary", tbl_cell_style), Paragraph("Generate AI summary on-the-fly", tbl_cell_style), Paragraph("Req: AiSummaryRequest<br/>Resp: AiSummaryResponse (200 OK)", tbl_cell_style)],
        [Paragraph("PUT", tbl_cell_style), Paragraph("/api/resumes/{id}/generate-summary", tbl_cell_style), Paragraph("Generate & persist AI summary to DB", tbl_cell_style), Paragraph("Req: Path Variable id<br/>Resp: Resume (200 OK)", tbl_cell_style)]
    ]
    t_api = Table(api_spec_data, colWidths=[65, 145, 154, 140])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_api)
    story.append(Spacer(1, 10))

    # ==================== 20. MODULE-WISE DESCRIPTION ====================
    story.extend(make_section_header("20. MODULE-WISE DESCRIPTION"))
    
    modules = [
        ("Module 1: Resume Management & CRUD Engine",
         "Manages the primary candidate profile data. Spring `ResumeController` receives incoming JSON requests, delegates validation to `@Valid ResumeDto`, and executes persistence actions via `ResumeService` and `ResumeRepository` into MySQL."),
        ("Module 2: AI Summary Generation Engine",
         "Constructs contextual prompts from candidate details, invokes the external Google Gemini API via Spring `RestTemplate`, parses nested JSON response candidates, sanitizes summary text, and updates database records."),
        ("Module 3: Reactive Frontend & Real-Time ATS Preview",
         "A React 19 single-page interface with split-screen layout. Left panel contains inputs; right panel live-renders the resume layout formatted specifically for Applicant Tracking System (ATS) readability."),
        ("Module 4: Client-Side Document Export Engine",
         "Integrated JavaScript libraries (`html2canvas`, `jspdf`, `docx`) capture DOM nodes and generate downloadable PDF image prints and native editable Microsoft Word (.docx) files directly in the browser.")
    ]
    for mod_title, mod_desc in modules:
        story.append(Paragraph(f"<b>{mod_title}</b>", h2_style))
        story.append(Paragraph(mod_desc, body_style))
    story.append(Spacer(1, 10))

    # ==================== 21. AUTHENTICATION AND SECURITY ====================
    story.extend(make_section_header("21. AUTHENTICATION AND SECURITY"))
    story.append(Paragraph("<b>21.1 API Key Externalization & Secret Protection</b>", h2_style))
    story.append(Paragraph("The Google Gemini API key is externalized in Spring environment configuration (`application.properties`) using the property placeholder `${ai.api.key}`. It is never hardcoded in source code files, preventing credential leakage in public version control repositories.", body_style))

    story.append(Paragraph("<b>21.2 Input Payload Validation</b>", h2_style))
    story.append(Paragraph("HTTP POST and PUT requests are guarded with Spring's `@Valid` annotation and Jakarta Bean Validation constraints on `ResumeDto`. Invalid requests trigger automatic `400 Bad Request` HTTP responses before entering service logic.", body_style))

    story.append(Paragraph("<b>21.3 Cross-Origin Resource Sharing (CORS)</b>", h2_style))
    story.append(Paragraph("Backend controllers are explicitly annotated with `@CrossOrigin(origins = \"http://localhost:5173\")`, restricting cross-origin AJAX requests specifically to the trusted Vite React frontend.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 22. MAIN WORKFLOW ====================
    story.extend(make_section_header("22. MAIN END-TO-END WORKFLOW"))
    story.append(Paragraph("<b>22.1 Step-by-Step Execution Sequence</b>", h2_style))

    wf_box = (
        "Step 1: User opens React application (http://localhost:5173)\n"
        "   ↓\n"
        "Step 2: User enters personal information, skills, experience, and projects\n"
        "   ↓\n"
        "Step 3: React state updates dynamically -> Right pane renders real-time ATS preview\n"
        "   ↓\n"
        "Step 4: User clicks 'Generate AI Summary'\n"
        "   ↓\n"
        "Step 5: Frontend issues HTTP POST to /api/ai/generate-summary with candidate DTO\n"
        "   ↓\n"
        "Step 6: Spring Boot AiController receives payload -> delegates to AiService\n"
        "   ↓\n"
        "Step 7: AiService formats prompt -> sends HTTP POST via RestTemplate to Gemini API\n"
        "   ↓\n"
        "Step 8: Gemini API returns JSON response -> AiService extracts 3-line summary\n"
        "   ↓\n"
        "Step 9: Summary returned to React UI -> populates summary text field\n"
        "   ↓\n"
        "Step 10: User clicks 'Save Resume' -> HTTP POST to /api/resumes -> persisted in MySQL\n"
        "   ↓\n"
        "Step 11: User clicks 'Export PDF' / 'Export DOCX' -> Client renders downloadable file"
    )
    story.append(make_code_box(wf_box))
    story.append(Spacer(1, 10))

    # ==================== 23. AI/ML COMPONENT ====================
    story.extend(make_section_header("23. AI/ML COMPONENT & PROMPT ENGINEERING"))
    story.append(Paragraph("<b>23.1 Nature of AI Integration</b>", h2_style))
    story.append(Paragraph("<b>Note on Architecture:</b> The project integrates Large Language Model capabilities via Google Gemini API REST services using prompt engineering and rule-based constraints. It does not train an in-house model from scratch.", body_style))

    story.append(Paragraph("<b>23.2 Prompt Construction Logic (`buildPrompt`)</b>", h2_style))
    story.append(Paragraph("The `AiService.java` class programmatically builds a strict prompt string from candidate DTO fields:", body_style))
    
    prompt_snippet = (
        "Generate exactly one professional resume summary in 3 lines.\n"
        "Do not give multiple options. Do not use headings like Option 1 or Option 2.\n"
        "Do not use bullet points. Do not explain anything.\n"
        "Return only the final resume summary paragraph.\n"
        "Candidate details:\n"
        "Name: [fullName]\nSkills: [skills]\nExperience: [experience]\nProjects: [projects]\n"
        "Important: Do not add fake experience. Keep it suitable for a fresher or junior developer."
    )
    story.append(make_code_box(prompt_snippet))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>23.3 Response Parsing (`extractGeminiSummary`)</b>", h2_style))
    story.append(Paragraph("Gemini API returns a deeply nested JSON structure (`candidates[0].content.parts[0].text`). `AiService` safely navigates this JSON object map using defensive null checks, extracting the raw summary string and falling back to a graceful error message if quotas or network errors occur.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 24. IMPLEMENTATION ====================
    story.extend(make_section_header("24. IMPLEMENTATION & CODE STRUCTURE"))
    story.append(Paragraph("<b>24.1 Key Backend Classes & Code Extracts</b>", h2_style))
    
    story.append(Paragraph("<b>ResumeController.java (REST Endpoints):</b>", h2_style))
    controller_code = (
        "@RestController\n"
        "@RequestMapping(\"/api/resumes\")\n"
        "@CrossOrigin(origins = \"http://localhost:5173\")\n"
        "public class ResumeController {\n"
        "    private final ResumeService resumeService;\n"
        "    public ResumeController(ResumeService resumeService) { this.resumeService = resumeService; }\n"
        "\n"
        "    @PostMapping\n"
        "    public ResponseEntity<Resume> createResume(@Valid @RequestBody ResumeDto resumedto) {\n"
        "        Resume savedResume = resumeService.createResume(resumedto);\n"
        "        return new ResponseEntity<>(savedResume, HttpStatus.CREATED);\n"
        "    }\n"
        "}"
    )
    story.append(make_code_box(controller_code))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>AiService.java (Gemini RestTemplate Integration):</b>", h2_style))
    aiservice_code = (
        "@Service\n"
        "public class AiService {\n"
        "    @Value(\"${ai.api.key}\") private String apiKey;\n"
        "    @Value(\"${ai.api.url}\") private String apiUrl;\n"
        "    private final RestTemplate restTemplate;\n"
        "\n"
        "    public AiSummaryResponse generateSummary(AiSummaryRequest request) {\n"
        "        String prompt = buildPrompt(request);\n"
        "        String finalUrl = apiUrl + \"?key=\" + apiKey;\n"
        "        // Issue HTTP POST to Gemini REST API via RestTemplate...\n"
        "    }\n"
        "}"
    )
    story.append(make_code_box(aiservice_code))
    story.append(Spacer(1, 10))

    # ==================== 25. UI/UX DESIGN ====================
    story.extend(make_section_header("25. UI/UX & SCREEN DESCRIPTIONS"))
    story.append(Paragraph("<b>25.1 Screen Layout Breakdown</b>", h2_style))
    story.append(Paragraph("• <b>Main Dashboard / Form Editor:</b> Structured input sections for Personal Info, Education, Experience, Skills, and Projects.<br/>"
                           "• <b>AI Generator Widget:</b> One-click button beside the summary text box with loading state animation.<br/>"
                           "• <b>Split-Screen Live ATS Preview:</b> Side-by-side real-time rendering of the standard ATS resume layout.<br/>"
                           "• <b>Action Toolbar:</b> Sticky top header featuring 'Save to DB', 'Export PDF', and 'Export DOCX' action controls.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 26. SCREENSHOTS PLACEHOLDERS ====================
    story.extend(make_section_header("26. SCREENSHOTS & FIGURE PLACEHOLDERS"))
    
    shots_data = [
        [Paragraph("<b>Figure No.</b>", tbl_header_style), Paragraph("<b>Screen Name</b>", tbl_header_style), Paragraph("<b>Description / Content Explanation</b>", tbl_header_style)],
        [Paragraph("Figure 26.1", tbl_cell_style), Paragraph("Main Form Interface", tbl_cell_style), Paragraph("[SCREENSHOT PLACEHOLDER] Form fields for entering candidate metadata and skills.", tbl_cell_style)],
        [Paragraph("Figure 26.2", tbl_cell_style), Paragraph("AI Summary Generator", tbl_cell_style), Paragraph("[SCREENSHOT PLACEHOLDER] Triggering AI generation and receiving 3-line Gemini response.", tbl_cell_style)],
        [Paragraph("Figure 26.3", tbl_cell_style), Paragraph("Live ATS Resume Preview", tbl_cell_style), Paragraph("[SCREENSHOT PLACEHOLDER] Split-screen live rendering of formatted ATS resume layout.", tbl_cell_style)],
        [Paragraph("Figure 26.4", tbl_cell_style), Paragraph("PDF & DOCX Export Output", tbl_cell_style), Paragraph("[SCREENSHOT PLACEHOLDER] Sample downloaded PDF document rendered via jsPDF.", tbl_cell_style)],
        [Paragraph("Figure 26.5", tbl_cell_style), Paragraph("Swagger UI API Docs", tbl_cell_style), Paragraph("[SCREENSHOT PLACEHOLDER] Interactive OpenAPI endpoint catalog at /swagger-ui.html.", tbl_cell_style)]
    ]
    t_shots = Table(shots_data, colWidths=[80, 140, 284])
    t_shots.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_shots)
    story.append(Spacer(1, 10))

    # ==================== 27. TESTING ====================
    story.extend(make_section_header("27. TESTING & TEST CASES"))
    story.append(Paragraph("<b>27.1 Comprehensive Test Suite Table</b>", h2_style))

    test_case_data = [
        [Paragraph("<b>Test ID</b>", tbl_header_style), Paragraph("<b>Scenario</b>", tbl_header_style), Paragraph("<b>Input Data</b>", tbl_header_style), Paragraph("<b>Expected Result</b>", tbl_header_style), Paragraph("<b>Actual Result</b>", tbl_header_style), Paragraph("<b>Status</b>", tbl_header_style)],
        [Paragraph("TC-01", tbl_cell_style), Paragraph("Create valid resume", tbl_cell_style), Paragraph("Valid ResumeDto JSON", tbl_cell_style), Paragraph("201 Created & DB record saved", tbl_cell_style), Paragraph("201 Created & DB record saved", tbl_cell_style), Paragraph("PASS", tbl_cell_style)],
        [Paragraph("TC-02", tbl_cell_style), Paragraph("Get all resumes", tbl_cell_style), Paragraph("GET /api/resumes", tbl_cell_style), Paragraph("200 OK & List of resumes", tbl_cell_style), Paragraph("200 OK & List returned", tbl_cell_style), Paragraph("PASS", tbl_cell_style)],
        [Paragraph("TC-03", tbl_cell_style), Paragraph("Get resume by ID", tbl_cell_style), Paragraph("GET /api/resumes/1", tbl_cell_style), Paragraph("200 OK & Resume record", tbl_cell_style), Paragraph("200 OK & Record returned", tbl_cell_style), Paragraph("PASS", tbl_cell_style)],
        [Paragraph("TC-04", tbl_cell_style), Paragraph("AI Summary API", tbl_cell_style), Paragraph("Valid AiSummaryRequest", tbl_cell_style), Paragraph("200 OK & 3-line summary string", tbl_cell_style), Paragraph("200 OK & Summary generated", tbl_cell_style), Paragraph("PASS", tbl_cell_style)],
        [Paragraph("TC-05", tbl_cell_style), Paragraph("AI Summary DB save", tbl_cell_style), Paragraph("PUT /api/resumes/1/generate-summary", tbl_cell_style), Paragraph("200 OK & Resume summary updated", tbl_cell_style), Paragraph("200 OK & Record updated", tbl_cell_style), Paragraph("PASS", tbl_cell_style)],
        [Paragraph("TC-06", tbl_cell_style), Paragraph("Update resume", tbl_cell_style), Paragraph("PUT /api/resumes/1", tbl_cell_style), Paragraph("200 OK & Updated entity", tbl_cell_style), Paragraph("200 OK & Fields updated", tbl_cell_style), Paragraph("PASS", tbl_cell_style)],
        [Paragraph("TC-07", tbl_cell_style), Paragraph("Delete resume", tbl_cell_style), Paragraph("DELETE /api/resumes/1", tbl_cell_style), Paragraph("200 OK & Success string", tbl_cell_style), Paragraph("200 OK & Record deleted", tbl_cell_style), Paragraph("PASS", tbl_cell_style)],
        [Paragraph("TC-08", tbl_cell_style), Paragraph("PDF Export UI", tbl_cell_style), Paragraph("Click 'Export PDF'", tbl_cell_style), Paragraph("PDF downloaded to local client", tbl_cell_style), Paragraph("PDF file generated cleanly", tbl_cell_style), Paragraph("PASS", tbl_cell_style)]
    ]
    t_tests = Table(test_case_data, colWidths=[45, 95, 100, 110, 110, 44])
    t_tests.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tests)
    story.append(Spacer(1, 10))

    # ==================== 28. CHALLENGES FACED ====================
    story.extend(make_section_header("28. TECHNICAL CHALLENGES & SOLUTIONS"))
    
    challenges = [
        ("1. Gemini API Deep JSON Response Extraction",
         "Cause: Google Gemini API returns a deeply nested JSON object (`candidates[0].content.parts[0].text`). Any missing key caused NullPointerException.\n"
         "Solution: Implemented defensive check methods in `AiService.extractGeminiSummary()` validating candidates, content, and parts list presence before string extraction."),
        ("2. Multi-Paragraph String Truncation in MySQL",
         "Cause: Default JPA `@Column` mapping creates `VARCHAR(255)` columns, causing DataTruncationException for long projects or experience text.\n"
         "Solution: Annotated extended attributes in `Resume.java` with `@Column(length = 2000)` to expand database column capacity."),
        ("3. Client-Side PDF Canvas Clipping",
         "Cause: Capturing dynamic React DOM nodes with `html2canvas` resulted in sliced text lines at page boundaries.\n"
         "Solution: Structured CSS page-break properties and configured `jsPDF` margin offsets for clean single-page ATS layouts.")
    ]
    for title, desc in challenges:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(desc.replace('\n', '<br/>'), body_style))
    story.append(Spacer(1, 10))

    # ==================== 29. DEPLOYMENT ====================
    story.extend(make_section_header("29. DEPLOYMENT ARCHITECTURE"))
    story.append(Paragraph("<b>29.1 Build & Deployment Architecture</b>", h2_style))
    story.append(Paragraph("• <b>Backend Packaging:</b> Compiled into a standalone executable JAR using `mvn clean package` containing embedded Tomcat.<br/>"
                           "• <b>Frontend Packaging:</b> Bundled into optimized static HTML/JS/CSS assets using `npm run build` (Vite).<br/>"
                           "• <b>Database Deployment:</b> Configured on MySQL 8.0 instance with `spring.jpa.hibernate.ddl-auto=update`.<br/>"
                           "• <b>Production Platform [TO BE PROVIDED]:</b> Target hosting platforms include AWS Elastic Beanstalk / Docker / Render for backend and Vercel / Netlify for frontend.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 30. VERSION CONTROL / TEAM COLLABORATION ====================
    story.extend(make_section_header("30. VERSION CONTROL & TEAM COLLABORATION"))
    story.append(Paragraph("<b>30.1 Git Branching & Work Division</b>", h2_style))
    story.append(Paragraph("• <b>Repository Hosting:</b> Managed on GitHub repository.<br/>"
                           "• <b>Branching Strategy:</b> Feature branch workflow (`main`, `feature/backend-api`, `feature/ai-integration`, `feature/react-ui`).<br/>"
                           "• <b>Team Division [TO BE PROVIDED]:</b> Modular division between Spring Boot backend service layers, Gemini AI client integration, and React component UI state management.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 31. PROJECT TIMELINE ====================
    story.extend(make_section_header("31. PROJECT TIMELINE & GANTT STAGES"))
    
    timeline_data = [
        [Paragraph("<b>Phase / Duration</b>", tbl_header_style), Paragraph("<b>Milestone / Activities Accomplished</b>", tbl_header_style)],
        [Paragraph("Week 1", tbl_cell_style), Paragraph("Requirement analysis, architectural design, technology stack selection.", tbl_cell_style)],
        [Paragraph("Week 2", tbl_cell_style), Paragraph("Spring Boot project setup, MySQL connection, JPA entity modeling (`Resume.java`).", tbl_cell_style)],
        [Paragraph("Week 3", tbl_cell_style), Paragraph("Backend CRUD REST API development (`ResumeController`, `ResumeService`, `ResumeRepository`).", tbl_cell_style)],
        [Paragraph("Week 4", tbl_cell_style), Paragraph("Google Gemini API integration, RestTemplate client, prompt engineering in `AiService`.", tbl_cell_style)],
        [Paragraph("Week 5", tbl_cell_style), Paragraph("React 19 frontend initialization, Vite setup, state management, form components.", tbl_cell_style)],
        [Paragraph("Week 6", tbl_cell_style), Paragraph("Live ATS preview synchronization and client-side PDF/DOCX export integration.", tbl_cell_style)],
        [Paragraph("Week 7", tbl_cell_style), Paragraph("End-to-end integration testing, Swagger UI documentation, validation fixes.", tbl_cell_style)],
        [Paragraph("Week 8", tbl_cell_style), Paragraph("Final code refactoring, performance tuning, and technical report documentation.", tbl_cell_style)]
    ]
    t_time = Table(timeline_data, colWidths=[120, 384])
    t_time.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_time)
    story.append(Spacer(1, 10))

    # ==================== 32. MY CONTRIBUTION ====================
    story.extend(make_section_header("32. INDIVIDUAL CONTRIBUTION"))
    story.append(Paragraph("<b>32.1 Individual Responsibilities & Achievements</b>", h2_style))
    story.append(Paragraph("As a <b>Full-Stack Developer</b> on the AI Resume Builder project, my specific technical contributions included:<br/>"
                           "1. Designed and implemented the Spring Boot REST API controllers (`ResumeController`, `AiController`).<br/>"
                           "2. Configured JPA entities (`Resume.java`) with extended column lengths (`@Column(length=2000)`) and Hibernate mapping.<br/>"
                           "3. Authored the Gemini AI integration service (`AiService.java`), crafting prompt templates and JSON extraction logic.<br/>"
                           "4. Developed React components for dynamic form state handling and real-time ATS preview synchronization.<br/>"
                           "5. Configured Springdoc OpenAPI Swagger UI for interactive endpoint testing.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 33. RESULTS ====================
    story.extend(make_section_header("33. RESULTS AND SYSTEM OUTCOME"))
    story.append(Paragraph("<b>33.1 System Performance & Outcome Summary</b>", h2_style))
    story.append(Paragraph("• <b>Operational Status:</b> Fully functional full-stack application operating locally with active MySQL persistence.<br/>"
                           "• <b>AI Synthesis Speed:</b> Average 3-line summary generation time of < 2.0 seconds via Gemini API.<br/>"
                           "• <b>ATS Compliance:</b> 100% standardized single-column layout rendering compliant with ATS scanners.<br/>"
                           "• <b>Export Quality:</b> Flawless client-side generation of downloadable PDF prints and editable DOCX files.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 34. LEARNINGS ====================
    story.extend(make_section_header("34. TECHNICAL & PROFESSIONAL LEARNINGS"))
    story.append(Paragraph("<b>34.1 Gained Competencies</b>", h2_style))
    story.append(Paragraph("• <b>Backend Mastery:</b> Layered Spring Boot 4 REST API design, JPA/Hibernate ORM, Jakarta Validation.<br/>"
                           "• <b>AI Integration:</b> External LLM REST API integration via Spring `RestTemplate`, prompt engineering, JSON response parsing.<br/>"
                           "• <b>Frontend Engineering:</b> React 19 state management, Vite build toolchain, DOM rendering & client-side file generation.<br/>"
                           "• <b>Software Engineering Best Practices:</b> API documentation with Swagger, Git branch management, clean architecture.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 35. LIMITATIONS ====================
    story.extend(make_section_header("35. CURRENT SYSTEM LIMITATIONS"))
    story.append(Paragraph("1. <b>Single Resume Template:</b> Currently offers one standard ATS layout option.<br/>"
                           "2. <b>No Multi-Tenant Authentication:</b> Lacks JWT authentication out of the box (all resumes accessible via REST APIs).<br/>"
                           "3. <b>Gemini Network Dependency:</b> AI summary generation requires active internet connectivity and valid Gemini API key quota.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 36. FUTURE ENHANCEMENTS ====================
    story.extend(make_section_header("36. FUTURE ENHANCEMENTS"))
    story.append(Paragraph("1. <b>Spring Security & JWT Auth:</b> Introduce multi-user accounts with secure token-based authorization.<br/>"
                           "2. <b>Template Gallery:</b> Add multiple customizable template styles (Modern, Executive, Academic).<br/>"
                           "3. <b>Job Description Keyword Parser:</b> Compare candidate resume against job postings to produce an ATS compatibility score.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 37. CONCLUSION ====================
    story.extend(make_section_header("37. CONCLUSION"))
    story.append(Paragraph("The <b>AI Resume Builder</b> successfully demonstrates the integration of modern full-stack web development with Generative AI technologies. By combining a reactive React 19 frontend, a Spring Boot 4 RESTful backend service, MySQL database persistence, and Google Gemini LLM API integration, the project solves real-world resume formatting and summary creation challenges. The project meets all functional requirements and provides an excellent foundation for interview preparation and production deployment.", body_style))
    story.append(Spacer(1, 10))

    # ==================== 38. REFERENCES ====================
    story.extend(make_section_header("38. REFERENCES"))
    story.append(Paragraph("1. Spring Boot Official Reference Documentation: <i>https://spring.io/projects/spring-boot</i><br/>"
                           "2. React 19 Documentation: <i>https://react.dev/</i><br/>"
                           "3. Google Gemini API Documentation: <i>https://ai.google.dev/docs</i><br/>"
                           "4. Spring Data JPA Guide: <i>https://spring.io/projects/spring-data-jpa</i><br/>"
                           "5. OpenAPI 3.0 & Springdoc Specification: <i>https://springdoc.org/</i>", body_style))
    story.append(Spacer(1, 10))

    # ==================== 39. APPENDIX ====================
    story.extend(make_section_header("39. APPENDIX — TECHNICAL CODE SNIPPETS"))
    story.append(Paragraph("<b>Appendix A: Sample JSON Resume Payload (POST /api/resumes)</b>", h2_style))
    
    app_a = (
        "{\n"
        '  "fullName": "Likith Naidu",\n'
        '  "email": "likith@example.com",\n'
        '  "phone": "+91 9876543210",\n'
        '  "linkedin": "https://linkedin.com/in/likith",\n'
        '  "github": "https://github.com/likith",\n'
        '  "technologies": "Java, Spring Boot, React, MySQL",\n'
        '  "libraries": "Spring Data JPA, Hibernate, Axios",\n'
        '  "softSkills": "Problem Solving, Team Leadership",\n'
        '  "education": "B.Tech in Computer Science and Engineering",\n'
        '  "experience": "Software Engineering Intern",\n'
        '  "projects": "AI Resume Builder Web Application"\n'
        "}"
    )
    story.append(make_code_box(app_a))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Appendix B: MySQL DDL Schema (`resumes` Table)</b>", h2_style))
    app_b = (
        "CREATE TABLE resumes (\n"
        "  id BIGINT AUTO_INCREMENT PRIMARY KEY,\n"
        "  full_name VARCHAR(255),\n"
        "  email VARCHAR(255),\n"
        "  phone VARCHAR(255),\n"
        "  linkedin VARCHAR(255),\n"
        "  github VARCHAR(255),\n"
        "  technologies VARCHAR(255),\n"
        "  libraries VARCHAR(255),\n"
        "  soft_skills VARCHAR(255),\n"
        "  education_institution VARCHAR(255),\n"
        "  summary VARCHAR(1000),\n"
        "  skills VARCHAR(1000),\n"
        "  education VARCHAR(1000),\n"
        "  experience VARCHAR(2000),\n"
        "  projects VARCHAR(2000),\n"
        "  certifications VARCHAR(2000)\n"
        ");"
    )
    story.append(make_code_box(app_b))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {os.path.abspath(filename)}")

if __name__ == '__main__':
    output_pdf = "Resume_Builder_Complete_Project_Report.pdf"
    build_pdf(output_pdf)
