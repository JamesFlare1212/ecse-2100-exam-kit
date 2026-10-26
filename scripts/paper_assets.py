"""Locate canonical paper JSON and assets for offline image tools."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER_NAME = re.compile(r'exam[1-9]\d*_[fs]\d{2}')


def papers():
    result = []
    for directory in sorted((ROOT / 'content').iterdir()):
        if directory.is_dir() and PAPER_NAME.fullmatch(directory.name):
            result.append({'name': directory.name, 'directory': directory,
                           'exam': json.loads((directory / 'paper.json').read_text())})
    return result


def documents():
    result = json.loads((ROOT / 'content/documents.json').read_text())
    for paper in papers():
        local = json.loads((paper['directory'] / 'documents.json').read_text())
        for key, value in local.items():
            if key in result:
                raise ValueError(f'Duplicate document: {key}')
            base = '/papers/' + paper['name'] + '/'
            result[key] = dict(value, pdf=base+value['pdf'], pageBase=base+value['pageBase'])
    return result


def asset_source(path):
    parts = Path(path.lstrip('/')).parts
    if '..' in parts:
        raise ValueError(f'Invalid asset path: {path}')
    if parts[0] == 'papers':
        if not PAPER_NAME.fullmatch(parts[1]):
            raise ValueError(f'Invalid paper asset path: {path}')
        return ROOT / 'content' / parts[1] / 'assets' / Path(*parts[2:])
    return ROOT / 'static' / Path(*parts)


def text_source(doc_id):
    for paper in papers():
        local = json.loads((paper['directory'] / 'documents.json').read_text())
        if doc_id in local:
            return paper['directory'] / 'extracted' / f'{doc_id}.txt'
    return ROOT / 'content/extracted' / f'{doc_id}.txt'
