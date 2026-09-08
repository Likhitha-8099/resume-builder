import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL;

export const createResume = async (resumeData) => {
  const response = await axios.post(`${API_BASE_URL}/api/resumes`, resumeData);
  return response.data;
};

export const getAllResumes = async () => {
  const response = await axios.get(`${API_BASE_URL}/api/resumes`);
  return response.data;
};

export const getResumeById = async (id) => {
  const response = await axios.get(`${API_BASE_URL}/api/resumes/${id}`);
  return response.data;
};

export const updateResume = async (id, resumeData) => {
  const response = await axios.put(`${API_BASE_URL}/api/resumes/${id}`, resumeData);
  return response.data;
};

export const deleteResume = async (id) => {
  const response = await axios.delete(`${API_BASE_URL}/api/resumes/${id}`);
  return response.data;
};

export const generateAiSummary = async (resumeId) => {
  const response = await axios.put(
    `${API_BASE_URL}/api/resumes/${resumeId}/generate-summary`
  );
  return response.data;
};

export const analyzeJobFitUpload = async (formData) => {
  const response = await axios.post(
    `${API_BASE_URL}/api/job-fit/analyze`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      timeout: 45000,
    }
  );
  return response.data;
};