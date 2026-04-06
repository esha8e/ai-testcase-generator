import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

// Add a request interceptor to include the auth token
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const generateRequirementTestCases = (formData) =>
  API.post("generate/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

export const generateApiTestCases = (formData) =>
  API.post("generate/api/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

export const loginUser = (data) => API.post("auth/login/", data);

export const signupUser = (data) => API.post("auth/signup/", data);

// History endpoints
export const fetchHistory = () => API.get("history/");
export const fetchRunDetail = (runId) => API.get(`history/${runId}/`);

export default API;