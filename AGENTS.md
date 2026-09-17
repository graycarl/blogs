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
├── _layouts/home.html       # 覆盖首页布局（只列出 blog 分类文章）
├── fs/                      # 图片等静态资源
├── blog.md                  # 「博客」栏目页（/blog/）
├── essays.md                # 「随笔」栏目页（/essays/）
├── archive.md               # 年份归档页（/archive/）
├── tags.md                  # 标签聚合页（/tags/）
├── about.md                 # 关于我（/about/）
├── index.md                 # 首页
├── 404.html                 # 404 页面
├── Gemfile / Gemfile.lock   # Ruby 依赖
├── .ruby-version            # Ruby 版本
├── .pi/                     # pi 系统目录（gitignore，Jekyll 亦排除）
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

## 写作规范

- 文章放到 `_posts/blog/`（默认）或 `_posts/essay/`（随笔/感想），文件名必须形如 `YYYY-MM-DD-title.md`
- 分类由 `_config.yml` 的 `defaults` 按目录自动注入（`_posts/blog/**` → `blog`，`_posts/essay/**` → `essay`），**不要**在 front matter 里手写 `categories`
- Front matter 示例：
  ```yaml
  ---
  layout: post
  title: 文章标题
  date: 2026-07-13 12:00
  tags: [tag1, tag2]
  ---
  ```
- `date` 字段请使用当前准确时间（Asia/Shanghai），不要沿用模板中的占位时间（例如 `2026-07-13 12:00`）。
- `tags` 必须是 YAML 数组格式，不要写成 `tags: a, b`
- 图片等静态资源建议放在 `fs/` 目录，引用路径为 `/fs/{filename}`

## 发布流程

- 提交信息使用英文，固定格式：`feat(blog): Add {slug}` 或 `feat(essay): Add {slug}`
- 推送前需用户确认，不要未经确认直接 `git push`
- 详细的写作/阅读/发布流程见 blog skill（`~/.pi/agent/skills/blog/SKILL.md`）

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

## 常见注意事项

1. **不要重新引入 `github-pages` gem**：当前使用独立 Jekyll 4.x + GitHub Actions，切换回 `github-pages` gem 会破坏部署。
2. **不要修改 `.ruby-version` 为不支持的版本**：工作流和本地环境都依赖此版本。
3. **新增 Jekyll 插件**：需要同时加入 `Gemfile` 的 `:jekyll_plugins` 组和 `_config.yml` 的 `plugins` 列表。
4. **Sass 弃用告警**：Ruby 4 + Dart Sass 下 minima 2.5 会触发 import/color 相关 deprecation，已在 `_config.yml` 用 `sass.silence_deprecations` 静默，升级主题前不要随意删除。
5. **`_config.yml` 的 `exclude`**：已排除 `Gemfile`、`Gemfile.lock`、`AGENTS.md`、`.pi/`、`vendor/` 等，新增非站点文件时注意同步。
6. **主题限制**：当前 minima 2.5 不支持原生暗色模式/站内搜索，如需这些功能需换主题或自定义实现。
