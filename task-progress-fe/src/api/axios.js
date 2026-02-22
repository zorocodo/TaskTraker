import axios from "axios";

const url = import.meta.env.VITE_API_URL

const api = axios.create({
  baseURL: url,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
