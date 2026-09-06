package com.resumebuilder.resume_builder.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.resumebuilder.resume_builder.dto.AiSummaryRequest;
import com.resumebuilder.resume_builder.dto.AiSummaryResponse;
import com.resumebuilder.resume_builder.service.AiService;

import io.swagger.v3.oas.annotations.Operation;

@RestController
@RequestMapping("/api/ai")
@CrossOrigin(origins = "http://localhost:5173")
public class AiController {
	
	private final AiService aiService;

    public AiController(AiService aiService) {
        this.aiService = aiService;
    }
    @Operation(summary = "Generate AI resume summary")
    @PostMapping("/generate-summary")
    public ResponseEntity<AiSummaryResponse> generateSummary(@RequestBody AiSummaryRequest request) {
    	
        AiSummaryResponse response = aiService.generateSummary(request);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

}
