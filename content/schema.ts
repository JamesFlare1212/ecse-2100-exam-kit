import katex from 'katex';
import type { Exam, Formula, SourceDocument } from './types.ts';

type Rule = (value: unknown, path: string) => void;
function fail(path: string, message: string): never {
  throw new Error(`Invalid content at ${path}: ${message}`);
}
const text: Rule = (value, path) => {
  if (typeof value !== 'string' || !value.trim()) fail(path, 'expected nonempty text');
  if (/[\u0000-\u0008\u000b-\u001f]/.test(value)) fail(path, 'contains a control character; check JSON TeX escapes');
};
const natural: Rule = (value, path) => {
  if (typeof value !== 'number' || !Number.isInteger(value) || value < 0) fail(path, 'expected a nonnegative integer');
};
const positive: Rule = (value, path) => {
  natural(value, path);
  if (value === 0) fail(path, 'expected a positive integer');
};
const boolean: Rule = (value, path) => { if (typeof value !== 'boolean') fail(path, 'expected a boolean'); };
const array = (rule: Rule, minimum = 0): Rule => (value, path) => {
  if (!Array.isArray(value) || value.length < minimum) fail(path, `expected an array with at least ${minimum} entries`);
  value.forEach((item, index) => rule(item, `${path}[${index}]`));
};
const object = (required: Record<string, Rule>, optional: Record<string, Rule> = {}): Rule => (value, path) => {
  if (!value || typeof value !== 'object' || Array.isArray(value)) fail(path, 'expected an object');
  const record = value as Record<string, unknown>;
  for (const [key, rule] of Object.entries(required)) rule(record[key], `${path}.${key}`);
  for (const [key, entry] of Object.entries(record)) {
    if (Object.hasOwn(optional, key)) optional[key](entry, `${path}.${key}`);
    else if (!Object.hasOwn(required, key)) fail(`${path}.${key}`, 'unknown field');
  }
};
const localized = object({ zh: text, en: text });
const tex: Rule = (value, path) => {
  text(value, path);
  try { katex.renderToString(value as string, { throwOnError: true, strict: 'ignore', trust: false }); }
  catch (error) { fail(path, `invalid TeX: ${error instanceof Error ? error.message : String(error)}`); }
};
const region: Rule = (value, path) => {
  if (!Array.isArray(value) || value.length !== 4 || value.some(n => typeof n !== 'number' || !Number.isFinite(n))) fail(path, 'expected [x, y, width, height]');
  const [x, y, width, height] = value as number[];
  if (x < 0 || y < 0 || width <= 0 || height <= 0 || x + width > 1 || y + height > 1) fail(path, 'rectangle must fit inside the PDF page');
};
const originalFigure = object({ doc: text, page: positive, region });
const source = object({ doc: text, page: positive, label: localized }, { region });
const step = object({ text: localized, math: tex, refs: array(text) });
const part = object({
  id: text, label: text, points: natural, prompt: localized, steps: array(step, 3),
  answer: tex, sourcePage: positive, solutionPage: positive,
}, {
  answerText: localized, note: localized, figure: text, figureCaption: localized, spatialFigure: text,
  questionFigure: object({ name: text, source: originalFigure, caption: localized }),
});
const problem = object({
  wording: (value, path) => { if (value !== 'original') fail(path, 'must preserve original exam wording'); },
  id: text, number: positive, title: localized, topic: localized, statement: localized,
  givens: array(tex), points: natural, figure: text, figureCaption: localized,
  originalFigure, lectures: array(source, 1),
  guide: object({ concept: localized, known: localized, goal: localized, approach: localized }),
  parts: array(part, 1),
}, { figureAtParts: boolean, note: localized });
const exam = object({
  id: text, number: positive, term: localized, year: positive, points: natural,
  doc: text, solutionDoc: text, questionsOnly: boolean, problems: array(problem, 1),
});
const formula = object({ id: text, title: localized, math: tex, source }, { note: localized });
const dimensions: Rule = (value, path) => {
  if (!Array.isArray(value) || value.length !== 2 || value.some(n => typeof n !== 'number' || !Number.isFinite(n) || n <= 0)) fail(path, 'expected positive PDF page dimensions');
};
const document = object({
  id: text, title: text, kind: text, pages: positive, pdf: text, pageBase: text,
  sizes: array(dimensions, 1), original: text,
  sha256: (value, path) => { if (typeof value !== 'string' || !/^[a-f0-9]{64}$/.test(value)) fail(path, 'expected SHA-256 provenance'); },
});

