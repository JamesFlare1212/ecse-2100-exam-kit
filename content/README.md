# Markdown paper library

English and Simplified Chinese papers are independent files and assets:

```text
content/
  en/exam1_f26/
    paper.json
    questions/q1.md
    documents.json
    figure-sources.json
    generate_figures.py
    extracted/
    assets/{sources,pages,figures,original-figures}/
  zh-cn/exam1_f26/
    ...the same independently owned files and directories...
```

Each problem has an [English article](en/exam1_f26/questions/q1.md) and a
[Chinese article](zh-cn/exam1_f26/questions/q1.md). Neither contains the other
language's prose or bilingual frontmatter. PDFs and images are separate copies,
including identical originals; do not introduce cross-language fallbacks or
symlinks. A Chinese asset copy of an English PDF remains that original English
PDF with its original SHA-256 provenance.

Names follow `exam{number}_{f|s}{year}`: `exam1_f26` means Exam 1, Fall 2026.
Both language trees are discovered automatically. Matching stable IDs pair files
into one study problem, preserving `/problems/{id}/` and saved records. A pair
counts once in navigation and progress.

## Paper ownership

Each language's paper owns metadata-only `paper.json`, single-language
`questions/q{number}.md`, PDF provenance in `documents.json`, crop metadata in
`figure-sources.json`, drawing configuration in `generate_figures.py`, extracted
PDF text in `extracted/`, and all PDFs/page images/SVGs/original crops in `assets/`.
SVGs retain both color themes. Document resource paths are relative to that
paper's own `assets/`.

Edit each language directly. Stable IDs, points, physical givens and source
metadata must agree across the pair. Guides and solutions are complete independent
Markdown strings: paragraph order, equation groups and formula references may
differ while preserving the same scientific result and full working. Questions
and parts pair by ID, not by paragraph or equation position. Missing counterparts
fail validation instead of silently showing the other language. Shared crib
formulas and lecture provenance remain in `content/formulas.json` and
`content/documents.json`, separate from papers.

## Writing an article

YAML frontmatter holds the stable ID, single-language title/topic, points, given
equations, lecture citations and exceptional figure/part metadata. Never put the
statement, solution or a duplicate answer in frontmatter. Astro and the CLI use
the same schema in `content/metadata.ts`. Plain or single-quoted YAML TeX uses one
backslash: `\epsilon`, not `\\epsilon`.

Avoid repeating defaults:

- The question number comes from the ID; the filename is `q{number}.md`.
- The main figure defaults to the question ID. Its original crop comes from that
  language's `figure-sources.json`, with 0.002 padding on each edge. Keep PDF
  document, page and region provenance there, rather than copying it into articles.
- The main figure caption defaults to the title. Override it only for a meaningful
  caption, such as an explanation of illustrative parameters.
- `parts` is a mapping keyed by the exact printed label, containing overrides only.
  Part IDs derive from the question ID plus the label stripped of punctuation and
  lowercased; preserve exceptions such as `e1-s26-q1-rf` explicitly with `id`.
- A part defaults to zero declared points, the main crop's PDF page, and the same
  solution page. Override `points`, `page` or `solutionPage` when the source differs.
  Zero means the source declares no individual score; do not invent one.
- Optional `figure` names a solution SVG. `questionFigure` names a part-specific
  question SVG, either as a string or `{name, caption}`. Its original crop also
  resolves from `figure-sources.json`. Part captions default to the prompt.

Use these exact structural headings in both languages, with direct prose only in
the file's own language. Do not add `English` or `中文` subsections:

- `## Question`: original English wording, or its faithful Chinese translation.
- `## Guide`: short natural Markdown introducing concepts, givens, goals and the
  starting approach, without mandatory subsections.
- `## Part a` (or the exact printed label, e.g. `## Part a(i)`): the subquestion's
  wording directly beneath the heading.
- `### Solution`: ordinary paragraphs, formula links and displayed TeX blocks.
  The last displayed formula contains the boxed final result, written once.
- Optional `### Source correction`: that part's correction prose.
- Optional `## Source correction` applies to the whole question.

For example:

