---
layout: post
title: blog skill
date: 2026-07-14 07:12
tags: [AI, pi, Jekyll, 工具]
---

为 pi 增加了一个 blog skill，用来管理 `~/Sources/Blogs` 这个 Jekyll 博客仓库。

## 功能

- 写文章：用户给出标题或大纲，skill 负责生成 Markdown、补全 front matter、选择分类目录，预览确认后执行 commit 和 push。
- 读文章：列出 `_posts/blog/` 和 `_posts/essay/` 下的所有文章，或读取指定文章。

## 文件位置

- skill 文档：`~/.shell/apps/agents/skills/blog/SKILL.md`
- pi 软链：`~/.pi/agent/skills/blog -> ~/.shell/apps/agents/skills/blog`

## 写作约定

- 技术文章默认写入 `_posts/blog/`，随笔写入 `_posts/essay/`。
- 文件名格式：`YYYY-MM-DD-{english-slug}.md`。
- front matter 包含 `layout: post`、`title`、`date` 和 `tags`。
- `tags` 使用 YAML 数组格式，AI 根据内容自动提取 3-5 个。
- `date` 使用当前北京时间，避免模板占位时间。
- commit message 格式：`feat(blog): Add {slug}` 或 `feat(essay): Add {slug}`。

## 部署

skill 已通过 `~/.shell/apps/pi/setup.sh` 链接到 pi 配置目录。用户用“写篇博客/随笔”或“列出文章”等意图触发。