/** Validate the authored JSON directly. No generated JSON or content rewriting. */
export function parseContent(rawExams: unknown, rawFormulas: unknown, rawDocuments: unknown) {
  array(exam, 1)(rawExams, 'exams');
  array(formula, 1)(rawFormulas, 'formulas');
  if (!rawDocuments || typeof rawDocuments !== 'object' || Array.isArray(rawDocuments)) fail('documents', 'expected a document registry');
  for (const [id, entry] of Object.entries(rawDocuments)) document(entry, `documents.${id}`);
  const exams = rawExams as Exam[];
  const formulas = rawFormulas as Formula[];
  const documents = rawDocuments as Record<string, SourceDocument>;
  const ids = new Set<string>();
  function unique(id: string, path: string) {
    if (!/^[a-z0-9-]+$/.test(id) || ids.has(id)) fail(path, `invalid or duplicate ID ${id}`);
    ids.add(id);
  }
  function page(doc: string, number: number, path: string) {
    if (!documents[doc]) fail(path, `unknown document ${doc}`);
    if (number > documents[doc].pages) fail(path, `PDF page ${number} exceeds ${doc}'s ${documents[doc].pages} pages`);
  }
  for (const [id, doc] of Object.entries(documents)) {
    if (id !== doc.id) fail(`documents.${id}.id`, 'must match its registry key');
    if (doc.sizes.length !== doc.pages) fail(`documents.${id}.sizes`, 'must describe every PDF page');
    if (!/^\/(?:papers\/exam[1-9]\d*_[fs]\d{2}\/)?sources\//.test(doc.pdf)
      || !/^\/(?:papers\/exam[1-9]\d*_[fs]\d{2}\/)?pages\//.test(doc.pageBase)) fail(`documents.${id}`, 'source assets must use local paths');
  }
  const formulaIds = new Set<string>();
  for (const f of formulas) {
    unique(f.id, `formulas.${f.id}`); formulaIds.add(f.id);
    page(f.source.doc, f.source.page, `formulas.${f.id}.source`);
  }
  for (const e of exams) {
    unique(e.id, `exams.${e.id}`);
    page(e.doc, 1, `${e.id}.doc`); page(e.solutionDoc, 1, `${e.id}.solutionDoc`);
    if (e.problems.reduce((sum, q) => sum + q.points, 0) !== e.points) fail(`${e.id}.points`, 'must equal the total problem points');
    for (const q of e.problems) {
      unique(q.id, `${e.id}.problems`);
      if (q.id !== `${e.id}-q${q.number}`) fail(q.id, 'must match its exam ID and problem number');
      for (const ref of [q.originalFigure, ...q.lectures]) page(ref.doc, ref.page, `${q.id}.sources`);
      for (const p of q.parts) {
        unique(p.id, `${q.id}.parts`);
        if (!p.id.startsWith(`${q.id}-`)) fail(p.id, 'must belong to its problem');
        page(e.doc, p.sourcePage, `${p.id}.sourcePage`); page(e.solutionDoc, p.solutionPage, `${p.id}.solutionPage`);
        if (p.questionFigure) page(p.questionFigure.source.doc, p.questionFigure.source.page, `${p.id}.questionFigure`);
        if (p.figure && !p.figureCaption) fail(`${p.id}.figureCaption`, 'solution figures need bilingual captions');
        for (const [index, s] of p.steps.entries()) for (const ref of s.refs) {
          if (!formulaIds.has(ref)) fail(`${p.id}.steps[${index}].refs`, `unknown formula ${ref}`);
        }
      }
    }
  }
  return { exams, formulas, documents };
}
