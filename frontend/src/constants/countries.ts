/** Mirrors backend COUNTRY_CURRENCY_MAP */
export const COUNTRY_CURRENCY_MAP: Record<string, string> = {
  US: "USD",
  IN: "INR",
  GB: "GBP",
  DE: "EUR",
  FR: "EUR",
  CA: "CAD",
  AU: "AUD",
  SG: "SGD",
  JP: "JPY",
  BR: "BRL",
};

export const COUNTRY_OPTIONS = Object.keys(COUNTRY_CURRENCY_MAP).sort();
