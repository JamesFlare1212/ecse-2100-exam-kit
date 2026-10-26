import { fromMarkdown } from 'mdast-util-from-markdown';
import { math } from 'micromark-extension-math';
import { mathFromMarkdown } from 'mdast-util-math';
import { parseDocument } from 'yaml';
import type { Localized, Part, Problem, ProblemGuide, Step } from './types';

export type PartMetadata = Omit<Part, 'prompt' | 'steps' | 'answer' | 'answerText' | 'note'>;
export type ProblemMetadata = Omit<Problem, 'statement' | 'guide' | 'parts' | 'note'> & { parts: PartMetadata[] };
export interface MarkdownQuestion { filePath: string; problem: Problem }

interface Section {
  name: string;
  depth: number;
  line: number;
  start: number;
  bodyStart: number;
  end: number;
  children: Section[];
}

const markdown = (source: string) => fromMarkdown(source, {
  extensions: [math()], mdastExtensions: [mathFromMarkdown()],
});

/** Read ordinary YAML frontmatter; question prose and equations live in the body. */
export function readQuestionMarkdown(source: string, file = 'question.md'): Problem {
  const match = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(source);
  if (!match) throw new Error(`${file}: expected YAML frontmatter delimited by ---`);
  const document = parseDocument(match[1], { uniqueKeys: true });
  if (document.errors.length) throw new Error(`${file}: ${document.errors.map(error => error.message).join('; ')}`);
  const metadata: unknown = document.toJS({ maxAliasCount: 0 });
  return parseQuestionBody(metadata, source.slice(match[0].length), file);
}

