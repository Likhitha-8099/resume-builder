package com.resumebuilder.resume_builder.service;

import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.resumebuilder.resume_builder.dto.AiSummaryRequest;
import com.resumebuilder.resume_builder.dto.AiSummaryResponse;

@Service
public class AiService {

    private static final Logger logger = LoggerFactory.getLogger(AiService.class);

    @Value("${groq.api.key:}")
    private String apiKey;

    @Value("${groq.api.url:https://api.groq.com/openai/v1/chat/completions}")
    private String apiUrl;

    @Value("${groq.api.model:llama-3.3-70b-versatile}")
    private String model;

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    public AiService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
        this.objectMapper = new ObjectMapper();
    }

    public AiSummaryResponse generateSummary(AiSummaryRequest request) {
        try {
            String prompt = buildSummaryPrompt(request);
            String content = callGroqApi("You are an expert resume writer. Generate concise, professional resume summaries.", prompt);
            return new AiSummaryResponse(content);
        } catch (Exception ex) {
            logger.error("[AI-SUMMARY] Error generating summary: " + ex.getMessage(), ex);
            return new AiSummaryResponse("Unable to generate summary right now. Please try again.");
        }
    }

    public Map<String, Object> analyzeJobFitSemantic(String resumeText, String jdText) {
        logger.info("[JOB-FIT] Calling Groq for semantic analysis");

        String systemPrompt = "You are an expert AI HR Specialist and Applicant Tracking System (ATS) evaluator.\n"
                + "Analyze the candidate's Resume against the Job Description.\n"
                + "CRITICAL RULE: DO NOT fabricate, invent, or hallucinate any skills, experience, or achievements. Only evaluate data explicitly present in the provided texts.\n"
                + "You MUST return ONLY a valid, raw JSON object (with no markdown backticks, no markdown code block markers, no explanatory prefix or suffix).\n"
                + "The JSON MUST follow this EXACT structure:\n"
                + "{\n"
                + "  \"skillsScore\": <integer 0-100 representing technical skill alignment>,\n"
                + "  \"keywordScore\": <integer 0-100 representing job requirement/keyword density>,\n"
                + "  \"experienceScore\": <integer 0-100 representing relevant work experience alignment>,\n"
                + "  \"educationScore\": <integer 0-100 representing education requirement alignment>,\n"
                + "  \"projectScore\": <integer 0-100 representing project relevance to job domain>,\n"
                + "  \"matchedSkills\": [<array of string exact skill matches found in both>],\n"
                + "  \"partialMatches\": [<array of string transferable/related skills>],\n"
                + "  \"missingSkills\": [<array of string required skills missing from candidate resume>],\n"
                + "  \"resumeStrengths\": [<array of string key candidate highlights relevant to JD>],\n"
                + "  \"recommendations\": [<array of string actionable improvements for candidate>],\n"
                + "  \"matchSummary\": \"<2-3 sentence overview of candidate suitability for this position>\"\n"
                + "}";

        String userPrompt = "RESUME TEXT:\n" + resumeText + "\n\n"
                + "JOB DESCRIPTION TEXT:\n" + jdText;

        String rawResponse = callGroqApi(systemPrompt, userPrompt);
        logger.info("[JOB-FIT] Groq response received");

        return parseJsonResponse(rawResponse);
    }

    private String callGroqApi(String systemMessage, String userMessage) {
        if (apiKey == null || apiKey.trim().isEmpty()) {
            throw new IllegalStateException("GROQ_API_KEY is not configured in environment.");
        }

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.setBearerAuth(apiKey.trim());

        Map<String, Object> requestBody = Map.of(
                "model", model,
                "messages", List.of(
                        Map.of("role", "system", "content", systemMessage),
                        Map.of("role", "user", "content", userMessage)
                ),
                "temperature", 0.2
        );

        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

        try {
            ResponseEntity<Map<String, Object>> response = restTemplate.exchange(
                    apiUrl,
                    HttpMethod.POST,
                    entity,
                    new ParameterizedTypeReference<Map<String, Object>>() {}
            );

            return extractContentFromGroqResponse(response.getBody());

        } catch (HttpClientErrorException | HttpServerErrorException ex) {
            logger.error("Groq API HTTP Error (" + ex.getStatusCode() + "): " + ex.getResponseBodyAsString());
            throw new RuntimeException("Groq API error (" + ex.getStatusCode() + "): " + ex.getResponseBodyAsString());
        } catch (Exception ex) {
            logger.error("Unexpected Groq API Error: " + ex.getMessage(), ex);
            throw new RuntimeException("AI service error: " + ex.getMessage());
        }
    }

    private String extractContentFromGroqResponse(Map<String, Object> responseBody) {
        if (responseBody == null) {
            throw new RuntimeException("Empty response received from Groq API.");
        }

        List<?> choices = (List<?>) responseBody.get("choices");
        if (choices == null || choices.isEmpty()) {
            throw new RuntimeException("No choices returned from Groq API.");
        }

        Map<?, ?> firstChoice = (Map<?, ?>) choices.get(0);
        if (firstChoice == null || firstChoice.get("message") == null) {
            throw new RuntimeException("Invalid choice structure from Groq API.");
        }

        Map<?, ?> message = (Map<?, ?>) firstChoice.get("message");
        Object content = message.get("content");

        if (content == null) {
            throw new RuntimeException("Null content in Groq API response message.");
        }

        return content.toString().trim();
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> parseJsonResponse(String rawContent) {
        try {
            String cleaned = rawContent;
            if (cleaned.startsWith("```json")) {
                cleaned = cleaned.substring(7);
            } else if (cleaned.startsWith("```")) {
                cleaned = cleaned.substring(3);
            }
            if (cleaned.endsWith("```")) {
                cleaned = cleaned.substring(0, cleaned.length() - 3);
            }
            cleaned = cleaned.trim();

            return objectMapper.readValue(cleaned, Map.class);
        } catch (Exception ex) {
            logger.error("[JOB-FIT] Failed to parse JSON from AI response: " + rawContent, ex);
            throw new RuntimeException("Failed to parse structured analysis from Groq response.");
        }
    }

    private String buildSummaryPrompt(AiSummaryRequest request) {
        return "Generate exactly one professional resume summary in 3 lines.\n"
                + "Do not give multiple options. Do not use bullet points or headings.\n"
                + "Candidate Name: " + request.getFullName() + "\n"
                + "Skills: " + request.getSkills() + "\n"
                + "Experience: " + request.getExperience() + "\n"
                + "Projects: " + request.getProjects();
    }
}