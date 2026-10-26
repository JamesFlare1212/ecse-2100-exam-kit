import type { Locale } from './types';

export const STORAGE_KEY = 'ecse2100-fieldnotes-v1';

export function readSavedLocale(): Locale {
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '{}');
    return data.version === 1 && data.locale === 'en' ? 'en' : 'zh';
  } catch { return 'zh'; }
}

/** Change the error-page language without replacing saved study records. */
export function saveLocale(locale: Locale) {
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '{}');
    if (!data || typeof data !== 'object' || Array.isArray(data)) return;
    if (data.version !== undefined && data.version !== 1) return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ ...data, version: 1, locale }));
  } catch { /* The language can still change when storage is unavailable. */ }
}
