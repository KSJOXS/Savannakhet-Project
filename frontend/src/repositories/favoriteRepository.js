import api from "@/services/api";

export const favoriteRepository = {
  getUserFavorites(userId) {
    return api.get(`/users/${userId}/favorites`);
  },
  toggleFavorite(userId, placeId) {
    return api.post("/favorites/toggle", {
      user_id: userId,
      place_id: placeId,
    });
  },
};
