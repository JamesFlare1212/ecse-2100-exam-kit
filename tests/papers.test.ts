import { describe, expect, test } from 'bun:test';
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { loadContent, assetSource, stagePaperAssets } from '../content/papers.server';

const project = resolve(import.meta.dir, '..');
function fixture() {
  const root = mkdtempSync(resolve(tmpdir(), 'fieldnotes-papers-'));
  for (const name of ['documents.json', 'formulas.json']) cpSync(resolve(project, 'content', name), resolve(root, name));
  function add(name: string, id: string, year: number) {
    const directory = resolve(root, name);
    mkdirSync(resolve(directory, 'assets/figures'), { recursive: true });
    const original = resolve(project, 'content/exam1_f25');
    const exam = JSON.parse(readFileSync(resolve(original, 'paper.json'), 'utf8').replaceAll('e1-f25', id));
    exam.year = year;
    writeFileSync(resolve(directory, 'paper.json'), JSON.stringify(exam));
    writeFileSync(resolve(directory, 'documents.json'), readFileSync(resolve(original, 'documents.json'), 'utf8').replaceAll('e1-f25', id));
    writeFileSync(resolve(directory, 'assets/figures/test.svg'), '<svg/>');
    return directory;
  }
  return { root, add };
}

describe('Pluggable paper folders', () => {
  test('discovers added papers, scopes assets and removes unplugged staged assets without a registry edit', () => {
    const { root, add } = fixture();
    try {
      const first = add('exam1_f25', 'e1-f25', 2025);
      expect(loadContent(root).exams.map(exam => exam.id)).toEqual(['e1-f25']);
      const next = add('exam1_f27', 'e1-f27', 2027);
      const both = loadContent(root);
      expect(both.exams.map(exam => exam.id)).toEqual(['e1-f25', 'e1-f27']);
      expect(both.documents['e1-f27'].pdf).toBe('/papers/exam1_f27/sources/e1-f27.pdf');
      expect(assetSource('/papers/exam1_f27/figures/test.svg', root)).toBe(resolve(next, 'assets/figures/test.svg'));
      const staged = resolve(root, 'public');
      stagePaperAssets(both.papers, staged);
      expect(readFileSync(resolve(staged, 'exam1_f27/figures/test.svg'), 'utf8')).toBe('<svg/>');
      expect(existsSync(resolve(staged, 'exam1_f27/paper.json'))).toBe(false);
      rmSync(first, { recursive: true });
      const remaining = loadContent(root);
      stagePaperAssets(remaining.papers, staged);
      expect(remaining.exams.map(exam => exam.id)).toEqual(['e1-f27']);
      expect(existsSync(resolve(staged, 'exam1_f25'))).toBe(false);
      expect(existsSync(resolve(staged, 'exam1_f27/figures/test.svg'))).toBe(true);
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  test('reports incomplete or misnamed papers instead of silently omitting them', () => {
    const { root, add } = fixture();
    try {
      mkdirSync(resolve(root, 'exam1_f27'));
      expect(() => loadContent(root)).toThrow('paper.json');
      rmSync(resolve(root, 'exam1_f27'), { recursive: true });
      add('exam1_f27', 'e1-f25', 2025);
      expect(() => loadContent(root)).toThrow('must match the paper folder');
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  test('rejects asset traversal outside a paper', () => {
    expect(() => assetSource('/papers/exam1_f26/../paper.json')).toThrow('Invalid local asset');
  });
});
