---
layout: post
title: "AI Agent 帮我写鸿蒙客户端：全程零人工介入"
date: 2026-08-10 08:46
tags: [ai-agent, harmonyos, deepseek, kimi, coding]
---

最近用 pi + deepseek-v4-flash 写了个 Lumi 的鸿蒙客户端，结果还挺惊喜的。

deepseek-v4-flash 的正式版据说性能大幅提升，正好拿来实测一把。

开工前，我在 AGENTS.md 里备好了鸿蒙开发的相关文档链接和必要指引；Plan 也很简单，背景信息在 Lumi 的 AGENTS.md 里早就有了。之后 deepseek-v4-flash 自主工作了大约一个小时，全程没有任何人工介入，就交付了一个功能基本完备的客户端。更让我没想到的是，它还自主调用鸿蒙开发者工具，在我的手机上真机测试、调试 bug。

不过 deepseek-v4-flash 读不了图，UI 上的细节问题它发现不了。有了「agent 可以直接操作真机」的经验，我换成 Kimi K3，重新开了个 session，让 agent 把界面整体过一遍，用截图把所有 UI 问题找出来。又是大约一个小时的自助工作（K3 确实比较慢），问题被逐个揪了出来。

可这时 K3 的额度已经用完——每月 100 元的订阅实在不经用。我只好再换到 Copilot 里的 Claude，让它照着 K3 列出的问题清单依次修复。大约 30 分钟后，所有 UI 问题全部解决。

整个过程丝滑顺畅，令人心旷神怡。
