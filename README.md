# Fieldnotes · ECSE 2100 Back Exams

中英双语的 Fields and Waves I 学习工作台。使用本目录已有的课程资料，完整覆盖 **5 套试卷、20 道大题、93 个小问**。

## 启动

```bash
cd ecse-2100-backexams
bun install --frozen-lockfile
bun run dev
```

打开终端显示的地址（默认 http://localhost:5173）。 `bun run build` 输出可静态托管的 `build/`；`bun run preview --host 127.0.0.1` 可预览构建结果。已包含 PDF、页图和 SVG，运行网页无需 Python 或外部服务。

每套试卷是 `content/exam1_f26/` 这样的独立 paper 目录，包含 `paper.json`、PDF 来源记录、图源坐标、图像/PDF 资源、提取文本和对应的 `generate_figures.py`。构建自动扫描符合命名规则的目录；新增或移除 paper 无需修改导入清单，导航、考试分类和数量也由数据生成。修改 JSON 后直接运行 `bun run build` 即可更新页面；Bun/TypeScript 校验内容，Vite/SvelteKit 直接读取 JSON 并生成静态 HTML，没有题库编译步骤或生成的 JSON 副本。题库结构、校验和编辑约定见 [content/README.md](content/README.md)。开发服务器也会监听 paper 的新增、移除、JSON 编辑和资源变化。`assets/` 是资源源文件，构建和开发启动时自动复制到 Git 忽略的 `static/papers/`；不要手工编辑暂存目录。

每题使用独立路径，如 `/problems/e2-s26-q3/`。构建时枚举全部 20 题，生成 `build/problems/<题目 ID>/index.html`，HTML 已包含对应题目的标题、题干及所有小问；关闭 JavaScript 仍能阅读题面。根路径静态跳转至默认题目。SvelteKit 接管交互后，切题会加载该题预生成的数据并更新浏览器历史，支持刷新、前进后退和在新标签页打开。完整解答题库仅由构建端读取，前端共享的是不含解答的导航与搜索索引，每页只携带当前题目的完整内容；个人显示偏好与学习进度仍在浏览器恢复。

技术栈：Svelte 5、SvelteKit 3、Vite 8、TypeScript、Tailwind CSS 4、原生 shadcn-svelte / Bits UI、Bun、KaTeX。Inter、Noto Sans SC 与 KaTeX 字体均随应用提供，不访问 Google Fonts。为支持 OneDrive / WSL 文件系统，Vite 开发服务器启用了文件轮询。

