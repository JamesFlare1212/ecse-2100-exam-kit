import { cpSync, existsSync, mkdirSync, readFileSync, readdirSync, rmSync } from 'node:fs';
import { resolve } from 'node:path';
import { parseContent } from './schema.ts';
import { createExamIndex } from './navigation.ts';
import type { Exam, Formula, SourceDocument } from './types.ts';

export const PAPER_NAME = /^exam[1-9]\d*_[fs]\d{2}$/;
export interface Paper {
  name: string;
  directory: string;
  assetBase: string;
  exam: Exam;
  documents: Record<string, SourceDocument>;
}
function readJson<T>(path: string): T {
  try { return JSON.parse(readFileSync(path, 'utf8')); }
  catch (error) { throw new Error(`Cannot read ${path}`, { cause: error }); }
}

/** Discover complete paper folders; no source list or generated registry. */
export function loadContent(directory = resolve('content')) {
  const documents = readJson<Record<string, SourceDocument>>(resolve(directory, 'documents.json'));
  const formulas = readJson<Formula[]>(resolve(directory, 'formulas.json'));
  const papers: Paper[] = readdirSync(directory, { withFileTypes: true })
    .filter(entry => entry.isDirectory() && PAPER_NAME.test(entry.name))
    .map(entry => {
      const folder = resolve(directory, entry.name);
      const exam = readJson<Exam>(resolve(folder, 'paper.json'));
      const match = /^e([1-9]\d*)-([fs]\d{2})$/.exec(exam.id);
      if (!match || entry.name !== `exam${match[1]}_${match[2]}` || exam.number !== Number(match[1])
        || exam.year % 100 !== Number(match[2].slice(1))) {
        throw new Error(`${entry.name}/paper.json: exam ID and number must match the paper folder`);
      }
      const assetBase = `/papers/${entry.name}`;
      const local = readJson<Record<string, SourceDocument>>(resolve(folder, 'documents.json'));
      const owned: Record<string, SourceDocument> = {};
      for (const [id, doc] of Object.entries(local)) {
        if (Object.hasOwn(documents, id)) throw new Error(`${entry.name}: duplicate document ${id}`);
        if (!/^sources\/[a-z0-9-]+\.pdf$/.test(doc.pdf) || !/^pages\/[a-z0-9-]+$/.test(doc.pageBase)) {
          throw new Error(`${entry.name}/documents.json: use relative sources/*.pdf and pages/* asset paths`);
        }
        owned[id] = { ...doc, pdf: `${assetBase}/${doc.pdf}`, pageBase: `${assetBase}/${doc.pageBase}` };
        documents[id] = owned[id];
      }
      if (!Object.hasOwn(owned, exam.doc) || !Object.hasOwn(owned, exam.solutionDoc)) {
        throw new Error(`${entry.name}: the paper must own its exam and solution PDFs`);
      }
      if (!existsSync(resolve(folder, 'assets'))) throw new Error(`${entry.name}: missing assets directory`);
      return { name: entry.name, directory: folder, assetBase, exam, documents: owned };
    });
  papers.sort((a, b) => a.exam.number - b.exam.number || a.exam.year - b.exam.year
    || Number(a.exam.id.includes('-f')) - Number(b.exam.id.includes('-f')) || a.name.localeCompare(b.name));
  const checked = parseContent(papers.map(paper => paper.exam), formulas, documents);
  return { ...checked, papers, examIndex: createExamIndex(checked.exams) };
}

/** Resolve public asset URLs to canonical source files without staging. */
export function assetSource(path: string, directory = resolve('content')) {
  if (!path.startsWith('/') || path.includes('\\') || path.split('/').some(part => part === '..' || part === '.')) {
    throw new Error(`Invalid local asset path: ${path}`);
  }
  if (path.startsWith('/papers/')) {
    const [, , name, ...parts] = path.split('/');
    if (!PAPER_NAME.test(name) || !parts.length) throw new Error(`Invalid paper asset path: ${path}`);
    return resolve(directory, name, 'assets', ...parts);
  }
  return resolve(directory, '../static', path.slice(1));
}

/** Copy only public assets. JSON, extracted text and Python remain private. */
export function stagePaperAssets(papers: Paper[], destination = resolve('static/papers')) {
  mkdirSync(destination, { recursive: true });
  const active = new Set(papers.map(paper => paper.name));
  for (const entry of readdirSync(destination)) {
    if (!active.has(entry)) rmSync(resolve(destination, entry), { recursive: true, force: true });
  }
  for (const paper of papers) {
    const target = resolve(destination, paper.name);
    rmSync(target, { recursive: true, force: true });
    cpSync(resolve(paper.directory, 'assets'), target, { recursive: true });
  }
}
