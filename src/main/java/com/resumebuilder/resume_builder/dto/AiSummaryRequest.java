package com.resumebuilder.resume_builder.dto;

public class AiSummaryRequest {
	    private String fullName;
	    public String getFullName() {
			return fullName;
		}
		public void setFullName(String fullName) {
			this.fullName = fullName;
		}
		public String getSkills() {
			return skills;
		}
		public void setSkills(String skills) {
			this.skills = skills;
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
		private String skills;
	    private String experience;
	    private String projects;

}
