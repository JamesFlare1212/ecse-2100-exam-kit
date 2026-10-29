"""Localize renderer-owned SVG labels and embed the existing local CJK font.

Only ordinary text nodes are translated. Math spans and original exam crops
retain their source notation. Embedded font subsets keep SVG images independent
of the reader's installed fonts and make no runtime font requests.
"""
import base64
import re
from pathlib import Path


def localize(path, labels):
    svg = path.read_text()
    used = set()
    for original, translated in labels.items():
        needle = '>' + original + '<'
        if needle in svg:
            svg = svg.replace(needle, '>' + translated + '<')
            used.update(ord(char) for char in translated if ord(char) > 127)
    if not used:
        return
    root = Path(__file__).resolve().parents[1]
    fonts = root / 'node_modules/@fontsource-variable/noto-sans-sc'
    css = (fonts / 'index.css').read_text()
    faces = []
    missing = used.copy()
    for block in re.findall(r'@font-face\s*\{([^}]+)\}', css):
        ranges = re.search(r'unicode-range:\s*([^;]+)', block).group(1)
        covered = set()
        for item in ranges.split(','):
            bounds = item.strip()[2:].split('-')
            low, high = int(bounds[0], 16), int(bounds[-1], 16)
            covered.update(code for code in used if low <= code <= high)
        if not covered:
            continue
        file = fonts / re.search(r'url\(\./([^\)]+)\)', block).group(1)
        encoded = base64.b64encode(file.read_bytes()).decode()
        subset = ','.join(f'U+{code:X}' for code in sorted(covered))
        faces.append("@font-face{font-family:'Fieldnotes Chinese';font-weight:100 900;src:url(data:font/woff2;base64," + encoded + ") format('woff2');unicode-range:" + subset + ';}')
        missing -= covered
    if missing:
        raise ValueError(f'Missing local font characters: {missing}')
    styles = ''.join(faces) + "text{font-family:'Fieldnotes Chinese','DejaVu Sans',sans-serif!important}"
    svg = svg.replace('<defs>', '<defs>\n<style type="text/css">' + styles + '</style>', 1)
    path.write_text(svg)
