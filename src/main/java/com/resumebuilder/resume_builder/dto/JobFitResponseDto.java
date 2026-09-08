package com.resumebuilder.resume_builder.dto;

import java.util.List;

public class JobFitResponseDto {

    private int matchScore;
    private ScoreBreakdown scoreBreakdown;
    private List<String> matchedSkills;
    private List<String> partialMatches;
    private List<String> missingSkills;
    private List<String> resumeStrengths;
    private List<String> recommendations;
    private String matchSummary;
    private String calculationExplanation;

    public static class ScoreBreakdown {
        private int skillsScore;
        private int keywordScore;
        private int experienceScore;
        private int educationScore;
        private int projectScore;

        public ScoreBreakdown() {
        }

        public ScoreBreakdown(int skillsScore, int keywordScore, int experienceScore, int educationScore, int projectScore) {
            this.skillsScore = skillsScore;
            this.keywordScore = keywordScore;
            this.experienceScore = experienceScore;
            this.educationScore = educationScore;
            this.projectScore = projectScore;
        }

        public int getSkillsScore() {
            return skillsScore;
        }

        public void setSkillsScore(int skillsScore) {
            this.skillsScore = skillsScore;
        }

        public int getKeywordScore() {
            return keywordScore;
        }

        public void setKeywordScore(int keywordScore) {
            this.keywordScore = keywordScore;
        }

        public int getExperienceScore() {
            return experienceScore;
        }

        public void setExperienceScore(int experienceScore) {
            this.experienceScore = experienceScore;
        }

        public int getEducationScore() {
            return educationScore;
        }

        public void setEducationScore(int educationScore) {
            this.educationScore = educationScore;
        }

        public int getProjectScore() {
            return projectScore;
        }

        public void setProjectScore(int projectScore) {
            this.projectScore = projectScore;
        }
    }

    public JobFitResponseDto() {
    }

    public int getMatchScore() {
        return matchScore;
    }

    public void setMatchScore(int matchScore) {
        this.matchScore = matchScore;
    }

    public ScoreBreakdown getScoreBreakdown() {
        return scoreBreakdown;
    }

    public void setScoreBreakdown(ScoreBreakdown scoreBreakdown) {
        this.scoreBreakdown = scoreBreakdown;
    }

    public List<String> getMatchedSkills() {
        return matchedSkills;
    }

    public void setMatchedSkills(List<String> matchedSkills) {
        this.matchedSkills = matchedSkills;
    }

    public List<String> getPartialMatches() {
        return partialMatches;
    }

    public void setPartialMatches(List<String> partialMatches) {
        this.partialMatches = partialMatches;
    }

    public List<String> getMissingSkills() {
        return missingSkills;
    }

    public void setMissingSkills(List<String> missingSkills) {
        this.missingSkills = missingSkills;
    }

    public List<String> getResumeStrengths() {
        return resumeStrengths;
    }

    public void setResumeStrengths(List<String> resumeStrengths) {
        this.resumeStrengths = resumeStrengths;
    }

    public List<String> getRecommendations() {
        return recommendations;
    }

    public void setRecommendations(List<String> recommendations) {
        this.recommendations = recommendations;
    }

    public String getMatchSummary() {
        return matchSummary;
    }

    public void setMatchSummary(String matchSummary) {
        this.matchSummary = matchSummary;
    }

    public String getCalculationExplanation() {
        return calculationExplanation;
    }

    public void setCalculationExplanation(String calculationExplanation) {
        this.calculationExplanation = calculationExplanation;
    }
}
