# Pluggable course papers

Each folder matching `exam{number}_{f|s}{year}` is discovered automatically.
`exam1_f26` means Exam 1, Fall 2026; `exam2_s26` means Exam 2, Spring 2026.
No import list or generated registry is maintained.

```text
content/
  exam1_f26/
    paper.json                 # Complete bilingual questions, guides and solutions
    documents.json             # This paper's PDF metadata and SHA-256 provenance
    figure-sources.json        # Exact crop regions and multi-panel geometry
    generate_figures.py        # This paper's question and solution drawings
    extracted/                 # Original PDF text for transcription checks
    assets/
      sources/                 # Preserved exam and solution PDFs
      pages/                   # Pre-rendered PDF pages, grouped by document ID
      figures/                 # SVGs in both themes and generation provenance
      original-figures/        # Original PDF figure crops
  exam1_f25/
  exam1_s26/
  exam2_f25/
  exam2_s26/
  formulas.json                # Shared crib and lecture formulas
  documents.json               # Shared crib and lecture PDF metadata
  extracted/                  # Shared crib and lecture text
```

JSON is edited and consumed directly. `paper.json` keeps the existing stable IDs
such as `e1-f26` and `e1-f26-q1` so links and local learning records survive moves.
The exam number, year and ID must match its folder name. A paper's document
paths are relative to its `assets/`, for example `sources/e1-f26.pdf` and
`pages/e1-f26`. Source filenames, page dimensions and SHA-256 must be preserved.
Shared course documents continue to use their local paths under `static/`.

`types.ts` defines the independent data model; `schema.ts` checks bilingual
fields, equations, IDs, citations and page bounds. `papers.server.ts` discovers
papers and combines their metadata. `navigation.ts` selects searchable question
text in memory. The browser receives that index and the selected problem's full
content, while the entire solution bank remains on the build side.

## Add or remove a paper

1. Create a folder such as `exam1_f27`, author `paper.json` and its source records.
2. Add the PDFs, page images, SVGs, original crops and extracted PDF text to that
   folder, with paths matching its metadata and figure names.
3. Put drawing configuration in `generate_figures.py`, exporting
   `render_figures(save, dark)`. Existing papers show the interface. Shared
   drawing primitives live in `scripts/plotting.py` and
   `scripts/question_primitives.py`; they contain no paper registration list.
4. Run `bun run build`. Pages, navigation and public assets are included
   automatically, including new exam-number tabs. Run `bun test` for full checks.

Move a paper outside `content/` to unplug it, then rebuild. Its pages and staged
assets disappear automatically. The root link selects an available problem if
its usual default is absent. Historical local progress, bookmarks, reveal counts
and legacy notes survive, but inactive records do not count toward progress.

`bun run content:check` validates without generating content. `bun run
papers:prepare` copies only paper `assets/` into the ignored `static/papers/`
staging directory; ordinary development and builds do this automatically. JSON,
Python and extracted text are never staged as public files. The dev server also
watches additions, removals and edits, including asset changes. Edit canonical
files inside each paper, not the staging directory.

## Drawings

```bash
python3 content/exam1_f26/generate_figures.py
python3 scripts/generate_figures.py --paper exam1_f26
python3 scripts/generate_figures.py
python3 scripts/check_figures.py
```

Drawing output stays in the owning paper's `assets/`. Python only handles
scientific drawings, PDF image assets and their checks; site builds require only
Bun. JSON TeX commands require escaped backslashes, for example `"\\epsilon"`.
Preserve literal original questions, faithful translations, complete derivations
and source-correction notes. Results belong in the solution, not in the givens.