/** Parse headings through the Markdown AST, never by splitting arbitrary prose. */
export function parseQuestionBody(metadata: unknown, body: string, file = 'question.md'): Problem {
  function fail(section: Section, message: string): never {
    throw new Error(`${file}:${section.line} (${section.name}): ${message}`);
  }
  const root: Section = { name: 'article', depth: 1, line: 1, start: 0, bodyStart: 0, end: body.length, children: [] };
  const stack = [root];
  for (const node of markdown(body).children) {
    if (node.type !== 'heading') continue;
    while (stack.length > 1 && stack.at(-1)!.depth >= node.depth) stack.pop()!.end = node.position!.start.offset!;
    const parent = stack.at(-1)!;
    const name = node.children.map(child => child.type === 'text' ? child.value : '').join('');
    const section: Section = {
      name, depth: node.depth, line: node.position!.start.line,
      start: node.position!.start.offset!, bodyStart: node.position!.end.offset!, end: body.length, children: [],
    };
    if (node.depth !== parent.depth + 1) fail(section, `expected a level ${parent.depth + 1} heading`);
    if (parent.children.some(child => child.name === name)) fail(section, 'duplicate section');
    parent.children.push(section);
    stack.push(section);
  }
  const prose = (section: Section) => body.slice(section.bodyStart, section.children[0]?.start ?? section.end).trim();
  function branch(section: Section, required: string[], optional: string[] = []) {
    if (prose(section)) fail(section, 'place content inside its named child sections');
    for (const name of required) if (!section.children.some(child => child.name === name)) fail(section, `missing section ${name}`);
    for (const child of section.children) if (![...required, ...optional].includes(child.name)) fail(child, 'unknown section');
  }
  function child(section: Section, name: string) {
    const found = section.children.find(entry => entry.name === name);
    if (!found) fail(section, `missing section ${name}`);
    return found;
  }
  function leaf(section: Section) {
    if (section.children.length) fail(section, 'unexpected nested heading');
    const value = prose(section);
    if (!value) fail(section, 'expected nonempty content');
    return value;
  }
  function localized(section: Section): Localized {
    branch(section, ['English', '中文']);
    return { en: leaf(child(section, 'English')), zh: leaf(child(section, '中文')) };
  }
  function equation(section: Section): string {
    const nodes = markdown(leaf(section)).children;
    if (nodes.length !== 1 || nodes[0].type !== 'math') fail(section, 'expected exactly one display equation between $$ lines');
    return nodes[0].value;
  }
  function references(section: Section): string[] {
    const nodes = markdown(leaf(section)).children;
    if (nodes.length !== 1 || nodes[0].type !== 'list') fail(section, 'expected a list of [formula-id](formula:formula-id) links');
    return nodes[0].children.map(item => {
      const paragraph = item.children[0];
      if (item.children.length !== 1 || paragraph.type !== 'paragraph' || paragraph.children.length !== 1) fail(section, 'each reference must be one formula link');
      const link = paragraph.children[0];
      if (link.type !== 'link' || !/^formula:[a-z0-9-]+$/.test(link.url)) fail(section, 'expected a formula:formula-id link');
      return link.url.slice('formula:'.length);
    });
  }
  function step(section: Section): Step {
    branch(section, ['Equation'], ['English', '中文', 'References']);
    const annotated = section.children.some(entry => entry.name === 'English' || entry.name === '中文');
    return {
      ...(annotated ? { text: { en: leaf(child(section, 'English')), zh: leaf(child(section, '中文')) } } : {}),
      math: equation(child(section, 'Equation')),
      refs: section.children.some(entry => entry.name === 'References') ? references(child(section, 'References')) : [],
    };
  }
  if (!metadata || typeof metadata !== 'object' || Array.isArray(metadata)) fail(root, 'expected a frontmatter object');
  const { parts, ...attributes } = metadata as ProblemMetadata;
  if (!Array.isArray(parts) || !parts.length) fail(root, 'frontmatter must describe at least one part');
  if (parts.some(part => !part || typeof part !== 'object' || Array.isArray(part))) fail(root, 'every part must be a metadata object');
  const labels = parts.map(part => part.label);
  if (labels.some(label => typeof label !== 'string' || !label.trim()) || new Set(labels).size !== labels.length) fail(root, 'part labels must be nonempty and unique');
  // Content-bearing fields are deliberately excluded from YAML.
  for (const name of ['statement', 'guide', 'note']) if (Object.hasOwn(attributes, name)) fail(root, `${name} belongs in the Markdown body`);
  branch(root, ['Question', 'Guide', ...labels.map(label => `Part ${label}`)], ['Source correction']);
  const guideSection = child(root, 'Guide');
  const guides = { Concepts: 'concept', Givens: 'known', Goal: 'goal', Approach: 'approach' } as const;
  branch(guideSection, Object.keys(guides));
  const guide = Object.fromEntries(Object.entries(guides).map(([name, key]) => [key, localized(child(guideSection, name))])) as unknown as ProblemGuide;
  const parsedParts = parts.map(part => {
    const section = child(root, `Part ${part.label}`);
    for (const name of ['prompt', 'steps', 'answer', 'answerText', 'note']) if (Object.hasOwn(part, name)) fail(section, `${name} belongs in the Markdown body`);
    const steps = section.children.filter(entry => /^Step \d+$/.test(entry.name));
    if (!steps.length) fail(section, 'expected at least one equation group');
    steps.forEach((entry, index) => { if (entry.name !== `Step ${index + 1}`) fail(entry, 'steps must be numbered consecutively from 1'); });
    branch(section, ['Question', ...steps.map(entry => entry.name), 'Answer'], ['Answer text', 'Source correction']);
    return {
      ...part, prompt: localized(child(section, 'Question')), steps: steps.map(step), answer: equation(child(section, 'Answer')),
      ...(section.children.some(entry => entry.name === 'Answer text') ? { answerText: localized(child(section, 'Answer text')) } : {}),
      ...(section.children.some(entry => entry.name === 'Source correction') ? { note: localized(child(section, 'Source correction')) } : {}),
    };
  });
  return {
    ...attributes, statement: localized(child(root, 'Question')), guide, parts: parsedParts,
    ...(root.children.some(entry => entry.name === 'Source correction') ? { note: localized(child(root, 'Source correction')) } : {}),
  };
}
