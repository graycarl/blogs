# AGENTS.md — 大灰狼.BLOG

## 项目概述

这是一个基于 **Jekyll 4.3.4** 的个人技术博客，主题使用 **minima 2.5**，部署在 **GitHub Pages** 上，自定义域名 `graycarl.me`。

- 仓库：`https://github.com/graycarl/blogs`
- 站点：`https://graycarl.me/`
- 构建方式：GitHub Actions（非 GitHub Pages 内置构建）
- Ruby 版本：`.ruby-version` 中固定为 `4.0.5`

## 目录结构

```
.
├── _config.yml              # Jekyll 站点配置（导航、分类 defaults、Sass、exclude）
├── _posts/                  # 博客文章（文件名格式 YYYY-MM-DD-title.md）
│   ├── blog/                # 博客分类（categories: [blog]）
│   └── essay/               # 随笔分类（categories: [essay]）
├── _includes/footer.html    # 覆盖 minima 页脚（兼容 site.author 为字符串/哈希）
├── _includes/header.html    # 覆盖 minima 头部（导航 + 主题切换按钮）
├── _includes/head.html      # 覆盖 minima head（theme-color + 主题初始化内联脚本，防 FOUC）
├── _includes/post-list.html # 文章列表组件（首页/博客/随笔/归档共用，支持按年份分组）
├── _layouts/home.html       # 覆盖首页布局（只列出 blog 分类文章）
├── assets/main.scss         # 覆盖 minima 样式入口（导入 minima 后追加自定义样式）
├── assets/js/theme-toggle.js # 亮/暗主题切换（自动→亮色→暗色 三态循环，localStorage 持久化）
├── fs/                      # 图片等静态资源
├── blog.md                  # 「博客」栏目页（/blog/）
├── essays.md                # 「随笔」栏目页（/essays/）
├── archive.md               # 年份归档页（/archive/）
├── about.md                 # 关于我（/about/）
├── index.md                 # 首页
├── 404.html                 # 404 页面
├── Gemfile / Gemfile.lock   # Ruby 依赖
├── .ruby-version            # Ruby 版本
├── .pi/                     # pi 系统目录（gitignore 仅放行 prompts/、scripts/，Jekyll 亦排除）
│   ├── prompts/             # /pub-blog、/pub-essay 发布流程模板
│   └── scripts/             # img-frame.py（窗口框合成）、img-frame-check.py（回归校验）
└── .github/workflows/       # CI/CD 工作流
    ├── pages.yml            # 构建并部署到 GitHub Pages
    └── test.yml             # PR/Push 构建与链接检查
```

## 本地开发

```bash
# 确保 Ruby 版本与 .ruby-version 一致（4.0.5）
bundle install
bundle exec jekyll serve

# 访问 http://localhost:4000
```

## 写作与发布流程（Blog / Essay）

本节是写作、阅读、发布文章的**唯一权威入口**（原 `~/.pi/agent/skills/blog` skill 的内容已全部合并到此文件，该 skill 已删除）。

### 触发场景

- 「写篇博客 / 随笔 / Blog / Essay，关于 xxx」→ 走写作流程
- 「列出所有文章」/「我最近写了什么」→ 走阅读流程的「列出」
- 「读一下 / 打开 / 查看某篇文章」→ 走阅读流程的「读取」

### 写作流程

1. **判断分类**
   - 用户明确说「随笔 / essay / 感想」→ 存到 `_posts/essay/`
   - 否则默认存到 `_posts/blog/`
   - 分类由 `_config.yml` 的 `defaults` 按目录自动注入（`_posts/blog/**` → `blog`，`_posts/essay/**` → `essay`），**不要**在 front matter 里手写 `categories`
2. **生成英文 slug**：把标题翻译成简洁、URL 友好的英文，全部小写，空格和标点替换为 `-`，去掉多余 `-`
   - 例：`AI 帮我升级博客基础设施` → `ai-helps-update-blog-infrastructure`
3. **确定文件名**：`_posts/{blog|essay}/YYYY-MM-DD-{slug}.md`
   - 例：`_posts/essay/2026-09-17-time-to-push-myself.md`
