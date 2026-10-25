"""Copy course sources and render deterministic, page-addressable previews.

Run with Python and PyMuPDF (see requirements.txt). PDF page numbers are 1-based.
The source directory defaults to the parent of this repository.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import pymupdf
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--source-dir', type=Path, default=ROOT.parent)
parser.add_argument('--force', action='store_true')
args = parser.parse_args()
SOURCES = [
    ('e1-f25', 'Exams/Exam_1_F25_w_Smith_Chart.pdf', 'exam', 'Exam 1 · Fall 2025'),
    ('e1-f25-sol', 'Exam_1_Solutions_F25.pdf', 'solution', 'Exam 1 · Fall 2025 · Solutions'),
    ('e1-s26', 'Exams/Exam_1_S26_v0.pdf', 'exam', 'Exam 1 · Spring 2026'),
    ('e1-s26-sol', 'Exams/Exam_1_S26_Solutions_v1.pdf', 'solution', 'Exam 1 · Spring 2026 · Solutions'),
    ('e1-f26', 'Exams/Exam_1_F26_Solutions.pdf', 'exam', 'Exam 1 · Fall 2026 · Questions & solutions'),
    ('e2-f25', 'Exams/Exam_2_F25.pdf.pdf', 'exam', 'Exam 2 · Fall 2025'),
    ('e2-f25-sol', 'Exams/Exam_2_F25_Solutions.pdf', 'solution', 'Exam 2 · Fall 2025 · Solutions'),
    ('e2-s26', 'Exams/Exam_2_S26.pdf', 'exam', 'Exam 2 · Spring 2026'),
    ('e2-s26-sol', 'Exams/Exam_2_S26_Solutions.pdf', 'solution', 'Exam 2 · Spring 2026 · Solutions'),
    ('crib', 'Fields and Waves Crib Sheet.pdf', 'crib', 'Fields and Waves · Crib Sheet'),
]
for i in range(1, 16):
    filename = 'Lecture 04 Transient Analysis.pdf' if i == 4 else f'Lecture {i:02d}.pdf'
    SOURCES.append((f'lecture-{i:02d}', f'Lecture Notes/{filename}', 'lecture', f'Lecture {i:02d}'))

manifest = {}
(ROOT / 'src/lib/data').mkdir(parents=True, exist_ok=True)
(ROOT / 'content/extracted').mkdir(parents=True, exist_ok=True)
for doc_id, relative, kind, title in SOURCES:
    path = args.source_dir / relative
    if not path.exists():
        raise FileNotFoundError(f'Missing source PDF: {path}')
    pdf_dir = ROOT / 'static/sources'
    pdf_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, pdf_dir / f'{doc_id}.pdf')
    doc = pymupdf.open(path)
    previews = ROOT / 'static/pages' / doc_id
    previews.mkdir(parents=True, exist_ok=True)
    sizes = []
    for number, page in enumerate(doc, 1):
        sizes.append([round(page.rect.width, 2), round(page.rect.height, 2)])
        dest = previews / f'{number}.webp'
        if dest.exists() and not args.force:
            continue
        target_width = 1100 if kind != 'lecture' else 1000
        pix = page.get_pixmap(matrix=pymupdf.Matrix(target_width / page.rect.width, target_width / page.rect.width), alpha=False)
        im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        im.save(dest, 'WEBP', quality=85, method=4)
    manifest[doc_id] = {'id': doc_id, 'title': title, 'kind': kind, 'pages': len(doc), 'pdf': f'/sources/{doc_id}.pdf', 'pageBase': f'/pages/{doc_id}', 'sizes': sizes, 'original': relative, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    (ROOT / 'content/extracted' / f'{doc_id}.txt').write_text('\n'.join(f'\n--- PAGE {i+1} ---\n'+p.get_text(sort=True) for i,p in enumerate(doc)))
    if kind in ('exam', 'crib'):
        columns = 3 if kind == 'crib' else 4
        thumb_w, thumb_h = 330, 460
        sheet = Image.new('RGB', (columns*thumb_w, ((len(doc)+columns-1)//columns)*(thumb_h+28)), '#e9e9e9')
        draw = ImageDraw.Draw(sheet)
        for i in range(len(doc)):
            im = Image.open(previews/f'{i+1}.webp')
            im.thumbnail((thumb_w-8, thumb_h))
            x,y = (i%columns)*thumb_w, (i//columns)*(thumb_h+28)
            sheet.paste(im, (x,y+24))
            draw.text((x+6,y+5), f'{doc_id} / PDF {i+1}', fill='black')
        sheet.save(f'/tmp/ecse-{doc_id}-contact.jpg')
    print(f'{doc_id}: {len(doc)} pages prepared', flush=True)

(ROOT/'src/lib/data/documents.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
print(f'{len(manifest)} documents, {sum(d["pages"] for d in manifest.values())} pages ready.')
