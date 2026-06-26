import axios from "axios";

const apiClient = axios.create({
  baseURL: "/api/v1",
  timeout: 60_000,
  headers: { "Content-Type": "application/json" },
});

apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    const message = err.response?.data?.detail ?? err.message ?? "Unknown error";
    return Promise.reject(new Error(message));
  }
);

export default apiClient;
