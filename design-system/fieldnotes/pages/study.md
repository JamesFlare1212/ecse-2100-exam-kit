# Study workspace

This page applies the generated Swiss Modernism direction to an engineering study tool.

- Product name: Fieldnotes / 场与波习题室. An academic reading workspace with three columns, not the generator's portfolio page pattern.
- Warm paper background, white surfaces, ink navy text, restrained burnt orange primary action, teal formula references. Define all colors as semantic tokens in the existing global CSS.
- Latin headings: Georgia or a locally available serif. Interface and bilingual body: self-hosted Inter plus system Chinese sans. KaTeX owns mathematical typography. No external font requests.
- Desktop: 250 px navigation, readable central document, 300 px source rail. Below 1180 px move the rail into a Sheet; below 800 px use a navigation Sheet. Keep a full document flow and visible focus.
- Both desktop sidebars can collapse independently from persistent top-bar panel buttons, following the shadcn block trigger pattern. Keep the reader centered at a comfortable maximum width, preserve panel content state and save preferences locally. Collapsed panels are inert; on compact screens these controls open the existing Sheets. Ctrl/Cmd+B toggles exam navigation.
- Native shadcn-svelte primitives: tabs, toggle groups, accordion, tooltip, dialog, sheet, popover, field, progress, buttons, inputs. Preserve their native semantics, keyboard behavior, tokens and variants.
- Illustrations: reproducible Matplotlib SVG with SVG text preserved, plus an original figure switch. Technical labels use standard symbols in both languages; omit boilerplate recreation captions. Reserve a lower-left area for the source-exam action in both views, and preserve drawing height when switching between them.
- Before derivations, introduce the concepts, actual givens, goals and starting approach in the selected language, with links to the relevant lecture PDF pages. Keep the introduction separate from the original exam wording.
- Formulas: comfortable display spacing, horizontal scrolling confined to a formula, units upright. Place KaTeX boxed results inside the final derivation step, without an answer card or extra border. Avoid shrinking entire pages to fit mobile.
- Worked steps display the governing formula before substitution, with the actual intermediate algebra, integration bounds and boundary conditions. A citation link accompanies an equation; it never substitutes for displaying it. Drawing questions explain the surface, common center, radius, normal and enclosed charge. Preserve the detailed bilingual steps.
- Each step can be revealed independently. A practice mode hides solutions until requested. Completion, bookmarks, locale and theme persist locally; source PDFs stay local. Practice is done on paper; omit note-taking and per-part text entry.
- Titles and question wording follow the global locale. Chinese is a faithful translation of the original exam; English retains the original wording. Use a single question block with no separate translation switch or supplemental panel.
- Source links show a cropped original excerpt on hover/focus and open a page viewer with a percentage-based bounding rectangle. Page numbers always mean 1-based PDF pages.
- All drawings that are schematic or use illustrative parameter values must say so in the caption. Recreated source geometries preserve the source's symbolic dimensions.
- Source viewer: use native 36 px buttons and input height, with matching outline controls for pagination and zoom. At sufficient width and height, show a vertical, independently scrolling list of all page thumbnails. Highlight and reveal the selected page when navigation changes it; clicks change pages, while the current thumbnail also supports pointer/keyboard positioning within the main page. Keep the original citation and current viewport markers. Hide this overview on compact screens.
- Motion is subtle and respects reduced motion; no visual reliance on color alone.

- Keep question diagrams as static SVG. An optional 3D cutaway may appear inside a revealed solution, on explicit request. Preserve the original figure switch and the static Gaussian-surface solution drawings; label 3D proportions as schematic.
- Scientific diagram labels are large and bold, including math symbols; position them clear of arrows. Navigate questions through the sidebar only; omit a bottom previous/next pager.
