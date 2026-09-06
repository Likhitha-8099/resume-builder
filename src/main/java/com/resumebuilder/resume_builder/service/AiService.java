package com.resumebuilder.resume_builder.service;

import java.util.List;
import java.util.Map;

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

import com.resumebuilder.resume_builder.dto.AiSummaryRequest;
import com.resumebuilder.resume_builder.dto.AiSummaryResponse;

@Service
public class AiService {

    @Value("${ai.api.key}")
    private String apiKey;

    @Value("${ai.api.url}")
    private String apiUrl;

    @Value("${ai.api.model}")
    private String model;

    private final RestTemplate restTemplate;

    public AiService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public AiSummaryResponse generateSummary(AiSummaryRequest request) {

        try {
            String prompt = buildPrompt(request);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            Map<String, Object> body = Map.of(
                    "contents", List.of(
                            Map.of(
                                    "parts", List.of(
                                            Map.of("text", prompt)
                                    )
                            )
                    )
            );

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(body, headers);

            String finalUrl = apiUrl + "?key=" + apiKey;

            ResponseEntity<Map<String, Object>> response = restTemplate.exchange(
                    finalUrl,
                    HttpMethod.POST,
                    entity,
                    new ParameterizedTypeReference<Map<String, Object>>() {
                    }
            );

            String summary = extractGeminiSummary(response.getBody());

            return new AiSummaryResponse(summary);

        } catch (HttpClientErrorException | HttpServerErrorException ex) {

            System.out.println("Gemini API Status: " + ex.getStatusCode());
            System.out.println("Gemini API Error Body: " + ex.getResponseBodyAsString());

            return new AiSummaryResponse(
                    "AI service error: " + ex.getStatusCode() + ". Please check your Gemini API key, model, or quota."
            );

        } catch (Exception ex) {

            System.out.println("Unexpected AI Error: " + ex.getMessage());

            return new AiSummaryResponse("Unable to generate summary right now. Please try again.");
        }
    }

    private String buildPrompt(AiSummaryRequest request) {
        return "Generate exactly one professional resume summary in 3 lines.\n"
                + "Do not give multiple options."
                + "Do not use headings like Option 1 or Option 2."
                + "Do not use bullet points."
                + "Do not explain anything."
                + "Return only the final resume summary paragraph."
                + "Candidate details:"
                + "Name: " + request.getFullName() + "\n"
                + "Skills: " + request.getSkills() + "\n"
                + "Experience: " + request.getExperience() + "\n"
                + "Projects: " + request.getProjects() + "\n\n"
                + "Important: Do not add fake experience. Keep it suitable for a fresher or junior developer.";
    }

    private String extractGeminiSummary(Map<String, Object> responseBody) {

        if (responseBody == null) {
            return "Unable to generate summary. Please try again.";
        }

        List<?> candidates = (List<?>) responseBody.get("candidates");

        if (candidates == null || candidates.isEmpty()) {
            return "Unable to generate summary. Please try again.";
        }

        Map<?, ?> firstCandidate = (Map<?, ?>) candidates.get(0);

        if (firstCandidate == null || firstCandidate.get("content") == null) {
            return "Unable to generate summary. Please try again.";
        }

        Map<?, ?> content = (Map<?, ?>) firstCandidate.get("content");

        if (content.get("parts") == null) {
            return "Unable to generate summary. Please try again.";
        }

        List<?> parts = (List<?>) content.get("parts");

        if (parts == null || parts.isEmpty()) {
            return "Unable to generate summary. Please try again.";
        }

        Map<?, ?> firstPart = (Map<?, ?>) parts.get(0);

        if (firstPart.get("text") == null) {
            return "Unable to generate summary. Please try again.";
        }

        return firstPart.get("text").toString();
    }
}