```markdown
## Part a

当 $Z_L=Z_0=75\,\Omega$ 时，负载处是否发生反射？

### Solution

使用 crib sheet 的[负载反射系数](formula:reflection)：

$$
\Gamma_L=\frac{Z_L-Z_0}{Z_L+Z_0}
$$

已知 $Z_L=Z_0=75\,\Omega$，求负载反射系数。把两阻抗代入，得

$$
\begin{aligned}
\Gamma_L&=\frac{75\,\Omega-75\,\Omega}{75\,\Omega+75\,\Omega}\\
&=\boxed{0}
\end{aligned}
$$

因此负载处无反射。
```

Formula IDs refer to the shared formula library. Native Hover Cards preview the
original excerpt and activate its exact PDF location. Keep formula names in the
prose; do not add source tags beside equations. Each language's actual links
determine its reference rail; there is no parallel reference list to maintain.

The last displayed calculation is the sole authored answer. The UI renders it
directly without generating, comparing or appending an answer. Do not restore
`Step`, `Explanation`, `Equation` or `Answer` wrappers. Preserve all source
corrections. Paragraphs, emphasis, lists, code and links are supported; math uses
`$...$` or `$$`. Optional deeper headings belong to the prose, not to a step
protocol. Raw HTML is escaped and script URLs rejected.

## Worked-example style

Follow governing crib formula → actual givens and goal → substitution → result.
Keep prose short and calculations complete. Identify question-supplied definitions
and earlier results by their actual origin. The guide introduces actual givens and
starting ideas, never computed answers.

For evaluated integrals, substitute the field/density and differential element,
show dot products and constant extraction, then integrate one variable at a time.
Show each antiderivative and upper-minus-lower substitution, including negative
lower limits. Explain unfamiliar area/volume elements briefly at first use.
Never jump straight from a multiple integral to its final area/volume factor.
Keep terms of one sum or difference together when they fit at normal reading size;
reserve continuation rows for meaningful calculation stages.

Retain limits, boundary constants, units, directions, conventions and source notes.
Verify givens and results against official PDFs, expanding abbreviated working.
A cited result from an earlier part may be reused. Drawing, setup-only and
conceptual questions keep their requested scope.

## Discovery and assets

Astro discovers both language trees through its `questions` collection. Collection
IDs have a language prefix; authored IDs and public URLs do not change. The AST
parser in `content/markdown.ts` reads each single-language article;
`content/localization.ts` pairs it with its counterpart. `content/papers.server.ts`
validates and assembles page data in memory. No question-bank JSON is generated.

Each page contains its own full bilingual problem plus a solution-free navigation
index. The persistent Svelte island preserves state across Astro navigation.
Language switching selects that language's figures, original crops, PDF pages and
downloads at `/papers/en/...` or `/papers/zh-cn/...`. Portals remain attached to
`#fieldnotes-overlays` across swaps.

`bun run papers:prepare` copies only `assets/` into ignored
`static/papers/{en|zh-cn}/`. Markdown, metadata, extraction and Python are not
staged. Never edit staging copies. Development watches both language trees.

To add a paper, create matching `en/exam1_f27` and `zh-cn/exam1_f27` directories
with their own complete metadata, articles and assets. Run `bun run check`,
`bun test`, and `bun run build`. Move both language folders outside `content/`
to unplug a paper; routes and both staged copies disappear while saved records
survive without affecting active totals. Removing only one counterpart is an error.

## Drawings and source checks

```bash
python3 content/en/exam1_f26/generate_figures.py
python3 content/zh-cn/exam1_f26/generate_figures.py
python3 scripts/generate_figures.py --paper exam1_f26 --locale en
python3 scripts/generate_figures.py
python3 scripts/prepare_sources.py --locale zh-cn
python3 scripts/check_figures.py
python3 scripts/check_sources.py
```

Batch drawings and checks discover both language directories. Figure reports are
namespaced by language. Python reads frontmatter only for offline asset work;
it never authors or compiles the question-bank body. Install
`scripts/requirements.txt` for these tools. Routine site work requires only Bun
and the JavaScript dependencies.
