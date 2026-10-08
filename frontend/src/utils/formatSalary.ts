const localeForCurrency: Record<string, string> = {
  USD: "en-US",
  GBP: "en-GB",
  EUR: "de-DE",
  INR: "en-IN",
  JPY: "ja-JP",
};

export function formatLocalSalary(amount: number, currency: string): string {
  const locale = localeForCurrency[currency] ?? "en-US";
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(amount);
}
