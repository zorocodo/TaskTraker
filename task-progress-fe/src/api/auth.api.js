import api from "./axios";

export const AuthAPI = {
  login: (username, password) =>
    api.post("/login/", {
      username,
      password,
    }),

  refreshToken: (refresh) =>
    api.post("/refresh/", {
      refresh,
    }),
};