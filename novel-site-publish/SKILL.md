---
name: novel-site-publish
description: "Use when 把小说章节同步发布到 Hexo+GitHub Pages 博客站点."
version: 1.0.0
author: anonymous
license: MIT
metadata:
  hermes:
    tags: [小说, 发布, Hexo, GitHub Pages]
    related_skills: [novel-foundation]
---

# 小说站点发布同步（Novel Site Publish）

把 novel-foundation 写出的章节，转换成 Hexo 章节格式，发布到个人博客站点（Hexo + GitHub Pages）。纯流程 + 格式规范，任何 agent 宿主可执行。

## When to Use

- novel-foundation 写好了新章节，要发布到博客站点。
- 需要新增 / 修改 / 删除站点上的小说章节。
- 站点小说内容维护（如清零、重建）。

## 站点信息（按你自己的站点填写）

| 项 | 值 |
|---|---|
| 站名 | <你的站名>（<你的域名>） |
| 技术栈 | Hexo + Butterfly 主题，GitHub Pages 托管 |
| 仓库 | github.com/<username>/<username>.github.io（main=源码，gh-pages=构建产物） |
| 本地主副本 | ~/code/blog（第二副本 ~/Projects/<username>.github.io，同一远程） |
| 部署 | hexo-deployer-git → gh-pages |

## 章节格式（novel 四件套 frontmatter，缺一不可）

```yaml
title: 第N章 章节标题
date: 实际发布日期（非故事时间线）
categories:
  - 小说
tags:
  - <作品名>
  - <主角名>
series: <作品名>
novel: <作品名>
novel_slug: <slug>
chapter: N
layout: post
permalink: novels/<slug>/NN-pinyin-slug/
toc: false
cover: false
top_img: false
aside: true
```

- `chapter` 从 0 开始（楔子=0）。
- `permalink` 里 `NN-pinyin-slug` 需与标题 slug 映射一致。
- 正文用 `{% series %}` 包裹可自动加章节导航（可选）。

## 发布流程（严格按序，不可跳步）

1. **同步检查**：`git fetch origin main` + `git status --short --branch`，确认本地=远程；落后则先 `git merge origin/main`，分叉则停下解决。双副本都要同步。
2. **生成章节**：把 novel-foundation 章节写成 `source/_posts/<作品名>/NN-第N章 标题.md`，带完整四件套 frontmatter。
3. **更新清单**：`source/_data/novel-<slug>.json`（章节 manifest）+ `source/_data/novels.yml`（小说元信息）。
4. **构建验证**：`npm run build`，确认新章节生成、无报错。
5. **部署**：`npx hexo g -d`（全量覆盖 gh-pages）。
6. **线上验证**：`curl` 新章节 URL——注意站点 404 页可能返回 200 状态码，**要看返回内容是不是 404 页**，不能只看状态码。
7. **回写 Vault**：章节同步进 Vault 对应章，更新索引 + `updated` 日期。

## 已知坑（务必遵守）

- **hexo deploy 是全量覆盖**，本地落后远程时直接部署会丢内容（双副本不同步的教训）。
- **仓库若配了 GitHub Actions 自动部署（deploy.yml：push main → hexo clean && generate → force_orphan 推 gh-pages），本地不要手动 `npx hexo deploy`**（踩坑 2026-08-22 第21章：本地 deploy 与 Actions 双写 gh-pages 竞争，本地推送被 Actions 覆盖；正确流程 = 只 `git push origin main`，等 Actions 完成，再 curl 线上验证）。
- **部署后线上 404 ≠ 部署失败**（踩坑 2026-08-22）：CF CDN 可能缓存部署完成前首次访问的 404 响应（忽略查询参数，`?v=` 也命中缓存），且 GitHub Pages 重建需 1-3 分钟。验证流程：先 `curl raw.githubusercontent.com/<repo>/gh-pages/<path>` 确认产物在 → 等 2 分钟 → 再 curl 站点 URL 看正文（不要只看状态码）。
- **新增静态资源（图片/二维码/JS/CSS）同样会被 CF 缓存 404**（踩坑 2026-08-17 打赏二维码）：首次访问新图片若赶上部署间隙，CF 会缓存该 404，之后一直 404。解法：① 资源改名（如 `xxx-qr.jpg` → 新文件名）强制新 URL；② 或 CF Dashboard purge 缓存；③ 发布流程末尾统一 `curl` 验证所有新增资源 URL 返回 200 且是正确内容（图片看 content-type/大小，不能只看状态码）。
- **双副本**（主副本 + 第二副本）必须保持同一版本。
- **date 用实际发布日期**，不是故事时间线（否则归档错乱）。
- **对白不用方言字**（易笔误），一律普通话。
- hexo 不在全局时，用 `npx hexo`。
- 删除章节后，要同时删 manifest 里对应条目，否则与实际不符。

## 与 novel-foundation 衔接

- novel-foundation 负责立项 + 章节正文（框架文件 00–06 + 未来章节）。
- 本 skill 负责发布：章节正文 → 站点。
- 章节写好后，调本 skill 走发布流程。
