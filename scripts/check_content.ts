import { exams, formulas, documents, papers } from '../content/catalog.server';
import { assetSource } from '../content/papers.server';
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';

function required(path: string) {
  if (!existsSync(path)) throw new Error(`Missing paper resource: ${path}`);
}
for (const paper of papers) {
  for (const name of ['generate_figures.py', 'figure-sources.json']) required(resolve(paper.directory, name));
  for (const doc of Object.values(paper.documents)) {
    required(assetSource(doc.pdf));
    required(resolve(paper.directory, 'extracted', `${doc.id}.txt`));
    for (let page = 1; page <= doc.pages; page++) required(assetSource(`${doc.pageBase}/${page}.webp`));
  }
  for (const question of paper.exam.problems) {
    const names = [question.figure, ...question.parts.flatMap(part => [part.figure, part.spatialFigure, part.questionFigure?.name])].filter((name): name is string => Boolean(name));
    for (const name of new Set(names)) for (const theme of ['', '-dark']) required(resolve(paper.directory, 'assets/figures', `${name}${theme}.svg`));
    for (const name of [question.figure, ...question.parts.flatMap(part => part.questionFigure ? [part.questionFigure.name] : [])]) required(resolve(paper.directory, 'assets/original-figures', `${name}.webp`));
  }
}

const problems = exams.flatMap(exam => exam.problems);
const parts = problems.flatMap(problem => problem.parts);
console.log(`Content verified directly from JSON: ${exams.length} exams / ${problems.length} problems / ${parts.length} parts / ${parts.reduce((sum, part) => sum + part.steps.length, 0)} steps / ${formulas.length} formulas / ${Object.keys(documents).length} documents.`);
