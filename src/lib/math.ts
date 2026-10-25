import katex from 'katex';

export function renderMath(tex: string, displayMode = false) {
  return katex.renderToString(tex, {displayMode, throwOnError:false, strict:'ignore', trust:false, output:'htmlAndMathml'});
}
function escape(text: string) {
  return text.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;');
}
export function renderText(text: string) {
  const pattern = /(\$\$[\s\S]*?\$\$|\$[^$\n]+\$)/g;
  let result = '', offset = 0;
  for (const match of text.matchAll(pattern)) {
    result += escape(text.slice(offset, match.index)).replaceAll('\n','<br>');
    const display = match[0].startsWith('$$');
    result += renderMath(match[0].slice(display ? 2 : 1, display ? -2 : -1), display);
    offset = match.index! + match[0].length;
  }
  return result + escape(text.slice(offset)).replaceAll('\n','<br>');
}