类型检查使用正式版 TypeScript 7.0.2 原生编译器，按 [svelte-check 官方方案](https://github.com/sveltejs/language-tools/tree/master/packages/svelte-check#typescript-7-supports)并存两个依赖：`@typescript/native` 是 `typescript@^7.0.2` 的 npm 别名；`typescript@~6.0.3` 为 SvelteKit 配置同步和 Svelte 文件转换提供仍需的 JavaScript 编译器 API。`bun run check` 与 `bun run check:watch` 均通过 `svelte-check --tsgo` 调用 TS7，CI 使用相同命令。保留 TS6 的兼容 API 符合 [TypeScript 官方迁移说明](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/)；Svelte 编辑器仍使用兼容工具链。Dependabot 继续更新原生编译器，兼容依赖 `typescript` 暂不自动升级主版本。

## 已实现

- Exam 1：Fall 2025、Spring 2026、Fall 2026；Exam 2：Fall 2025、Spring 2026。英文标题、题干和全部小问均转录试卷原文，只调整数学排版与换行；中文模式直接展示原题的忠实翻译，标题、题干和小问随全局语言一起切换。93 小问共 470 个双语推导步骤，每问 3–9 步：先展示公式，再代入实际条件或数值，展开积分、边界条件、逐次反射和代数化简。最终结果融入最后一步算式，仅用 KaTeX `\boxed{}` 强调。
- 44 幅可复现的 Matplotlib 原生 SVG，每幅提供浅色与深色版本。30 幅题图按原卷的视角、几何结构、坐标轴、标注与已知/未知量复刻；同轴线和微带线保留 3D 视角。多电路题的图放在各自小问旁。另有 14 幅辅助解题图，只在展开解答后显示。SVG 标注整体放大 30% 并使用粗体数学字体，避开箭头与线条。题图均可切换至原始 PDF 裁图，也可打开完整原卷。
- 球对称题图修正了赤道线的远近遮挡、共同球心及半径箭头端点，题面继续使用静态 SVG。第 a) 问解答可按需展开 3D 空间结构工具，支持鼠标、触控、键盘旋转与缩放；模型比例仅为示意，不替代原有高斯面解答图。Three.js 随项目本地打包并按需载入，无法使用 WebGL 时回退至矢量图。
- 29 条公式索引：优先采用 crib 原式；悬浮可查看原始截图，点击打开 PDF 页图并以矩形框定位。原表没有的初始分压式明确引用 Lecture 04。
- 20 道题均提供中英文解题导读，先说明考点、已知、所求与起步思路，再进入逐步推导；导读与试卷原题分别排版。
- 原页查看器统一使用 36px 高的翻页、页码与缩放控件。宽屏右侧将全部页面缩略图纵向排列并独立滚动，点击即可切页；当前页高亮，翻页或输入页码时自动显示对应缩略图。保留原引用页的定位框及当前页的视野标记，当前缩略图可点击定位或用方向键滚动原页；空间不足时隐藏概览。
- 每题关联对应讲次与具体 PDF 页码。完整浏览 Lecture 01–15、10 页 crib sheet 和全部原卷/官方答案，共 25 个 PDF、748 页。
- 精读 / 练习模式；在自己的本子上练习，需要时逐步揭示答案；用同一按钮切换“展开全部推导”与“收起全部推导”：有任意小问展开就全部收起，全部收起时就全部展开。可自行标记掌握情况。题目切换统一使用侧边栏。
- 顶栏左右图标可分别收起试卷导航与公式/课件栏，收起后释放阅读宽度，展开状态保存在本地。Ctrl/Cmd+B 切换左侧导航；手机端使用相同入口打开抽屉，保持桌面偏好。
- 中英文切换，浅色 / 深色主题，首次跟随系统主题；桌面三栏，手机使用原生 Sheet 抽屉。
- 支持题目 / 公式搜索（Ctrl/Cmd+K）；收藏、逐问进度及显示偏好保存在当前浏览器的 localStorage。
- 可分享 `/problems/e2-s26-q3/` 形式的题目链接。数学内容支持 MathML；支持键盘操作、跳转链接和减少动态效果设置。

进度属于当前浏览器，不在设备之间同步；“已掌握”由学习者自行判断。

## 来源核对

所有页码指 **从 1 开始的 PDF 页序**，不是课件中有时不同的幻灯片编号。共享 `content/documents.json` 与各 paper 的 `documents.json` 保存原文件名、页数、尺寸及 SHA-256；公式区域为相对 PDF 页面的 `[x, y, width, height]`，从左上角计。

- Fall 2026 Exam 1 本地仅有包含答案的 PDF，网页题目只转录原题文字；查看原始页面时会看到官方答案。
- Spring 2026 Exam 1 的单支节匹配数值已用输入导纳方程核对，两组精确解为 `(d/λ, ℓ/λ)=(0.275282714,0.307588706)` 与 `(0.378410847,0.192411294)`，原图的不同数值在页面中明确说明。
- Fall 2026 Exam 1 的 Smith 图实阻抗使用给定负载的精确计算值，并注明官方读数与乘法不一致。
- Fall 2026 Exam 1 第 4(e) 问按标准答案选 a、b、c，并逐一计算局部界面反射；整个网络匹配意味着返回馈线的反射相量抵消，不能据此排除 a。
- Fall 2025 Exam 2 的高斯面图按原题使用体电荷密度 ρ₀，说明原解草图中 ρsa 标记的差异；a、b、R 从共同球心画至各自边界，R 与体积分变量分别使用不同符号。
- Fall 2025 Exam 1 的四分之一波线相量明确采用“输入端 z=0、源相位为零”约定，并检查源与负载边界；网页说明它与原解写法的差别。
- Fall 2025 Exam 2 的平板题保留题面给出的电场符号，在解答中按 `E=−∇V` 指出矛盾并解释采用的约定，同时说明能量和电容不受影响；双导体球题明确说明原解所采用的等效点电荷近似。
- 未明确给出小问分值的原题不另行编造配分；Fall 2025 Exam 2 的 2 分 bonus 不计入标称总分。

