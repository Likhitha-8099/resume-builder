package com.resumebuilder.resume_builder.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public class ResumeDto {
	
	private Long id;
	@NotBlank(message = "Full name is required")
    private String fullName;
	@NotBlank(message = "Email is required")
    private String email;
	@NotBlank(message = "Phone number is required")
	@Size(min = 10, max = 10, message = "Phone number must be 10 digits")
    private String phone;
    private String linkedin;
    private String github;
    @NotBlank(message = "Summary is required")
    private String summary;
    @NotBlank(message = "Skills are required")
    private String skills;
    private String education;
    private String experience;
    private String projects;
    private String technologies;
    private String libraries;
    private String softSkills;
    private String certifications;
    private String educationInstitution;
	public String getTechnologies() {
		return technologies;
	}
	public void setTechnologies(String technologies) {
		this.technologies = technologies;
	}
	public String getLibraries() {
		return libraries;
	}
	public void setLibraries(String libraries) {
		this.libraries = libraries;
	}
	public String getSoftSkills() {
		return softSkills;
	}
	public void setSoftSkills(String softSkills) {
		this.softSkills = softSkills;
	}
	public String getCertifications() {
		return certifications;
	}
	public void setCertifications(String certifications) {
		this.certifications = certifications;
	}
	public String getEducationInstitution() {
		return educationInstitution;
	}
	public void setEducationInstitution(String educationInstitution) {
		this.educationInstitution = educationInstitution;
	}
	public Long getId() {
		return id;
	}
	public void setId(Long id) {
		this.id = id;
	}
	public String getFullName() {
		return fullName;
	}
	public void setFullName(String fullName) {
		this.fullName = fullName;
	}
	public String getEmail() {
		return email;
	}
	public void setEmail(String email) {
		this.email = email;
	}
	public String getPhone() {
		return phone;
	}
	public void setPhone(String phone) {
		this.phone = phone;
	}
	public String getLinkedin() {
		return linkedin;
	}
	public void setLinkedin(String linkedin) {
		this.linkedin = linkedin;
	}
	public String getGithub() {
		return github;
	}
	public void setGithub(String github) {
		this.github = github;
	}
	public String getSummary() {
		return summary;
	}
	public void setSummary(String summary) {
		this.summary = summary;
	}
	public String getSkills() {
		return skills;
	}
	public void setSkills(String skills) {
		this.skills = skills;
	}
	public String getEducation() {
		return education;
	}
	public void setEducation(String education) {
		this.education = education;
	}
	public String getExperience() {
		return experience;
	}
	public void setExperience(String experience) {
		this.experience = experience;
	}
	public String getProjects() {
		return projects;
	}
	public void setProjects(String projects) {
		this.projects = projects;
	}

}
