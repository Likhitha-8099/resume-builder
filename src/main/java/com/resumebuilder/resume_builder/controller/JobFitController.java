package com.resumebuilder.resume_builder.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.resumebuilder.resume_builder.dto.JobFitResponseDto;
import com.resumebuilder.resume_builder.service.JobFitService;

import io.swagger.v3.oas.annotations.Operation;

@RestController
@RequestMapping("/api/job-fit")
@CrossOrigin(origins = "http://localhost:5173")
public class JobFitController {

    private final JobFitService jobFitService;

    public JobFitController(JobFitService jobFitService) {
        this.jobFitService = jobFitService;
    }

    @Operation(summary = "Analyze Job Fit between Resume PDF and Job Description PDF/Text")
    @PostMapping(value = "/analyze", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<JobFitResponseDto> analyzeJobFit(
            @RequestParam("resumeFile") MultipartFile resumeFile,
            @RequestParam(value = "jobDescriptionFile", required = false) MultipartFile jobDescriptionFile,
            @RequestParam(value = "jobDescriptionText", required = false) String jobDescriptionText) {

        JobFitResponseDto response = jobFitService.analyzeJobFit(
                resumeFile, jobDescriptionFile, jobDescriptionText);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }
}
