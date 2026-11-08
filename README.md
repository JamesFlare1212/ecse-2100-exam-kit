# Fieldnotes · 双语考试学习工作台

可迁移到不同科目与考试的静态学习工作台：通用界面、课程配置与 Markdown 试卷包分开维护，解题风格固定在独立规范中。仓库保留完整的 **ECSE 2100 / Fields and Waves I** 示例，覆盖 **5 套试卷、20 道大题、93 个小问**；模板化不删除示例，也不改变现有 URL 和学习记录。

## 文档入口

| 要做什么 | 从这里开始 |
|----------|------------|
| 第一次贡献或提交内容 PR | [贡献流程](CONTRIBUTING.md) |
| 换科目、换考试，了解哪些文件该改 | [迁移与项目边界](docs/template-guide.md) |
| 编写或审阅解答，保持风格一致 | [解题风格规范：双语例子、反例与检查清单](docs/solution-style.md) |
| 复制一篇文章或一份课程配置 | [不进入正式题库的模板](templates/README.md) |
| 添加试卷、登记 PDF、理解 Markdown 结构 | [内容与资源契约](content/README.md) |
| 维护当前示例的科学约定与纠错记录 | [ECSE 2100 课程说明](docs/courses/ecse-2100.md) |

`content/course.json` 是课程标识、默认题目、浏览器存储键、讲义目录与公式表文档的统一配置入口。页面标题、资源名称与数量由配置和来源数据生成，不再要求每门课都有 15 讲或 10 页公式表。

## 启动

环境要求：Bun 版本以 `package.json` 的 `packageManager` 为准；完整开发校验还需安装 Node.js（与 CI 一致使用 Node 24），`svelte-check` 和类型检查回归测试会直接调用 `node`。开发服务器、内容校验和静态构建使用 Bun；只有离线 PDF/绘图工具需要 Python，CI 验证 Python 3.12 和 3.14。

```bash
cd ecse-2100-exam-kit
bun install --frozen-lockfile
bun run dev
```

打开终端显示的地址（默认 http://127.0.0.1:5173）。 `bun run build` 输出可静态托管的 `build/`；`bun run preview --host 127.0.0.1` 可预览构建结果。现有资源包含 PDF、页图和 SVG，运行网页无需 Python 或外部服务。

课程 PDF 允许随站点发布，`build/` 会包含供浏览和下载的 PDF；这与 Git 提交限制是两回事。不要把新增的大型 PDF 文件提交到 Git，应在本地或构建环境中将它们放入所属的规范资源目录，再构建和发布。保留已有 PDF、SHA-256 来源记录及双语独立副本；常规编辑不删除现有文件、不改变其跟踪状态，也不改写 Git 历史。

每道大题分别在 `content/en/exam1_f26/questions/q1.md` 和 `content/zh-cn/exam1_f26/questions/q1.md` 保存独立的单语言 Markdown。两边各自拥有试卷元数据、PDF、SVG、页图、提取文本和绘图配置，相同素材也分别保留。YAML frontmatter 保存标题、分值、来源和必要的元数据覆盖；题号、默认图名和裁图来源自动推导。正文只需 `Question`、`Guide`、`Part` 和 `Solution` 等结构标题，直接书写段落与公式，最终方框结果仅写一次。两种语言按题目和小问的稳定 ID 配对，保留相同的分值、物理条件和来源信息，各自独立安排解答的段落与公式；一对翻译只计为一套试卷。新增或移除 paper 时同时处理两边目录，无需修改导入清单。编辑规则见 [content/README.md](content/README.md)。开发服务器监听两种语言的文章、元数据和资源变化；各自的 `assets/` 自动复制到 Git 忽略的 `static/papers/en/` 和 `static/papers/zh-cn/`，不要手工编辑暂存目录。

Astro 内容集合负责发现文章和校验 frontmatter，Markdown 语法树解析器分别读取单语言文章，按稳定 ID 组装双语数据，完整保留各语言的正文和原始 TeX；现有内容校验继续检查公式、页码、引用和几何区域。数据仅在内存中组装，没有中间题库 JSON。每题保留独立路径，如 `/problems/e2-s26-q3/`，输出 `build/problems/<题目 ID>/index.html`；关闭 JavaScript 仍能阅读标题、题干和全部小问。根路径静态跳转至默认题目。Astro ClientRouter 处理切题与浏览器历史，持久化 Svelte 学习界面保留跨页面状态。每页只携带当前题的完整解答及不含解答的导航/搜索索引；偏好、进度和旧版记录仍保存在同一个 localStorage 中。

