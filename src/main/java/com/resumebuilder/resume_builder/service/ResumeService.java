package com.resumebuilder.resume_builder.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.resumebuilder.resume_builder.dto.AiSummaryRequest;
import com.resumebuilder.resume_builder.dto.AiSummaryResponse;
import com.resumebuilder.resume_builder.dto.ResumeDto;
import com.resumebuilder.resume_builder.exception.ResumeNotFoundException;
import com.resumebuilder.resume_builder.model.Resume;
import com.resumebuilder.resume_builder.repository.ResumeRepository;

@Service
public class ResumeService {

    private final ResumeRepository resumeRepository;
    private final AiService aiService;

    public ResumeService(ResumeRepository resumeRepository, AiService aiService) {
        this.resumeRepository = resumeRepository;
        this.aiService = aiService;
    }

    public Resume createResume(ResumeDto resumeDto) {

        Resume resume = new Resume();

        resume.setFullName(resumeDto.getFullName());
        resume.setEmail(resumeDto.getEmail());
        resume.setPhone(resumeDto.getPhone());
        resume.setLinkedin(resumeDto.getLinkedin());
        resume.setGithub(resumeDto.getGithub());
        resume.setSummary(resumeDto.getSummary());
        resume.setSkills(resumeDto.getSkills());
        resume.setEducation(resumeDto.getEducation());
        resume.setExperience(resumeDto.getExperience());
        resume.setProjects(resumeDto.getProjects());
        resume.setTechnologies(resumeDto.getTechnologies());
        resume.setLibraries(resumeDto.getLibraries());
        resume.setSoftSkills(resumeDto.getSoftSkills());
        resume.setCertifications(resumeDto.getCertifications());
        resume.setEducationInstitution(resumeDto.getEducationInstitution());

        return resumeRepository.save(resume);
    }

    public List<Resume> getResumes() {
        return resumeRepository.findAll();
    }

    public Resume resumeById(Long id) {
        return resumeRepository.findById(id)
                .orElseThrow(() -> new ResumeNotFoundException("Resume not found with id: " + id));
    }

    public Resume updateById(Long id, ResumeDto resumeDto) {

        Resume existingResume = resumeRepository.findById(id)
                .orElseThrow(() -> new ResumeNotFoundException("Resume not found with id: " + id));

        existingResume.setFullName(resumeDto.getFullName());
        existingResume.setEmail(resumeDto.getEmail());
        existingResume.setPhone(resumeDto.getPhone());
        existingResume.setLinkedin(resumeDto.getLinkedin());
        existingResume.setGithub(resumeDto.getGithub());
        existingResume.setSummary(resumeDto.getSummary());
        existingResume.setSkills(resumeDto.getSkills());
        existingResume.setEducation(resumeDto.getEducation());
        existingResume.setExperience(resumeDto.getExperience());
        existingResume.setProjects(resumeDto.getProjects());
        existingResume.setTechnologies(resumeDto.getTechnologies());
        existingResume.setLibraries(resumeDto.getLibraries());
        existingResume.setSoftSkills(resumeDto.getSoftSkills());
        existingResume.setCertifications(resumeDto.getCertifications());
        existingResume.setEducationInstitution(resumeDto.getEducationInstitution());

        return resumeRepository.save(existingResume);
    }

    public String deleteById(Long id) {

        Resume resume = resumeRepository.findById(id)
                .orElseThrow(() -> new ResumeNotFoundException("Resume not found with id: " + id));

        resumeRepository.delete(resume);

        return "Resume deleted successfully with id: " + id;
    }

    public Resume generateAndSaveSummary(Long id) {

        Resume resume = resumeRepository.findById(id)
                .orElseThrow(() -> new ResumeNotFoundException("Resume not found with id: " + id));

        AiSummaryRequest request = new AiSummaryRequest();

        request.setFullName(resume.getFullName());

        String combinedSkills = "";

        if (resume.getSkills() != null && !resume.getSkills().isBlank()) {
            combinedSkills += resume.getSkills();
        }

        if (resume.getTechnologies() != null && !resume.getTechnologies().isBlank()) {
            combinedSkills += ", Technologies: " + resume.getTechnologies();
        }

        if (resume.getLibraries() != null && !resume.getLibraries().isBlank()) {
            combinedSkills += ", Libraries: " + resume.getLibraries();
        }

        if (resume.getSoftSkills() != null && !resume.getSoftSkills().isBlank()) {
            combinedSkills += ", Soft Skills: " + resume.getSoftSkills();
        }

        if (resume.getCertifications() != null && !resume.getCertifications().isBlank()) {
            combinedSkills += ", Certifications: " + resume.getCertifications();
        }

        if (resume.getEducationInstitution() != null && !resume.getEducationInstitution().isBlank()) {
            combinedSkills += ", Education Institution: " + resume.getEducationInstitution();
        }

        request.setSkills(combinedSkills);
        request.setExperience(resume.getExperience());
        request.setProjects(resume.getProjects());

        AiSummaryResponse response = aiService.generateSummary(request);

        String generatedSummary = response.getSummary();

        if (generatedSummary == null
                || generatedSummary.isBlank()
                || generatedSummary.startsWith("AI service error")
                || generatedSummary.startsWith("Unable to generate")) {

            return resume;
        }

        resume.setSummary(generatedSummary);

        return resumeRepository.save(resume);
    }
}