## 项目 skills 与 MCP

已执行：

```bash
uipro init --ai universal
bunx skills add huntabyte/shadcn-svelte --agent universal --yes --copy
```

项目 skills 位于 `.agents/skills/ui-ux-pro-max` 和 `.agents/skills/shadcn-svelte`。设计规则保存在 `design-system/fieldnotes/MASTER.md` 与 `pages/study.md`，组件配置在 `components.json`。UI 组件由官方 `shadcn-svelte` CLI 安装；原生 Dialog / Sheet 的关闭按钮只增加了一个可翻译的 `closeLabel` 参数。

官方入口：[llms.txt](https://www.shadcn-svelte.com/llms.txt)、[Skills](https://www.shadcn-svelte.com/docs/skills)。该文档入口没有官方独立的 shadcn-svelte MCP 安装项；项目配置使用 [Michael-Obele/shadcn-svelte-mcp](https://github.com/Michael-Obele/shadcn-svelte-mcp) 的文档服务，未将 React 的组件服务器混作 Svelte 组件来源。

`.mcp.json` 与 `.vscode/mcp.json` 都已配置 HTTP MCP：

```text
https://shadcn-svelte-mcp.svelte-apps.workers.dev/api/mcp/shadcn/mcp
```

已成功完成 MCP `initialize` 握手：`Shadcn Svelte Docs`，版本 `1.10.0`，协议 `2025-03-26`。在支持对应项目配置的客户端中重新载入 MCP 即可使用；安装配置不会把新的 MCP 动态注入已经运行的对话。MCP 只用于开发文档查询，网页运行不依赖该服务。

## 校验与重新生成

GitHub Actions 配置位于 `.github/workflows/ci.yml`，在推送到 `main`、创建或更新 PR 时自动运行，也支持手动触发。前端任务按 `package.json` 指定的 Bun 版本安装锁定依赖，直接校验 JSON 题库，并运行下面的类型检查、测试和静态构建，全程无需 Python。独立的 Python 图像工具任务覆盖 3.12 和 3.14，验证依赖一致性、25 个 PDF 的 SHA-256 与页尺寸、全部页面的文字提取、引用区域渲染与 WebP 编解码，以及全部图形两种主题的标注和球形几何；不会改写原始素材，也不会上传课程 PDF 或站点构建产物。图形检查失败时保留 7 天的诊断图片和报告。

Dependabot 配置位于 `.github/dependabot.yml`，每周一纽约时间 09:00 检查 GitHub Actions、根目录的 Bun 依赖和 `scripts/requirements.txt` 中的 Python 依赖。Actions 更新按组提出；Bun / Python 次版本与补丁更新分别按生态分组提出 PR，主版本更新单独提出，不自动合并。

对于加入 CI 前已存在的 PR，可手动运行 `gh workflow run ci.yml -f ref=refs/pull/123/merge`，验证该 PR 与当前主分支的合并结果；手动运行记录显示在 Actions 中，之后的 PR 更新会正常触发 PR 检查。

```bash
bun run check
bun test
bun run build
```

内容测试包含所有小问与双语字段、KaTeX 公式、748 个页图、SVG 两种主题、PDF 页码与矩形引用，还包括匹配、源/负载边界、瞬态级数、功率、Gauss、电势梯度、微分电容、镜像法及电流密度的一致性检查。

`bun run content:check` 直接校验 JSON 的双语字段、KaTeX 公式、ID、引用关系、PDF 页码与引用矩形，不改写内容。`bun run build` 先执行该校验，再直接从 JSON 静态渲染；最后自动运行 `scripts/check_prerender.ts`，核对全部 20 个 HTML 中实际渲染的题干与 93 个小问，以及每页的 hydration 数据只包含当前题目的完整记录。paper 通过文件系统自动发现，导航与搜索数据通过 TypeScript 在内存中投影，由布局的 server load 提供，无独立索引文件。新增目录自动纳入构建，移除目录会清理对应的静态页面和资源；默认 paper 缺席时，根路径跳转到现有题目。暂时移除的 paper 的本地学习记录会保留，但不计入当前进度。投影与题库的一致性也包含在 `bun test` 中。

原生类型检查的回归测试在隔离目录中植入 Svelte 脚本、组件属性和通过 `#lib` 引入的 `.svelte.ts` rune 类型错误，检查 TS7 能逐项报错；修正后必须通过，避免迁移时漏掉诊断。

交付时检查结果：Svelte / TypeScript 为 0 错误、0 警告；36 项测试通过（12045 次断言）；静态构建通过。另以真实 Chromium 验证了 40 项浏览器场景，覆盖全部题目、470 个推导步骤的公式显示与逐步揭示、公式原页定位、多页缩略图独立滚动与切页、长讲义、原图切换、练习与数据持久化、中英文、主题，以及 4 种手机 / 平板尺寸；无未捕获异常或失败请求。全部 20 题、93 小问、470 个步骤均在 375px 手机宽度下完整展开检查，无页面横向溢出。原题英文正文中 267 个文字片段与 PDF 提取文本直接匹配，另 2 个因公式排版打乱提取顺序的片段已对照原页人工核验。

`python3 scripts/check_figures.py` 在相同 Matplotlib 环境中检查全部 44 幅图的两种主题，共 88 组：文字边界框不重叠，球形图的半径共享球心、箭头止于对应边界、法向从高斯面径向向外，球形文字避开曲线和引线。检查不改写静态素材，逐图 PNG 和报告写入 Git 忽略的 `artifacts/figure-review/`。

`python3 scripts/check_sources.py` 使用已保存的 PDF 核验来源散列、748 页的尺寸与文字提取，并在内存中验证引用裁图、缩略图拼接和 WebP 编解码，便于检查 PyMuPDF / Pillow 更新的兼容性；无需父目录中的原始文件。

可选浏览器回归脚本为 `scripts/browser-qa.mjs`。先在独立目录安装 Playwright 与 Chromium，再设置 `PLAYWRIGHT_MODULE` 为其模块的绝对路径；对已启动的本机预览运行：

```bash
PLAYWRIGHT_MODULE=/absolute/path/to/playwright/index.mjs \
QA_URL=http://localhost:4173 node scripts/browser-qa.mjs
```

若浏览器装在自定义位置，同时设置 `PLAYWRIGHT_BROWSERS_PATH`。结果写入 Git 忽略的 `artifacts/`，测试使用独立浏览器上下文，不修改日常浏览器进度。

编辑题库和构建站点只需要 Bun。只有重新绘图、渲染 PDF 页图及裁图，或核验这些图像工具时才需要 Python：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r scripts/requirements.txt
python3 scripts/prepare_sources.py
python3 scripts/render_excerpts.py
python3 scripts/generate_figures.py
# 也可单独绘制一套 paper
python3 content/exam1_f26/generate_figures.py
```

每个 paper 的 `paper.json` 将原始英文题干、中文译文、导读、完整推导和纠错说明集中保存；`documents.json` 保存该 paper 的原始 PDF 来源和散列，路径相对于它的 `assets/`；`figure-sources.json` 保存原始裁图区域，`generate_figures.py` 保存该 paper 的题图和解题图配置。`scripts/plotting.py` 与 `scripts/question_primitives.py` 只提供共用绘图工具，`scripts/generate_figures.py` 自动发现各 paper 的绘图入口，支持 `--paper exam1_f26`。Python 不编译或改写题库 JSON。PDF 图像工具直接读取 paper 内的 PDF 和共享课程 PDF，只有重新从外部导入时才使用 `--source-dir ..`，并核验已有 SHA-256 记录。
