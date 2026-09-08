package com.resumebuilder.resume_builder.service;

import java.util.Collections;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.resumebuilder.resume_builder.dto.JobFitResponseDto;

@Service
public class JobFitService {

    private static final Logger logger = LoggerFactory.getLogger(JobFitService.class);

    private final TextExtractionService textExtractionService;
    private final AiService aiService;

    public JobFitService(TextExtractionService textExtractionService, AiService aiService) {
        this.textExtractionService = textExtractionService;
        this.aiService = aiService;
    }

    public JobFitResponseDto analyzeJobFit(MultipartFile resumeFile,
                                           MultipartFile jobDescriptionFile,
                                           String jobDescriptionText) {

        logger.info("[JOB-FIT] Request received");

        if (resumeFile == null || resumeFile.isEmpty()) {
            throw new IllegalArgumentException("Resume PDF file is required.");
        }

        // Step 1: Extract Resume PDF Text
        String resumeText = textExtractionService.extractTextFromPdf(resumeFile, "Resume");

        // Step 2: Extract or Read Job Description Text
        String jdText = "";
        if (jobDescriptionFile != null && !jobDescriptionFile.isEmpty()) {
            jdText = textExtractionService.extractTextFromPdf(jobDescriptionFile, "Job Description");
        } else if (jobDescriptionText != null && !jobDescriptionText.trim().isEmpty()) {
            logger.info("[JOB-FIT] Using pasted Job Description text");
            jdText = jobDescriptionText.trim();
        } else {
            throw new IllegalArgumentException("Please upload a Job Description PDF or paste Job Description text.");
        }

        if (jdText.isEmpty()) {
            throw new IllegalArgumentException("Job Description text could not be extracted or is empty.");
        }

        // Safety: Truncate excessively long text to stay safely under Groq's 8,000 TPM limit
        if (resumeText.length() > 10000) {
            logger.info("[JOB-FIT] Truncating Resume text from " + resumeText.length() + " to 10000 characters for token safety");
            resumeText = resumeText.substring(0, 10000);
        }
        if (jdText.length() > 6000) {
            logger.info("[JOB-FIT] Truncating Job Description text from " + jdText.length() + " to 6000 characters for token safety");
            jdText = jdText.substring(0, 6000);
        }


        // Step 3: Invoke Groq AI for Semantic Analysis
        Map<String, Object> aiAnalysis = aiService.analyzeJobFitSemantic(resumeText, jdText);
        logger.info("[JOB-FIT] AI response parsed");

        // Step 4: Extract sub-scores safely from AI analysis
        int skillsScore = parseScore(aiAnalysis.get("skillsScore"));
        int keywordScore = parseScore(aiAnalysis.get("keywordScore"));
        int experienceScore = parseScore(aiAnalysis.get("experienceScore"));
        int educationScore = parseScore(aiAnalysis.get("educationScore"));
        int projectScore = parseScore(aiAnalysis.get("projectScore"));

        // Step 5: Calculate Deterministic Weighted Score in Spring Boot
        // Formula: Skills 40% + Keywords 25% + Experience 15% + Education 10% + Projects 10%
        double weightedScore = (skillsScore * 0.40)
                + (keywordScore * 0.25)
                + (experienceScore * 0.15)
                + (educationScore * 0.10)
                + (projectScore * 0.10);

        int finalMatchScore = (int) Math.round(weightedScore);
        // Clamp score between 0 and 100
        finalMatchScore = Math.max(0, Math.min(100, finalMatchScore));

        logger.info("[JOB-FIT] Score calculated: " + finalMatchScore + " / 100");

        // Step 6: Construct Final Response DTO
        JobFitResponseDto response = new JobFitResponseDto();
        response.setMatchScore(finalMatchScore);

        JobFitResponseDto.ScoreBreakdown breakdown = new JobFitResponseDto.ScoreBreakdown(
                skillsScore, keywordScore, experienceScore, educationScore, projectScore
        );
        response.setScoreBreakdown(breakdown);

        response.setCalculationExplanation(
                String.format("Calculated via weighted formula: Skills (40%%: %d) + Keywords (25%%: %d) + Experience (15%%: %d) + Education (10%%: %d) + Projects (10%%: %d)",
                        skillsScore, keywordScore, experienceScore, educationScore, projectScore)
        );

        response.setMatchedSkills(toStringList(aiAnalysis.get("matchedSkills")));
        response.setPartialMatches(toStringList(aiAnalysis.get("partialMatches")));
        response.setMissingSkills(toStringList(aiAnalysis.get("missingSkills")));
        response.setResumeStrengths(toStringList(aiAnalysis.get("resumeStrengths")));
        response.setRecommendations(toStringList(aiAnalysis.get("recommendations")));
        response.setMatchSummary(aiAnalysis.get("matchSummary") != null ? aiAnalysis.get("matchSummary").toString() : "");

        logger.info("[JOB-FIT] Response returned");
        return response;
    }

    private int parseScore(Object scoreObj) {
        if (scoreObj == null) return 0;
        try {
            if (scoreObj instanceof Number) {
                return ((Number) scoreObj).intValue();
            }
            return Integer.parseInt(scoreObj.toString().trim());
        } catch (Exception ex) {
            return 0;
        }
    }

    @SuppressWarnings("unchecked")
    private List<String> toStringList(Object obj) {
        if (obj instanceof List) {
            return ((List<?>) obj).stream()
                    .filter(item -> item != null && !item.toString().trim().isEmpty())
                    .map(Object::toString)
                    .toList();
        }
        return Collections.emptyList();
    }
}
