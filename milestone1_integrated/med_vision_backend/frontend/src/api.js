import axios from "axios";

const API_BASE = "https://medviss.in/api";

const api = axios.create({
  baseURL: API_BASE,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("medvision_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const loginUser = async (email, password) => {
  const params = new URLSearchParams();
  params.append("username", email);
  params.append("password", password);
  const response = await api.post("/auth/login", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return response.data;
};

export const registerUser = async (email, password) => {
  const response = await api.post("/auth/register", { email, password });
  return response.data;
};

export const createPrediction = (file) => {
  const form = new FormData();
  form.append("file", file);
  return api.post("/predictions", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const getPrediction = (id) => api.get(`/predictions/${id}`);

export const listPredictions = (page = 1, pageSize = 10) =>
  api.get("/predictions", { params: { page, page_size: pageSize } });

export const subscribeToEvents = (id, onStatus) => {
  const token = localStorage.getItem("medvision_token");
  const source = new EventSource(
    `${API_BASE}/predictions/${id}/events?token=${token}`,
  );
  source.addEventListener("status", (e) => onStatus(JSON.parse(e.data)));
  source.onerror = () => source.close();
  return source;
};
