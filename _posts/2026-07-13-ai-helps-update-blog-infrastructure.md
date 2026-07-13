---
layout: post
title: "AI 帮我更新了博客的基础设施"
date: 2026-07-13 22:45
tags: [blog, jekyll, github-actions, ai]
---

好久没管这个博客了，上一次认真折腾它还是 2018 年。前几天让 AI 帮我梳理了一下项目，发现基础设施已经相当陈旧：Jekyll 3.9.0、依赖老旧、没有 GitHub Actions、连文章标签格式都不统一。于是一鼓作气，让 AI 帮我把整个博客的底层设施翻新了一遍。

## 改动了什么

### 1. 修复文章元数据

- 把 `2016-9-27-ssl-client-side-authentication.md` 重命名为 `2016-09-27-ssl-client-side-authentication.md`，让 Jekyll 正确解析日期
- 把 `2014-01-22-about-gitignore.md` 里的 `tags: git, gitignore` 改成 `tags: [git, gitignore]`
- 给 `博客迁移` 和 `New Blog New Post` 两篇早期文章补齐了标签

这些细节看起来不起眼，但标签页能不能正确聚合就靠它们。

### 2. 升级依赖

博客原来用的是 `github-pages` gem，它会把 Jekyll 版本锁定在 3.9.x。为了用上新版 Jekyll，我把它换成了直接依赖：

- **Jekyll**: 3.9.0 → 4.3.4
- **minima**: 2.5.1 → 2.5.2
- **jekyll-feed / jekyll-seo-tag / jekyll-sitemap**: 升级到当前稳定版
- 新增 `kramdown-parser-gfm` 保持 GitHub Flavored Markdown 的解析行为
- 固定 Ruby 版本为 3.3.0（`.ruby-version`）

`Gemfile.lock` 也重新生成了，Security 那一堆 dependabot 警报终于可以消停了。

### 3. 从 GitHub Pages 内置构建迁移到 GitHub Actions

以前 GitHub Pages 会自动用内置服务构建，优点是无脑，缺点是版本老、看不到日志、出问题只能盲猜。现在改用 GitHub Actions：

- `.github/workflows/pages.yml`：构建并部署到 GitHub Pages
- `.github/workflows/test.yml`：每次 Push/PR 跑 Jekyll 构建 + htmlproofer 检查内部链接
- `.github/dependabot.yml`：自动为 bundler 和 GitHub Actions 创建依赖更新 PR

部署源从 `legacy` 改成了 `GitHub Actions`（需要在仓库 Settings > Pages 里手动切换）。

### 4. 优化 SEO 与站点配置

`_config.yml` 做了不少调整：

- 设置 `url: https://graycarl.me`
- 把英文的 description 换成中文
- 增加 `lang: zh-CN` 和 `author` 信息
- 显式启用 `jekyll-feed`、`jekyll-seo-tag`、`jekyll-sitemap`

这些改动主要是为了 RSS、搜索引擎和社交卡片能正确显示站点信息。

### 5. 新增归档和标签页

以前文章只能按时间流在首页看，现在多了两个页面：

- `/archive/`：按年份归档
- `/tags/`：按标签聚合

同时把 `about.md` 也更新了一下，加上联系方式和链接。

### 6. 新增 AGENTS.md

为了方便以后让 AI 继续维护这个博客，我加了一个 `AGENTS.md`，里面记录了项目结构、本地开发命令、写作规范、部署流程和常见坑。AI 接手时可以快速理解项目。

## 踩过的坑

这次改动不是一帆风顺的，记录几个印象深刻的：

1. **GitHub Actions 第一次部署失败**。原因是我把 `BUNDLE_WITHOUT=test` 放在 `setup-ruby` 步骤上，但 `build` 步骤没有，导致 Bundler 找不到 `html-proofer`。把环境变量移到 job 级别后解决。

2. **htmlproofer 报旧文章的 HTTP 链接**。博客里有很多 2012-2014 年的外链，当年都是 `http://`。htmlproofer 默认要求 HTTPS，只能加上 `--no-enforce-https` 放行这些历史链接。

3. **奇怪的 `BUNDLED WITH 4.0.11`**。本地 Bundler 版本显示是 4.0.11，一度让我以为 lock 文件格式有问题。后来确认这是本地环境自带的版本，CI 的 `ruby/setup-ruby` 会按 lock 文件自动安装对应 Bundler，所以没问题。

4. **AGENTS.md 会被 Jekyll 处理**。虽然它没有 front matter，不会渲染成 HTML，但会作为静态文件复制到 `_site`。最后在 `_config.yml` 的 `exclude` 里把它排除了。

## 现在的状态

- `https://graycarl.me/` 正常访问
- 所有 GitHub Actions 工作流通过
- 依赖全部更新到现代版本
- 本地预览：`bundle install && bundle exec jekyll serve`

## 还留下的尾巴

有几个优化方向还没做，主要是偏体验层的，得等我想好再动：

- 是否换主题（minima 2.5 比较朴素，Chirpy 或 Minimal Mistakes 功能更丰富）
- 图片压缩/转 WebP
- 站内搜索
- 暗色模式
- 评论系统（giscus）

这些不着急，先把基础打稳。博客虽然老了，但换个新底盘之后，感觉又能再写十年。
