import api from "@/services/api";

export const categoryRepository = {
  getAll() {
    return api.get("/categories");
  },
  create(data) {
    return api.post("/admin/categories", data);
  },
  delete(id) {
    return api.delete(`/admin/categories/${id}`);
  },
};
