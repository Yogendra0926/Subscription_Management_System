const STORAGE_KEY = "brightloop-demo-data-v1";

export function loadDemoData(fallback) {
  if (typeof window === "undefined") return fallback;
  try {
    const value = JSON.parse(window.localStorage.getItem(STORAGE_KEY));
    return value && typeof value === "object" ? { ...fallback, ...value } : fallback;
  } catch {
    return fallback;
  }
}

export function saveDemoData(value) {
  if (typeof window !== "undefined") window.localStorage.setItem(STORAGE_KEY, JSON.stringify(value));
}

export function resetDemoData() {
  if (typeof window !== "undefined") window.localStorage.removeItem(STORAGE_KEY);
}
