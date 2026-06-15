import api from "@/services/api";

export const authRepository = {
  login(credentials) {
    return api.post("/login", credentials);
  },
  register(userData) {
    return api.post("/register", userData);
  },
};
