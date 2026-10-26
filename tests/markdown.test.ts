import { describe, expect, test } from 'bun:test';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { parseQuestionBody, readQuestionMarkdown } from '../content/markdown';
import { renderText } from '../src/lib/math';
import { conclusionMath } from '../src/lib/answer-math';

const source = readFileSync(resolve(import.meta.dir, '../content/exam1_f26/questions/q1.md'), 'utf8');

describe('Markdown question articles', () => {
  test('reads both languages, native TeX, stable part IDs and formula references', () => {
    const problem = readQuestionMarkdown(source);
    expect(problem.id).toBe('e1-f26-q1');
    expect(problem.parts[0].id).toBe('e1-f26-q1-ai');
    expect(problem.statement.en).toContain('$\\Delta z\\ll\\lambda$');
    expect(problem.parts[0].steps[0].math).toBe('\\gamma=\\alpha+j\\beta');
    expect(problem.parts[0].steps[0].refs).toEqual(['lossy-wave']);
    expect(problem.parts.at(-1)?.questionFigure?.source.page).toBe(3);
    expect(problem.guide.known.zh).toContain('$60\\,\\mathrm m$');
  });

  test('uses the Markdown AST so headings inside code fences are ordinary content', () => {
    const changed = source.replace('This problem connects', '```text\n## Part fake\n```\n\nThis problem connects');
    expect(readQuestionMarkdown(changed).guide.concept.en).toContain('## Part fake');
    expect(readQuestionMarkdown(changed).parts).toHaveLength(4);
  });

  test('allows an equation without compulsory narration or an arbitrary step count', () => {
    const changed = source
      .replace(/### Step 1\n[\s\S]*?#### Equation/, '### Step 1\n\n#### Equation')
      .replace(/### Step 2\n[\s\S]*?(?=### Answer\n)/, '');
    const part = readQuestionMarkdown(changed).parts[0];
    expect(part.steps).toHaveLength(1);
    expect(part.steps[0].text).toBeUndefined();
    expect(part.steps[0].math).toContain('\\gamma=');
    expect(part.steps[0].refs).toEqual(['lossy-wave']);
  });

  test('still requires both translations when an annotation is supplied', () => {
    const changed = source.replace(/(### Step 1\n[\s\S]*?)#### 中文[\s\S]*?(?=#### Equation)/, '$1');
    expect(() => readQuestionMarkdown(changed)).toThrow('missing section 中文');
  });

  test('keeps a mathematical therefore symbol without repeating the final answer', () => {
    const result = conclusionMath('\\therefore\\quad E=Q/(4\\pi\\epsilon r^2)', 'E=Q/(4\\pi\\epsilon r^2)');
    expect(result.calculation).toBeUndefined();
    expect(result.result).toStartWith('\\therefore\\quad ');
    expect(result.result.match(/\\boxed\{/g)).toHaveLength(1);
    expect(renderText(`$$${result.result}$$`)).toContain('katex-display');
  });

  const cases: [string, (text: string) => string, RegExp][] = [
    ['missing translation', text => text.replace('### 中文', '### Chinese'), /missing section 中文/],
    ['duplicate section', text => text.replace('### 中文', '### English'), /duplicate section/],
    ['renamed guide field', text => text.replace('### Givens', '### Given'), /missing section Givens/],
    ['skipped step', text => text.replace('### Step 2', '### Step 99'), /numbered consecutively/],
    ['unknown section', text => text.replace('### Step 2', '### Summary'), /numbered consecutively|unknown section/],
    ['broken heading hierarchy', text => text.replace('#### Equation', '###### Equation'), /level 5/],
    ['missing governing equation', text => text.replace('#### Equation', '#### Equations'), /missing section Equation/],
    ['multiple equations per step', text => text.replace('#### References', '$$\nx=1\n$$\n\n#### References'), /exactly one display equation/],
    ['invalid formula link', text => text.replace('formula:lossy-wave', 'https://example.com/'), /formula:formula-id/],
    ['duplicate YAML property', text => text.replace('number: 1', 'number: 1\nnumber: 2'), /unique/],
    ['body stored in frontmatter', text => text.replace('number: 1', 'number: 1\nstatement: forbidden'), /belongs in the Markdown body/],
    ['unknown frontmatter field in a part', text => text.replace('label: a(i)', 'label: a(i)\n    steps: forbidden'), /belongs in the Markdown body/],
    ['missing frontmatter', text => text.replace(/^---/, ''), /YAML frontmatter/],
  ];
  test.each(cases)('rejects %s with the source filename', (_name, change, error) => {
    expect(() => readQuestionMarkdown(change(source), 'exam/questions/q1.md')).toThrow(error);
    expect(() => readQuestionMarkdown(change(source), 'exam/questions/q1.md')).toThrow('exam/questions/q1.md');
  });

  test('Astro body parsing and CLI frontmatter parsing produce identical question data', () => {
    const match = /^---\n([\s\S]*?)\n---\n/.exec(source)!;
    const problem = readQuestionMarkdown(source);
    const { statement, guide, parts, note, ...attributes } = problem;
    const metadata = { ...attributes, parts: parts.map(({ prompt, steps, answer, answerText, note, ...part }) => part) };
    expect(parseQuestionBody(metadata, source.slice(match[0].length))).toEqual(problem);
  });

  test('renders authored Markdown emphasis, lists and links while retaining math and escaping HTML', () => {
    const html = renderText('**Equation** with $\\alpha$ and *units*.\n\n- First\n- [Lecture](/sources/lecture-02.pdf)\n\n<script>alert(1)</script>');
    expect(html).toContain('<strong>Equation</strong>');
    expect(html).toContain('<em>units</em>');
    expect(html).toContain('katex');
    expect(html).toContain('role="listitem"');
    expect(html).toContain('href="/sources/lecture-02.pdf"');
    expect(html).toContain('&lt;script&gt;');
    expect(html).not.toContain('<script>');
    expect(renderText('[Unsafe](javascript:alert%281%29)')).toBe('Unsafe');
    expect(renderText('[Unsafe](data:text/html,hello)')).toBe('Unsafe');
    expect(renderText('`a_b`')).toBe('<code>a_b</code>');
    expect(renderText('$$\\rho(r)=\\rho_0 a/r$$')).toContain('katex-display');
  });
});
