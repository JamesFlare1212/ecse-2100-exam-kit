import { partIds, problemIds } from './catalog';
import type { Locale } from './types';

export const STORAGE_KEY = 'ecse2100-fieldnotes-v1';
export type Mode = 'study' | 'practice';
export class StudyState {
  locale = $state<Locale>('zh');
  theme = $state<'light' | 'dark' | 'system'>('system');
  mode = $state<Mode>('study');
  selected = $state('e2-s26-q3');
  navigationOpen = $state(true);
  referencesOpen = $state(true);
  completed = $state<Record<string, boolean>>({});
  bookmarks = $state<Record<string, boolean>>({});
  // Compatibility only: retain previously saved text without a note-taking UI.
  private legacyNotes?: Record<string, string>;
  revealed = $state<Record<string, number>>({});
  ready = $state(false);
  storageError = $state(false);

  restore(raw?: string | null) {
    try {
      const data = JSON.parse(raw ?? localStorage.getItem(STORAGE_KEY) ?? '{}');
      if (data.version !== 1) return;
      if (data.locale === 'zh' || data.locale === 'en') this.locale = data.locale;
      if (['light','dark','system'].includes(data.theme)) this.theme = data.theme;
      if (data.mode === 'study' || data.mode === 'practice') this.mode = data.mode;
      if (problemIds.has(data.selected)) this.selected = data.selected;
      if (typeof data.sidebars?.navigation === 'boolean') this.navigationOpen = data.sidebars.navigation;
      if (typeof data.sidebars?.references === 'boolean') this.referencesOpen = data.sidebars.references;
      const booleans = (value: unknown, valid: Set<string>) => {
        if (!value || typeof value !== 'object') return {};
        return Object.fromEntries(Object.entries(value).filter(([key,v]) => valid.has(key) && v === true));
      };
      this.completed = booleans(data.completed, partIds);
      this.bookmarks = booleans(data.bookmarks, problemIds);
      if (data.notes && typeof data.notes === 'object') {
        this.legacyNotes = Object.fromEntries(Object.entries(data.notes).filter(([key,value]) =>
          (partIds.has(key) || problemIds.has(key)) && typeof value === 'string').map(([key,value]) => [key, (value as string).slice(0,20000)]));
      }
      if (data.revealed && typeof data.revealed === 'object') {
        this.revealed = Object.fromEntries(Object.entries(data.revealed).filter(([key,value]) => partIds.has(key) && Number.isInteger(value) && (value as number) >= 0 && (value as number) <= 20).map(([key,value])=>[key,Number(value)]));
      }
    } catch { this.storageError = true; }
  }
  serialize() {
    return JSON.stringify({version:1, locale:this.locale, theme:this.theme, mode:this.mode, selected:this.selected,
      completed:this.completed, bookmarks:this.bookmarks, revealed:this.revealed,
      sidebars:{navigation:this.navigationOpen,references:this.referencesOpen},
      ...(this.legacyNotes ? {notes:this.legacyNotes} : {})});
  }
  persist(serialized: string) {
    try { localStorage.setItem(STORAGE_KEY, serialized); this.storageError = false; }
    catch { this.storageError = true; }
  }
  count(ids: string[]) { return ids.filter(id => this.completed[id]).length; }
}
