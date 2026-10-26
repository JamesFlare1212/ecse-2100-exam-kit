import { error } from '@sveltejs/kit';
import { problemEntries } from '#lib/catalog.server';
import type { EntryGenerator, PageServerLoad } from './$types';

export const entries: EntryGenerator = () => problemEntries.map(({ problem }) => ({ problem: problem.id }));

export const load: PageServerLoad = ({ params }) => {
  const entry = problemEntries.find(({ problem }) => problem.id === params.problem);
  if (!entry) error(404, 'Problem not found');
  // Never serialize the other problems in this exam into a page's hydration data.
  const { problems, ...exam } = entry.exam;
  return { exam, problem: entry.problem, assetBase: entry.paper.assetBase };
};
