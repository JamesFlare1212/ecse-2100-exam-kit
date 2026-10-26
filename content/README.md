# Markdown paper library

Each problem is one bilingual Markdown article, grouped under its source paper:
`content/exam1_f26/questions/q1.md`. Start with an existing article such as
[Fall 2026, Question 1](exam1_f26/questions/q1.md).

Paper folders matching `exam{number}_{f|s}{year}` are discovered automatically.
`exam1_f26` means Exam 1, Fall 2026; `exam2_s26` means Exam 2, Spring 2026.
There is no import list or generated registry.

## Paper ownership

Each paper directory contains:

- `paper.json`: paper metadata only (ID, number, term, year, total score and PDF IDs).
- `questions/q1.md`, `q2.md`, etc.: the only authored question and solution sources.
- `documents.json`: preserved PDF filenames, page dimensions and SHA-256 provenance.
- `figure-sources.json`: original figure crops and multi-panel geometry.
- `generate_figures.py`: question and solution drawing configuration.
- `extracted/`: original PDF text for transcription checks.
- `assets/sources/`: original exam and solution PDFs.
- `assets/pages/`: PDF page images, grouped by document ID.
- `assets/figures/`: static SVGs in both themes and drawing provenance.
- `assets/original-figures/`: original PDF figure crops.

Shared formulas and lecture provenance remain in `content/formulas.json` and
`content/documents.json`. Their existing local resource paths are unchanged.

## Writing an article

The YAML frontmatter contains metadata, not the question or worked prose:

- Stable problem ID, number, bilingual title/topic, points and given equations.
- Figure names, bilingual captions, PDF page/crop coordinates and lecture references.
- A `parts` array with each part's stable ID, printed label, points, source and
  solution page, and optional question/solution figure metadata.

Preserve IDs such as `e1-f26-q1` and `e1-f26-q1-ai`; URLs, bookmarks and learning
records depend on them. The filename must match `number`, for example `q1.md`.
YAML plain or single-quoted TeX uses a single backslash: `\epsilon`, not `\\epsilon`.
Quoted strings containing TeX should use single quotes to avoid YAML escapes.

The Markdown body uses these exact headings:

- `## Question`: `### English` for verbatim original wording and `### 中文` for
  its faithful translation.
- `## Guide`: four subsections, `### Concepts`, `### Givens`, `### Goal` and
  `### Approach`. Each contains `#### English` and `#### 中文` prose.
- `## Part a`, or the exact printed label from frontmatter, such as `## Part a(i)`.
  Its `### Question` contains `#### English` and `#### 中文`.
- Each part has consecutive `### Step 1`, `### Step 2`, etc., with as many
  equation groups as the calculation needs. `#### Equation` is required and
  holds one display equation between `$$` lines; use `aligned` for a calculation
  chain. Equations are shared by the two languages. Use `\because` and
  `\therefore` in TeX where they clarify a condition or deduction.
- For short lead-ins, add both `#### English` and `#### 中文` under that step;
  they appear before its equation. Prefer this flow: “use these crib sheet
  formulas” → “given …, find …” → “substitute … into …” → “this gives …”.
  Identify question-supplied definitions and earlier derived results accurately.
  Annotations remain optional; do not repeat prose for every algebraic line.
- Cite formulas where their names naturally occur in each annotation, for
  example `使用 [高斯定律](formula:gauss)` and `Use [Gauss’s law](formula:gauss)`.
  IDs refer to `formulas.json`; both languages must reference the same formulas.
  Source IDs are derived from these links, with no separate list to maintain.
  The text inherits the paragraph’s typography, previews the original excerpt
  with the native Hover Card, and opens its PDF location on activation.
  Keep source tags out of the equation row.
- A legacy `#### References` list of typed links remains supported for an
  equation-only step, for example `- [velocity](formula:velocity)`. The interface
  renders it as a short source sentence before the equation; prefer inline
  links when an annotation is present.
- `### Answer` holds one display equation for the final result. An optional
  `### Answer text` holds bilingual concluding prose. The interface incorporates
  the result into the last derivation step using KaTeX boxed emphasis, without
  displaying an extra answer heading or card.
- `### Source correction` inside a part, or `## Source correction` for the whole
  problem, contains the appropriately nested English and Chinese sections.

Body text supports paragraphs, emphasis, lists, inline code, fenced code and
links; math uses `$...$` or display `$$` blocks. Raw HTML is escaped and links
cannot execute script URLs. Source figures are attached through metadata so
both themes, original-image switching and PDF citation actions remain available.
Headings are structural: do not add arbitrary subheadings inside a prose section.

Every worked part starts with its governing equation, followed by actual
substitutions and intermediate algebra or calculus. Retain all integration
elements, limits, antiderivatives, boundary constants, units, vector directions
and source-correction notes. Do not silently repair an original question's givens.
The guide introduces actual givens and starting ideas, never computed answers.

## Discovery, validation and pages

Astro's `questions` collection in `src/content.config.ts` discovers the articles
and validates frontmatter. `content/markdown.ts` reads the body through a Markdown
syntax tree, preserving the original strings and TeX. `content/papers.server.ts`
assembles papers in memory; `schema.ts` validates translations, equations, IDs,
formula references, PDF pages and citation bounds. CLI checks use the same parser
and schema as Astro pages. No intermediate question-bank JSON is written.

Astro prerenders `/problems/{stable-id}/` for every active article. Each page
contains its own full problem and only a solution-free navigation/search index
for other problems. The Svelte study island preserves shared interaction state
across Astro navigation; browser history, deep links and local progress still work.
Native Bits UI portals use `#fieldnotes-overlays`, an independently persisted
mount point, so dialogs, sheets and tooltips remain usable after a page swap.

## Add, edit or remove a paper

1. Create a folder such as `exam1_f27` and author its metadata-only `paper.json`.
2. Add one complete bilingual `questions/q{number}.md` per problem.
3. Add source records, PDFs, page images, SVGs, original crops and extracted text.
   Resource paths in `documents.json` are relative to that paper's `assets/`.
4. Add `generate_figures.py`, exporting `render_figures(save, dark)`.
5. Run `bun run check`, `bun test` and `bun run build`.

Changing Markdown updates the site directly. The development server watches
article additions/removals, metadata changes and asset changes. Navigation,
exam-number tabs and counts derive from active content.

Move a whole paper outside `content/` to unplug it, then rebuild. Its routes and
staged assets disappear. Historical progress, bookmarks, reveal counts and legacy
notes survive, but inactive records do not count toward active progress.

`bun run content:check` validates without generating content. `bun run
papers:prepare` copies only `assets/` into the ignored `static/papers/` staging
directory. Markdown, JSON, extracted text and Python sources are never staged.
Edit canonical assets in the owning paper, never the staging directory.

## Drawings and source checks

```bash
python3 content/exam1_f26/generate_figures.py
python3 scripts/generate_figures.py --paper exam1_f26
python3 scripts/generate_figures.py
python3 scripts/check_figures.py
python3 scripts/check_sources.py
```

Python handles scientific drawings, PDF image assets and verification only.
It reads YAML frontmatter to find citation metadata, never the worked Markdown
body. Install `scripts/requirements.txt` for offline source tools. Ordinary site
development and builds require only Bun and the JavaScript dependencies.
