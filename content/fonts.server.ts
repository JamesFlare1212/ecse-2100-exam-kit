import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';

const css=readFileSync(resolve('node_modules/@fontsource-variable/noto-sans-sc/index.css'),'utf8');
const faces=[...css.matchAll(/@font-face\s*\{([^}]+)\}/g)].map(([,block])=>({
  name:/url\(\.\/files\/([^\)]+)\)/.exec(block)![1],
  ranges:/unicode-range:\s*([^;]+)/.exec(block)![1].split(',').map(range=>range.trim().slice(2).split('-').map(hex=>parseInt(hex,16))),
}));
/** Preload only the subsets used in the visible question and workspace labels. */
export function criticalFontFiles(text:string){
  const points=[...new Set([...text].map(char=>char.codePointAt(0)!))].filter(code=>code>127);
  return faces.filter(face=>face.ranges.some(([low,high=low])=>points.some(code=>code>=low&&code<=high))).map(face=>face.name);
}
