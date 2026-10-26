import { papers } from '../../content/catalog.server';

// SvelteKit prevents this complete solution bank from entering client bundles.
export { exams, examIndex, documents, papers } from '../../content/catalog.server';
export const problemEntries = papers.flatMap(paper => paper.exam.problems.map(problem => ({ exam: paper.exam, problem, paper })));
