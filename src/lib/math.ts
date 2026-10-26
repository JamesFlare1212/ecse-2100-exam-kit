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

/** Text alternatives use KaTeX's Unicode MathML, without spoken TeX commands. */
export function plainText(text: string) {
  return text.replace(/\$\$([\s\S]*?)\$\$|\$([^$\n]+)\$/g, (_, display, inline) => {
    const html = renderMath(display ?? inline);
    return (html.match(/<math\b[^>]*>([\s\S]*?)<\/math>/)?.[1] ?? '')
      .replace(/<annotation\b[^>]*>[\s\S]*?<\/annotation>/g, '')
      .replace(/<[^>]*>/g, '')
      .replace(/&#(x[\da-f]+|\d+);/gi, (_, code) => String.fromCodePoint(
        code.startsWith('x') ? parseInt(code.slice(1), 16) : Number(code),
      ))
      .replaceAll('&amp;', '&').replaceAll('&lt;', '<').replaceAll('&gt;', '>');
  });
}
