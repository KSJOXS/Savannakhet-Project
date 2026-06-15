import en from "./locales/en.js";
import la from "./locales/la.js";
import vi from "./locales/vi.js";
import th from "./locales/th.js";

export const messages = { en, la, vi, th };

export const supportedLocales = [
  { code: "en", label: "English", flag: "🇬🇧" },
  { code: "la", label: "ລາວ", flag: "🇱🇦" },
  { code: "th", label: "ไทย", flag: "🇹🇭" },
  { code: "vi", label: "Việt", flag: "🇻🇳" },
];
