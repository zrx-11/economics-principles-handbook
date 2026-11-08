# 曼昆《经济学原理（第 7 版）》点化学习系统

两册（微观 22 章、宏观 14 章）扫描版 PDF 转成的可开学知识库，读者基线为理工科本科。

## 打开方式
- 双击 `index.html`：总学习手册，顶部切换两本书与跨书总览，左侧按书导航（路径/章节/概念/测验/卡片/术语/模式/速查），搜索覆盖全部书，进度本地保存。
- 单册独立使用：`01-微观经济学分册/microeconomics学习伴侣.html`、`02-宏观经济学分册/macroeconomics学习伴侣.html`，可直接发给别人。
- Markdown 版：各册 `SKILL.md`、`chapters/`、`concepts/`、`glossary.md`、`patterns.md`、`cheatsheet.md`、`quiz.md`、`flashcards.md`。

## 部署 GitHub Pages
1. 把本目录解压到仓库根目录。
2. `git add . && git commit -m "add handbook" && git push`。
3. 仓库 Settings → Pages → Source 选 `main` / `(root)`，保存后访问 `https://<用户名>.github.io/<仓库名>/`。

`.nojekyll` 已放在根目录，用来关闭 Jekyll，保证中文文件名与 `_build/`、`_work/` 目录原样托管。

## 验证
`verify_handbook.py` 端到端 24/24 通过（首页、书卡、三篇跨书总览、两册首末章、测验作答与解析、抽认卡翻转、术语过滤、全局搜索、进度持久、路径完成标记、深色模式、控制台零错误）。报告见 `_build/verify_report.json`。
