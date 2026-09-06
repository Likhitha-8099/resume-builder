package com.resumebuilder.resume_builder.controller;

import java.util.List;
import com.resumebuilder.resume_builder.dto.ResumeDto;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.resumebuilder.resume_builder.model.Resume;
import com.resumebuilder.resume_builder.service.ResumeService;

import io.swagger.v3.oas.annotations.Operation;
import jakarta.validation.Valid;


@RestController
@RequestMapping("/api/resumes")
@CrossOrigin(origins = "http://localhost:5173")
public class ResumeController {
	
	
	private final ResumeService resumeService;
	public ResumeController(ResumeService resumeService) {
        this.resumeService = resumeService;
    }
     
	@Operation(summary="Create a new resume")
    @PostMapping
    public ResponseEntity<Resume> createResume(@Valid @RequestBody ResumeDto resumedto) {
        Resume savedResume =resumeService.createResume(resumedto);
        return new ResponseEntity<>(savedResume,HttpStatus.CREATED);
    }
	@Operation(summary = "Get all resumes")
    @GetMapping
    public ResponseEntity<List<Resume>> getResumes(){
    	
    	List<Resume> get=resumeService.getResumes();
    	return new ResponseEntity<>(get,HttpStatus.OK);
    	
    }
	@Operation(summary = "Get a resume by id")
    @GetMapping("/{id}")
    public ResponseEntity<Resume> resumeById(@Valid @PathVariable Long id) {
    	 Resume savedResume =resumeService.resumeById(id);
    	 return new ResponseEntity<>(savedResume,HttpStatus.OK);
    }
	@Operation(summary = "Update a resume by id")
    @PutMapping("/{id}")
    public ResponseEntity<Resume> updateById(@PathVariable Long id,@Valid @RequestBody ResumeDto resumedto) {
    	Resume update =resumeService.updateById(id, resumedto);
    	return new ResponseEntity<>(update,HttpStatus.OK);
    }
	@Operation(summary = "Delete a resume by id")
    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteById(@PathVariable Long id) {
    	String delete=resumeService.deleteById(id);
    	return new ResponseEntity<>(delete,HttpStatus.OK);
    }
	@Operation(summary = "Generate and save AI summary for a resume")
    @PutMapping("/{id}/generate-summary")
    public ResponseEntity<Resume> generateAndSaveSummary(@PathVariable Long id) {
        Resume updatedResume = resumeService.generateAndSaveSummary(id);
        return new ResponseEntity<>(updatedResume, HttpStatus.OK);
    }

}
