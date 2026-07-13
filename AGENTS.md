# AGENTS.md — 大灰狼.BLOG

## 项目概述

这是一个基于 **Jekyll 4.3.4** 的个人技术博客，主题使用 **minima 2.5**，部署在 **GitHub Pages** 上，自定义域名 `graycarl.me`。

- 仓库：`https://github.com/graycarl/blogs`
- 站点：`https://graycarl.me/`
- 构建方式：GitHub Actions（非 GitHub Pages 内置构建）
- Ruby 版本：`.ruby-version` 中固定为 `3.3.0`

## 目录结构

```
.
├── _config.yml              # Jekyll 站点配置
├── _posts/                  # 博客文章（Markdown，文件名格式 YYYY-MM-DD-title.md）
├── fs/                      # 图片等静态资源
├── archive.md               # 年份归档页
├── tags.md                  # 标签聚合页
├── about.md                 # 关于我
├── index.md                 # 首页
├── Gemfile / Gemfile.lock   # Ruby 依赖
├── .ruby-version            # Ruby 版本
└── .github/workflows/        # CI/CD 工作流
    ├── pages.yml            # 构建并部署到 GitHub Pages
    └── test.yml             # PR/Push 构建与链接检查
```

## 本地开发

```bash
# 确保 Ruby 版本与 .ruby-version 一致（3.3.0）
bundle install
bundle exec jekyll serve

# 访问 http://localhost:4000
```

## 写作规范

- 新文章放在 `_posts/`，文件名必须形如 `YYYY-MM-DD-title.md`
- Front matter 示例：
  ```yaml
  ---
  layout: post
  title: 文章标题
  date: 2026-07-13 12:00
  tags: [tag1, tag2]
  ---
  ```
- `tags` 必须是 YAML 数组格式，不要写成 `tags: a, b`
- 图片等静态资源建议放在 `fs/` 目录

## 部署

- Push 到 `master` 会自动触发 `.github/workflows/pages.yml`
- 部署源为 GitHub Actions（Settings > Pages > Build and deployment > GitHub Actions）
- 站点通常 1-2 分钟内更新

## CI / 检查

- `.github/workflows/test.yml` 在每次 Push/PR 时运行 Jekyll 构建和 htmlproofer 检查
- htmlproofer 禁用外部链接检查，并允许历史 HTTP 链接（`--no-enforce-https`）
- 部署工作流会跳过 `Gemfile` 的 `:test` 组（`BUNDLE_WITHOUT=test`）

## 依赖更新

- `.github/dependabot.yml` 会自动为 bundler 和 GitHub Actions 创建更新 PR
- 如需手动升级：修改 `Gemfile` 版本约束，然后 `bundle update` 并提交新的 `Gemfile.lock`
- `Gemfile.lock` 必须提交到仓库

## 常见注意事项

1. **不要重新引入 `github-pages` gem**：当前使用独立 Jekyll 4.x + GitHub Actions，切换回 `github-pages` gem 会破坏部署。
2. **不要修改 `.ruby-version` 为不支持的版本**：工作流和本地环境都依赖此版本。
3. **新增 Jekyll 插件**：需要同时加入 `Gemfile` 的 `:jekyll_plugins` 组和 `_config.yml` 的 `plugins` 列表。
4. **主题限制**：当前 minima 2.5 不支持原生暗色模式/站内搜索，如需这些功能需换主题或自定义实现。