4. **生成 front matter**：`title` 保留原始语言，正文中**不要**再重复标题
   ```yaml
   ---
   layout: post
   title: "文章标题"
   date: 2026-09-17 23:10
   tags: [tag1, tag2, tag3]
   ---
   ```
   - `date` 用 `TZ=Asia/Shanghai date "+%Y-%m-%d %H:%M"` 取当前准确时间，**不要**沿用模板/示例里的占位时间（如 `2026-07-13 12:00`）
   - `tags` 必须是 YAML 数组格式，按内容自动提取 3-5 个相关标签，**不要**写成 `tags: a, b, c`
5. **撰写正文**：完整、连贯的 Markdown，内容准确、精炼、有条理，避免无意义的情绪化表达
6. **预览并确认**：向用户展示文件完整路径、front matter、正文前 200 字摘要、拟用的 commit message，并询问是否确认发布
7. **提交并推送（仅在用户确认后执行）**
   ```bash
   git add _posts/{blog,essay}/YYYY-MM-DD-{slug}.md
   git commit -m "feat(essay): Add {slug}"   # 或 feat(blog): Add {slug}
   git push
   ```
   - 提交信息固定英文格式：`feat(blog): Add {slug}` 或 `feat(essay): Add {slug}`
   - **推送前必须取得用户确认**，不要未经确认直接 `git push`
   - 用户要求修改 → 回到第 5/6 步；用户放弃 → 不要创建文件，或删除已创建但未提交的文件

### 阅读流程

- **列出文章**：`ls -1 _posts/blog _posts/essay`，展示日期 + 标题/关键词
- **按关键词定位**：`rg -i "keyword" _posts --files-with-matches`；命中多篇时列出候选让用户选择
- **读取文章**：读取 `_posts/{blog,essay}/YYYY-MM-DD-title.md`，展示全文，必要时总结要点

### 静态资源

- 图片等静态资源建议放在 `fs/` 目录，引用路径为 `/fs/{filename}`
- 图片文件名建议带日期前缀：`17-08-03-xxx.png`；发布流程按 `YY-MM-DD-{原名}[-window].png` 命名
- 草稿里对图片有处理要求（如「加个 macOS 窗口框」）时，先按《图片预处理（窗口框合成）》一节处理再拷贝

## 图片预处理（窗口框合成）

草稿里带「处理要求」的图片，发布前要先合成 macOS 窗口效果（圆角窗口 + 标题栏 + 交通灯 + 投影），再进 `fs/`。本节是这套规则的唯一权威；`.pi/prompts/pub-blog.md` 与 `.pi/prompts/pub-essay.md` 只负责触发流程。

### 注解语法（自然语言式）

草稿中的图片引用形如：

```md
![表注文字, 加个 macOS 窗口框](local/img/app.png)
![表注文字, 套个窗口框，标题栏写 TableLite，浅灰色](/Users/me/Desktop/截屏 2026-10-09 00.46.55.png)
```

- 图注与要求之间用**逗号**分段：第一段是图注（发布稿里保留为 alt），其余段是**自然语言要求**
- 要求由 agent 理解后翻译成脚本参数；脚本只接受结构化参数，不做自然语言解析
- 路径支持相对草稿目录、`local/...`、绝对路径（可含中文与空格）

### 处理流程（强制执行）

1. 扫出最终稿里所有图片引用，按「图注 / 路径 / 要求」列给用户过目
2. **没有要求**的图 → 按原逻辑直接拷贝进 `fs/`，不做任何处理
3. **有要求**的图 → 先跑 `--dry-run --json`，用一句话说明「将要做什么」，经 `ask_user` 确认后再落盘
4. 要求**超出脚本能力** → 停下问用户（改脚本 / 换要求 / 放弃）；不要硬凑、不要静默忽略、不要自行删图
5. 发布稿把引用改成 `/fs/...`，并把图注中逗号后的要求段**删掉**（只留第一段）；**草稿文件本身不改**
6. 原图（桌面、`local/` 下的图）**永不修改、永不删除**
7. `fs/` 命名：未处理 `fs/YY-MM-DD-{原名}.png`；合成过 `fs/YY-MM-DD-{原名}-window.png`（`shadow-only` 用 `-shadow`）。日期取发布当天；同名直接覆盖，因此重复执行结果一致

### 调用

