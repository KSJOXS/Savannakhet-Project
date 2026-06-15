import api from "@/services/api";

export default {
  getExchangeRates() {
    return api.get("/v1/utilities/exchange-rates");
  },
  getPhrases() {
    return api.get("/v1/utilities/phrases");
  },
  getTransports() {
    return api.get("/v1/utilities/transports");
  },
};