技术栈：Astro 7、Svelte 5、TypeScript、Tailwind CSS 4、原生 shadcn-svelte / Bits UI、Bun、KaTeX。Astro 命令通过 Bun 运行时执行；正文使用自托管 Inter 和系统中文字体，KaTeX 字体本地提供，SVG 内的中文标签嵌入离线裁剪的 Noto Sans SC 字形，不请求远程字体。为支持 OneDrive / WSL 文件系统，开发服务器启用了文件轮询。

Astro 页面由 `astro check` 检查，Svelte 与 TypeScript 检查使用正式版 TypeScript 7.0.2 原生编译器，按 [svelte-check 官方方案](https://github.com/sveltejs/language-tools/tree/master/packages/svelte-check#typescript-7-supports)并存两个依赖：`@typescript/native` 是 `typescript@^7.0.2` 的 npm 别名；`typescript@~6.0.3` 为 Astro 检查工具和 Svelte 文件转换提供仍需的 JavaScript 编译器 API。`bun run check` 与 `bun run check:watch` 中的 Svelte 检查通过 `svelte-check --tsgo` 调用 TS7，CI 使用相同命令。保留 TS6 的兼容 API 符合 [TypeScript 官方迁移说明](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/)；Svelte 编辑器仍使用兼容工具链。Dependabot 继续更新原生编译器，兼容依赖 `typescript` 暂不自动升级主版本。

## 工作台能力（当前 ECSE 2100 示例）

- Exam 1：Fall 2025、Spring 2026、Fall 2026；Exam 2：Fall 2025、Spring 2026。英文标题、题干和全部小问均转录试卷原文，只调整数学排版与换行；中文模式直接展示原题的忠实翻译，标题、题干和小问随全局语言一起切换。全部 93 小问按“使用 crib sheet 公式 → 已知与所求 → 代入 → 得”的例题写法组织双语短注解，放在对应算式前；公式名称直接作为段落内的文字引用，悬停预览原式、点击定位 PDF，题设定义和前问推导结果按实际来源注明。保留积分、边界条件、逐次反射和代数化简，按需用 `\because`、`\therefore` 连接条件和推导。最终结果融入最后一步算式，仅用 KaTeX `\boxed{}` 强调。
- 44 幅可复现的 Matplotlib 原生 SVG，每幅提供浅色与深色版本。30 幅题图按原卷的视角、几何结构、坐标轴、标注与已知/未知量复刻；同轴线和微带线保留 3D 视角。多电路题的图放在各自小问旁。另有 14 幅辅助解题图，只在展开解答后显示。SVG 标注整体放大 30% 并使用粗体数学字体，避开箭头与线条。题图均可切换至原始 PDF 裁图，也可打开完整原卷。
- 球对称题图使用统一正交投影，保持赤道线的远近遮挡、共同球心及半径箭头端点。题面与高斯面解答图均使用静态 SVG，不载入交互三维组件。
- 29 条公式索引：优先采用 crib 原式；悬浮可查看原始截图，点击打开 PDF 页图并以矩形框定位。原表没有的初始分压式明确引用 Lecture 04。
- 20 道题均提供中英文解题导读，先说明考点、已知、所求与起步思路，再进入逐步推导；导读与试卷原题分别排版。
- 原页查看器统一使用 36px 高的翻页、页码与缩放控件。宽屏右侧将全部页面缩略图纵向排列并独立滚动，点击即可切页；当前页高亮，翻页或输入页码时自动显示对应缩略图。保留原引用页的定位框及当前页的视野标记，当前缩略图可点击定位或用方向键滚动原页；空间不足时隐藏概览。
- 每题关联对应讲次与具体 PDF 页码。完整浏览 Lecture 01–15、10 页 crib sheet 和全部原卷/官方答案，共 25 个 PDF、748 页。
- 统一解答视图；在自己的本子上练习，需要时展开完整计算；用同一按钮切换“展开全部推导”与“收起全部推导”：有任意小问展开就全部收起，全部收起时就全部展开。可自行标记掌握情况。题目切换统一使用侧边栏。
- 顶栏左右图标可分别收起试卷导航与公式/课件栏，收起后释放阅读宽度，展开状态保存在本地。Ctrl/Cmd+B 切换左侧导航；手机端使用相同入口打开抽屉，保持桌面偏好。
- 中英文切换，浅色 / 深色主题，首次跟随系统主题；桌面三栏，手机使用原生 Sheet 抽屉。
- 支持题目 / 公式搜索（Ctrl/Cmd+K）；收藏、逐问进度及显示偏好保存在当前浏览器的 localStorage。
- 可分享 `/problems/e2-s26-q3/` 形式的题目链接。数学内容支持 MathML；支持键盘操作、跳转链接和减少动态效果设置。

进度属于当前浏览器，不在设备之间同步；“已掌握”由学习者自行判断。

## 来源核对

所有页码指 **从 1 开始的 PDF 页序**，不是课件中有时不同的幻灯片编号。共享 `content/documents.json` 与各 paper 的 `documents.json` 保存原文件名、页数、尺寸及 SHA-256；公式区域为相对 PDF 页面的 `[x, y, width, height]`，从左上角计。

当前课程的匹配数值、界面反射选项、相量约定、原卷符号冲突与近似模型记录集中保留在 [ECSE 2100 课程说明](docs/courses/ecse-2100.md#来源核对与纠错记录)。详细纠错仍由两种语言的题目 Markdown 各自持有；这些是示例课程的事实，不是迁移到别科时要照搬的模板规则。

## 项目 skills 与 MCP

已执行：

```bash
uipro init --ai universal
bunx skills add huntabyte/shadcn-svelte --agent universal --yes --copy
```

项目 skills 位于 `.agents/skills/ui-ux-pro-max` 和 `.agents/skills/shadcn-svelte`。设计总规则见 [MASTER.md](design-system/fieldnotes/MASTER.md)，当前工作台的细化与覆盖规则见 [pages/study.md](design-system/fieldnotes/pages/study.md)；组件配置在 `components.json`，实际主题 token 定义在 `src/styles/layout.css`。UI 组件由官方 `shadcn-svelte` CLI 安装；原生 Dialog / Sheet 的关闭按钮只增加了一个可翻译的 `closeLabel` 参数。

官方入口：[llms.txt](https://www.shadcn-svelte.com/llms.txt)、[Skills](https://www.shadcn-svelte.com/docs/skills)。该文档入口没有官方独立的 shadcn-svelte MCP 安装项；项目配置使用 [Michael-Obele/shadcn-svelte-mcp](https://github.com/Michael-Obele/shadcn-svelte-mcp) 的文档服务，未将 React 的组件服务器混作 Svelte 组件来源。

项目只在根目录的 `.mcp.json` 中配置 MCP，使用 `mcpServers` 格式，不依赖 VS Code 或其他特定编辑器：

```json
{
  "mcpServers": {
    "shadcn-svelte": {
      "type": "http",
      "url": "https://shadcn-svelte-mcp.svelte-apps.workers.dev/api/mcp/shadcn/mcp"
    }
  }
}
```

支持 `.mcp.json` 的 MCP 客户端可直接加载；其他客户端可将上述服务地址按 HTTP 传输方式添加到各自的 MCP 配置中，无需安装编辑器扩展。

已成功完成 MCP `initialize` 握手：`Shadcn Svelte Docs`，版本 `1.10.0`，协议 `2025-03-26`。配置后需在客户端重新载入 MCP 或新建会话，不会把新的 MCP 动态注入已经运行的对话。MCP 只用于开发文档查询，网页运行不依赖该服务。

## 校验与重新生成

GitHub Actions 配置位于 `.github/workflows/ci.yml`，在推送到 `main`、创建或更新 PR 时自动运行，也支持手动触发。前端任务按 `package.json` 指定的 Bun 版本安装锁定依赖，校验 Markdown 题库和元数据，并运行下面的类型检查、测试和静态构建，全程无需 Python。独立的 Python 图像工具任务覆盖 3.12 和 3.14，验证依赖一致性、25 个 PDF 的 SHA-256 与页尺寸、全部页面的文字提取、引用区域渲染与 WebP 编解码，以及全部图形两种主题在 Matplotlib 生成阶段的标注布局和球形几何，并核验交付 SVG 的内嵌字体；这些检查不覆盖中文标签替换后的最终文字碰撞，仍需目视复核。CI 不会改写原始素材；当前工作流也不上传课程 PDF 或站点构建产物，这不是禁止站点发布 PDF 的规则。图形检查失败时保留 7 天的诊断图片和报告。

Dependabot 配置位于 `.github/dependabot.yml`，每周一纽约时间 09:00 检查 GitHub Actions、根目录的 Bun 依赖和 `scripts/requirements.txt` 中的 Python 依赖。Actions 更新按组提出；Bun / Python 次版本与补丁更新分别按生态分组提出 PR，主版本更新单独提出，不自动合并。

对于加入 CI 前已存在的 PR，可手动运行 `gh workflow run ci.yml -f ref=refs/pull/123/merge`，验证该 PR 与当前主分支的合并结果；手动运行记录显示在 Actions 中，之后的 PR 更新会正常触发 PR 检查。

```bash
bun run check
bun test
bun run build
```

内容测试包含两种语言的独立文章与资产、KaTeX 公式、全部 PDF 页图、SVG 两种主题、PDF 页码与矩形引用，还包括匹配、源/负载边界、瞬态级数、功率、Gauss、电势梯度、微分电容、镜像法及电流密度的一致性检查。

`bun run content:check` 校验课程配置、两种语言的独立 Markdown、配对关系、KaTeX 公式、ID、引用关系、PDF 页码与引用矩形，以及共享来源 PDF/页图、公式摘录和 paper 自有资源是否齐备，不改写内容。`bun run build` 先执行校验，再由 Astro 内容集合构建静态页面；最后自动运行 `scripts/check_prerender.ts`，核对全部 20 个 HTML 中实际渲染的题干与 93 个小问，以及每页 Svelte 岛的序列化数据只包含当前题目的完整记录。导航与搜索数据由 TypeScript 在内存中投影，无独立索引文件。新增目录自动纳入构建，移除目录会清理对应的静态页面和资源；默认 paper 缺席时，根路径跳转到现有题目。暂时移除的 paper 的本地学习记录会保留，但不计入当前进度。投影与题库的一致性也包含在 `bun test` 中。

原生类型检查的回归测试在隔离目录中植入 Svelte 脚本、组件属性和通过 `#lib` 引入的 `.svelte.ts` rune 类型错误，检查 TS7 能逐项报错；修正后必须通过，避免迁移时漏掉诊断。

`bun test` 包含通用结构、存储、类型和配置检查，以及不依赖现有题库的非 ECSE 课程夹具与风格示例检查。当前 ECSE 的原题措辞、KaTeX、来源坐标、内容发现和独立物理数值回归保留，并按课程 ID 启用；新课应增加自己的课程回归，不能把电磁学答案当通用规则。`scripts/browser-qa.mjs` 使用真实 Chromium 检查全部题目、小问和公式组，覆盖无脚本阅读、浏览器历史、双语、主题、解答展开、存储兼容、侧栏、搜索、原图和 PDF 查看器，以及手机和平板尺寸。原题英文继续与独立提取的 PDF 文本核对；因公式排版打乱提取顺序的片段保留人工核验记录。

`python3 scripts/check_figures.py` 在相同 Matplotlib 环境中检查两种语言目录下各 44 幅图的两种主题，共 176 组生成阶段布局：检查文字边界框碰撞、指定标注与线条碰撞，以及球形图共享球心、半径端点和径向外法向等几何约束。中文标签由后处理替换到交付 SVG 中，因此这里的碰撞检查和诊断 PNG 不包含替换后的中文排版；交付 SVG 的自动检查仅覆盖下述字体项目，最终中文标签仍须目视检查。检查不改写静态素材，逐图 PNG 和报告写入 Git 忽略的 `artifacts/figure-review/`。

`python3 scripts/check_sources.py` 使用已保存的 PDF 核验来源散列、748 页的尺寸与文字提取，并在内存中验证引用裁图、缩略图拼接和 WebP 编解码，便于检查 PyMuPDF / Pillow 更新的兼容性；无需父目录中的原始文件。

可选浏览器回归脚本为 `scripts/browser-qa.mjs`。先在独立目录安装 Playwright 与 Chromium，再设置 `PLAYWRIGHT_MODULE` 为其模块的绝对路径；对已启动的本机预览运行：

```bash
PLAYWRIGHT_MODULE=/absolute/path/to/playwright/index.mjs \
QA_URL=http://localhost:4173 bun scripts/browser-qa.mjs
```

若浏览器装在自定义位置，同时设置 `PLAYWRIGHT_BROWSERS_PATH`。结果写入 Git 忽略的 `artifacts/`，测试使用独立浏览器上下文，不修改日常浏览器进度。

`scripts/browser-startup-qa.mjs` 使用同样的环境变量，CI 会单独运行；它从课程配置读取存储键，从构建结果选择题目，支持迁移后的课程。它还调用通用 `browser-hover-qa.mjs`，在两种主题和桌面/手机宽度下检查条目的悬浮/焦点底色、边界、小字对比度和尺寸稳定性，诊断截图写入 `artifacts/hover-review/`。通用 `browser-study-ux-qa.mjs` 进一步验证 Sheet→资料库关闭焦点、桌面嵌套来源返回、常态文字对比度、窄屏来源放大/平移及页宽重置，诊断图默认写入 `artifacts/study-ux-review/`。延迟字体检查把内嵌与独立加载字体都计入 200 KiB 预算，失败前保留 `artifacts/font-loading/` 中的前后截图及布局偏移来源；CI 失败时上传浏览器诊断产物。两份关键 KaTeX WOFF2 随 CSS 内嵌，避免公式字体分批到达造成窄屏重排，其余资源沿用 Vite 默认策略。`browser-figure-qa.mjs` 检查图示分段选择器与 Exam 原生样式一致，并覆盖中英、深浅主题、320/390 px 手机及桌面的切图、键盘、放大和高度稳定性；记录写入 `artifacts/figure-segmented/`。`browser-navigation-qa.mjs` 在高低视口、正常/减少动画、深浅主题及两种 DOM 迁移实现下，逐帧检查初始与手动展开试卷的目录高度、滚动和行位置，覆盖跨试卷后连续切题、前进/后退及 Exam 分组切换；截图与记录写入 `artifacts/navigation-stability/`。`browser-qa.mjs` 及阅读、交互、修复、主题、语言等补充回归仍含当前 ECSE 的具体试题用例，迁移时应按新课内容调整，详见迁移指南。它为每道题建立冷缓存上下文，记录从 HTML 响应到正文可见的时间；在手机、桌面和两种语言下扣住脚本及字体，验证静态题目先可读、脚本到达后交互不等字体，并限制晚到字体造成的布局偏移与字体下载量。构建同时限制每页字体预加载不超过 64 KiB。中文正文使用系统中文字体；图内中文仍用离线裁剪的 Noto 字形，`check_figures.py` 会解码交付 SVG 的内嵌字体，检查字形覆盖、多余字符及每图 32 KiB 的字体上限。

编辑题库和构建站点使用 Bun 与已安装的 JavaScript 依赖；运行完整检查和测试还需要 Node.js。只有重新绘图、渲染 PDF 页图及裁图，或核验这些图像工具时才需要 Python。先完成上面的 `bun install --frozen-lockfile`，绘图后处理还会读取其中的本地 Noto 字体包。

从保存的 PDF 完整重建两种语言的页图、公式裁图、SVG 和原题裁图：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r scripts/requirements.txt
python3 scripts/prepare_sources.py --locale en --force
python3 scripts/prepare_sources.py --locale zh-cn --force
python3 scripts/render_excerpts.py
python3 scripts/generate_figures.py
# 也可单独绘制一套 paper
python3 content/en/exam1_f26/generate_figures.py
python3 content/zh-cn/exam1_f26/generate_figures.py
```

`prepare_sources.py` 默认只处理 `en`，已有页图默认跳过；上面的两次显式调用覆盖两种语言，`--force` 强制重绘已有页图。只补齐缺失页图时省略 `--force`；提取文本仍会更新，共享课程页图由两个调用使用同一目录。`generate_figures.py` 默认绘制两种语言，单独限制时使用 `--locale`。`bun run assets:prepare` 是增量入口，会补齐两种语言的缺失页图并重新生成裁图和绘图，不强制重绘已有页图。新增试卷的元数据模板、来源登记和生成顺序见 [新增试卷指南](content/README.md#adding-a-paper)。

每种语言的 paper 使用自己的 `questions/q{number}.md` 保存该语言的题干、导读、完整推导和纠错说明；`paper.json` 仅存试卷元数据。`documents.json` 保存原始 PDF 来源和散列，路径相对于该 paper 的 `assets/`；`figure-sources.json` 保存裁图区域，`generate_figures.py` 保存绘图配置。共享绘图工具与自动发现入口保持不变。Python 仅用 PyYAML 读取文章 frontmatter 中的资源引用以核验来源，不读取或改写正文。PDF 图像工具直接读取 paper 内的 PDF 和共享课程 PDF，只有重新从外部导入时才使用 `--source-dir ..`，并核验已有 SHA-256 记录。
