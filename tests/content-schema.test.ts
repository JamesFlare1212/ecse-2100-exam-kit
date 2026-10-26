import { describe, expect, test } from 'bun:test';
import { exams, formulas, documents } from '../content/catalog.server';
import { parseContent } from '../content/schema';
import type { Exam } from '../content/types';

describe('Authored JSON validation', () => {
  test('uses the source objects without rewriting question or solution data', () => {
    const input = structuredClone(exams);
    const before = JSON.stringify(input);
    expect(parseContent(input, formulas, documents).exams).toBe(input);
    expect(JSON.stringify(input)).toBe(before);
  });

  const cases: [string, (exam: Exam) => void, RegExp][] = [
    ['missing translation', e => { Reflect.deleteProperty(e.problems[0].statement, 'zh'); }, /statement\.zh/],
    ['unescaped TeX control character', e => { e.problems[0].statement.en += '\b'; }, /control character/],
    ['invalid equation', e => { e.problems[0].parts[0].steps[0].math = '\\frac{'; }, /steps\[0\]\.math.*invalid TeX/],
    ['unknown formula reference', e => { e.problems[0].parts[0].steps[0].refs.push('missing-formula'); }, /unknown formula missing-formula/],
    ['duplicate part ID', e => { e.problems[0].parts.push(structuredClone(e.problems[0].parts[0])); }, /duplicate ID/],
    ['invalid PDF page', e => { e.problems[0].parts[0].sourcePage = 9999; }, /sourcePage.*exceeds/],
    ['out-of-page citation', e => { e.problems[0].originalFigure.region = [.9, .9, .2, .2]; }, /rectangle must fit/],
    ['misspelled field', e => { Object.assign(e.problems[0], { statment: 'typo' }); }, /statment.*unknown field/],
  ];
  test.each(cases)('rejects %s before static rendering', (_name, mutate, error) => {
    const input = structuredClone(exams);
    mutate(input[0]);
    expect(() => parseContent(input, formulas, documents)).toThrow(error);
  });
});
