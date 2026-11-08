import formulaData from '../../content/formulas.json';
import type { ExamIndex, Formula, Problem, SourceDocument, Locale } from './types';
import { formulaReferences } from '../../content/text';
import { DEFAULT_PROBLEM_ID } from './problem-navigation';

export const formulas = formulaData as Formula[];
export const formulaById = Object.fromEntries(formulas.map(f => [f.id, f]));
export function createCatalog(exams: ExamIndex[], documents: Record<string, SourceDocument>) {
  const problemEntries = exams.flatMap(exam => exam.problems.map(problem => ({ exam, problem })));
  const partIds = new Set(problemEntries.flatMap(({problem}) => problem.parts.map(p => p.id)));
  const problemIds = new Set(problemEntries.map(({problem}) => problem.id));
  const findProblem = (id: string) => problemEntries.find(p => p.problem.id === id)
    ?? problemEntries.find(p => p.problem.id === DEFAULT_PROBLEM_ID) ?? problemEntries[0];
  return { exams, documents, problemEntries, partIds, problemIds, totalParts: partIds.size, findProblem };
}
export type Catalog = ReturnType<typeof createCatalog>;
export function problemFormulas(problem: Problem, locale: Locale) {
  const ids = [...new Set(problem.parts.flatMap(p => formulaReferences(p.solution[locale])))];
  return ids.map(id => formulaById[id]).filter(Boolean);
}
