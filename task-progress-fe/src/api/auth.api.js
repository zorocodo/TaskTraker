import api from "./axios";

export const AuthAPI = {
  login: (username, password) =>
    api.post("/login/", { username, password }),

  refreshToken: (refresh) =>
    api.post("/refresh/", { refresh }),

  register: (username, email, password, password2) =>
    api.post("/register/", { username, email, password, password2 }),
};