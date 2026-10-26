/** Validate the deliverable HTML and per-page data after adapter-static runs. */
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { problemEntries } from '../src/lib/catalog.server';
import { DEFAULT_PROBLEM_ID, problemPath } from '../src/lib/problem-navigation';
import { renderText } from '../src/lib/math';

const root = resolve(import.meta.dir, '..', 'build');
const ids = problemEntries.map(({ problem }) => problem.id).sort();
assert.deepEqual(readdirSync(resolve(root, 'problems')).sort(), ids);
const defaultId = problemEntries.find(entry => entry.problem.id === DEFAULT_PROBLEM_ID)?.problem.id ?? problemEntries[0].problem.id;
assert.ok(readFileSync(resolve(root, 'index.html'), 'utf8').includes(problemPath(defaultId)));

let parts = 0;
for (const { problem } of problemEntries) {
  const directory = resolve(root, 'problems', problem.id);
  const html = readFileSync(resolve(directory, 'index.html'), 'utf8');
  const document = html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '');
  assert.ok(document.includes(`data-problem="${problem.id}"`), `${problem.id}: page identity`);
  assert.ok(document.includes(`>${problem.title.zh}</h1>`), `${problem.id}: prerendered title`);
  assert.ok(document.includes(renderText(problem.statement.zh)), `${problem.id}: prerendered statement`);
  for (const part of problem.parts) {
    assert.ok(document.includes(renderText(part.prompt.zh)), `${part.id}: prerendered question`);
    parts++;
  }

  // SvelteKit serializes server load data as reference arrays. The complete
  // Problem records in this static payload must belong to this page alone.
  const payload = JSON.parse(readFileSync(resolve(directory, '__data.json'), 'utf8'));
  const problemIds: string[] = [];
  for (const node of payload.nodes) {
    if (node?.type !== 'data') continue;
    const rootData = node.data[0];
    if (rootData && 'exam' in rootData) {
      assert.ok(!('problems' in node.data[rootData.exam]), `${problem.id}: exam metadata excludes other solutions`);
    }
    for (const value of node.data) {
      if (!value || typeof value !== 'object' || Array.isArray(value)) continue;
      if ('wording' in value && 'guide' in value && 'parts' in value) problemIds.push(node.data[value.id]);
    }
  }
  assert.deepEqual(problemIds, [problem.id], `${problem.id}: isolated hydration data`);
}
console.log(`Prerender verified: ${ids.length} problem HTML pages, ${parts} question parts, isolated page data.`);
