import { redirect } from '@sveltejs/kit';
import { DEFAULT_PROBLEM_ID, problemPath } from '#lib/problem-navigation';
import type { PageServerLoad } from './$types';
import { problemEntries } from '#lib/catalog.server';

export const load: PageServerLoad = () => redirect(307, problemPath(
  (problemEntries.find(entry => entry.problem.id === DEFAULT_PROBLEM_ID) ?? problemEntries[0]).problem.id,
));