```bash
S=.pi/scripts/img-frame.py
python3 $S <src> -o fs/26-10-10-app-window.png                                # 白底标题栏 + 交通灯 + 投影，不写标题（默认）
python3 $S <src> -o fs/26-10-10-app-window.png --title "TableLite" --bar gray  # 灰底标题栏 + 居中标题
python3 $S <src> -o fs/26-10-10-app-window.png --title "TableLite" --title-align left
python3 $S <src> -o fs/26-10-10-app-shadow.png --style shadow-only             # 只加圆角与投影
python3 $S <src> -o fs/26-10-10-app-window.png --no-shadow                    # 不画投影
python3 $S <src> -o fs/26-10-10-app-window.png --dry-run --json               # 只看计划，不落盘
```

| 参数 | 说明 |
| --- | --- |
| `--style window`（默认）/ `shadow-only` | 圆角 + 标题栏 + 交通灯 + 投影 / 只加圆角与投影 |
| `--title` / `--title-align center\|left` | 标题文字（默认不写）；`center` 为窗口居中，`left` 为紧跟交通灯右侧 |
| `--bar white`（默认）/ `gray` | 标题栏底色；`gray` 自带 1px 分隔线 |
| `--no-shadow` / `--radius PT` | 去掉投影 / 圆角半径（默认 17pt） |
| `--scale auto`（默认）/ `1` / `2` | 渲染倍率：DPI ≥ 120 或宽 ≥ 1400px 判为 2x，输出写入 144 / 72 dpi |
| `--dry-run` / `--json` | 不落盘 / 结构化输出（供 agent 汇报与确认） |

**能力边界**：只做「在图片外圈套一层窗口」——不重绘窗口内部、不裁剪、不修图、不生成浏览器/终端等其它窗口样式。

### 视觉规格与回归验证

`SPEC` 常量以 `fs/26-09-26-tablelite-main-window.png`、`fs/26-09-26-tablelite-query-editor.png` 两张真实 `screencapture -w` 素材为基准标定：画布外边距 38/56/74pt（上/左右/下）、圆角 17pt、标题栏 28pt、交通灯直径 13pt 间距 10pt、三层投影。真实窗口风格并不唯一——`fs/26-10-09-pi-status-tmux.png` 是另一种更重的浮动窗口投影，**不作为基准**。

```bash
python3 .pi/scripts/img-frame-check.py   # 退出码 0=通过；比对外边距、圆角内缩与三条投影剖面
```

改动 `SPEC` 后必须跑一次；判定线：投影剖面平均差 ≤ 3/255、单点 ≤ 25/255，圆角内缩差 ≤ 3px，画布外边距相差 ≤ 2px。

**依赖**：Python 3 + Pillow（本机 `/opt/homebrew/bin/python3` 自带，缺失时 `python3 -m pip install --user pillow`）。字体：拉丁 `/System/Library/Fonts/SFNS.ttf`（回退 Helvetica/Arial），中文 PingFang → Hiragino Sans GB → STHeiti（本机无 PingFang）。

## 发布到墨问（MoWen）

同一篇文章可以额外同步到墨问（`mocli` CLI）。墨问正文不是 Markdown，而是 NoteAtom 语法树 JSON，需先转换再用 `mocli note create --file` 提交。转换时有两个反复踩到、值得先记住的点：

### 区块间距（空段落）

墨问渲染器自带块间距，**不要在每个 block 之间机械插入空段落**，否则会渲染出大量多余留白。

- **要加**一个空段落（`{ "type": "paragraph" }`）：仅用于分隔「普通段落 ↔ 普通段落 / 列表 / 引用块」
- **不要加**空段落的位置：
  - H1/H2/H3 标题之前、之后 —— 标题紧贴其正文
  - 同一列表的列表项之间 —— 列表项连排
  - 连续引用块（`quote`）之间
  - 图片（`image`）之前、之间、之后
  - 内链笔记（`note`）节点前后
  - 文档开头与结尾

### 跨平台链接：优先用墨问内链

- 被引用的文章若在墨问上也有对应笔记，**不要**外链到 `graycarl.me`，改用独立的 `note` 节点引用墨问笔记 ID：
  `{ "type": "note", "attrs": { "uuid": "<墨问 note_id>" } }`
- 内链节点单独成块，正文里用纯文本说明（如「在上篇文章中，我解释…」），**不再保留 `link` mark**
- 因此需要维护「博客文章 slug ↔ 墨问 note_id」的对应关系
- 只有墨问上没有对应笔记时才保留外链，且要用**绝对 URL**（墨问里相对路径不可用）

