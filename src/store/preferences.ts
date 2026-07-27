export interface UserPreferences {
  readonly theme: "light" | "dark" | "system";
  readonly language: string;
  readonly largeText: boolean;
  readonly highContrast: boolean;
  readonly reducedMotion: boolean;
}

const STORAGE_KEY = "namo-setu.preferences.v1";
const DEFAULTS: UserPreferences = {
  theme: "system",
  language: "en-IN",
  largeText: false,
  highContrast: false,
  reducedMotion: false
};

export function loadPreferences(): UserPreferences {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? { ...DEFAULTS, ...JSON.parse(saved) as Partial<UserPreferences> } : DEFAULTS;
  } catch {
    return DEFAULTS;
  }
}

export function savePreferences(preferences: UserPreferences): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(preferences));
}