## 部署

- Push 到 `master` 会自动触发 `.github/workflows/pages.yml`
- 部署源为 GitHub Actions（Settings > Pages > Build and deployment > GitHub Actions）
- 站点通常 1-2 分钟内更新

## CI / 检查

- `.github/workflows/test.yml` 在每次 Push/PR 时运行 Jekyll 构建和 htmlproofer 检查
- htmlproofer 禁用外部链接检查，并允许历史 HTTP 链接（`--disable-external --ignore-empty-alt --no-enforce-https`）
- 部署工作流会跳过 `Gemfile` 的 `:test` 组（`BUNDLE_WITHOUT=test`）

## 依赖说明（Gemfile）

- `jekyll ~> 4.3.4` + `minima ~> 2.5`
- `kramdown-parser-gfm`：保持 GitHub Flavored Markdown 解析行为一致
- `csv` / `base64`：Ruby 3.4+/4.x 将部分标准库改为默认不安装，需显式声明
- `:jekyll_plugins` 组：`jekyll-feed`、`jekyll-seo-tag`、`jekyll-sitemap`（需同时列在 `_config.yml` 的 `plugins` 中）
- `:test` 组：`html-proofer`（部署时通过 `BUNDLE_WITHOUT=test` 跳过）

## 依赖更新

- `.github/dependabot.yml` 会自动为 bundler 和 GitHub Actions 创建更新 PR
- 如需手动升级：修改 `Gemfile` 版本约束，然后 `bundle update` 并提交新的 `Gemfile.lock`
- `Gemfile.lock` 必须提交到仓库

## 亮/暗主题

- 默认**跟随系统**（`prefers-color-scheme`），页头导航末尾的按钮可在 **自动 → 亮色 → 暗色 → 自动** 三态间循环
- 状态仅存于 `localStorage.theme`（`auto` / `light` / `dark`），无服务端参与，也无需 `_config.yml` 配置
- 实现拆成三处，改样式时注意保持同步：
  1. `_includes/head.html`：`<html>` 上同步写入 `data-theme`（在样式表之前，避免刷新闪烁）+ 加载 `theme-toggle.js`
  2. `assets/main.scss`：`@mixin dark-theme` 一次编写，`html[data-theme="dark"]`（手动暗色）与 `@media (prefers-color-scheme: dark) html:not([data-theme="light"])`（跟随系统）两处引入；另含 `.theme-toggle` 图标/按钮样式
  3. `assets/js/theme-toggle.js`：三态循环、`meta[name=theme-color]` 同步、系统偏好变化监听
- 新增暗色样式时请写进 `@mixin dark-theme`，不要在别处硬写 `@media (prefers-color-scheme: dark)`，否则手动切换会失效

## 常见注意事项

1. **不要重新引入 `github-pages` gem**：当前使用独立 Jekyll 4.x + GitHub Actions，切换回 `github-pages` gem 会破坏部署。
2. **不要修改 `.ruby-version` 为不支持的版本**：工作流和本地环境都依赖此版本。
3. **新增 Jekyll 插件**：需要同时加入 `Gemfile` 的 `:jekyll_plugins` 组和 `_config.yml` 的 `plugins` 列表。
4. **Sass 弃用告警**：Ruby 4 + Dart Sass 下 minima 2.5 会触发 import/color 相关 deprecation，已在 `_config.yml` 用 `sass.silence_deprecations` 静默，升级主题前不要随意删除。
5. **`_config.yml` 的 `exclude`**：已排除 `Gemfile`、`Gemfile.lock`、`AGENTS.md`、`.pi/`、`vendor/` 等，新增非站点文件时注意同步。
6. **主题限制**：minima 2.5 没有原生暗色模式/站内搜索。暗色模式已由本项目自行实现（见「亮/暗主题」），站内搜索仍需换主题或额外方案。
7. **图片预处理**：改动 `.pi/scripts/img-frame.py` 的视觉常量（`SPEC`）后必须跑 `python3 .pi/scripts/img-frame-check.py`；输出的窗口框图（`fs/*-window.png`）请勿再交给脚本处理第二遍，否则会「框套框」（脚本仅在 stderr 提醒，不阻断）。
