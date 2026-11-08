#!/usr/bin/env python3
"""把章节 md + 每章数据（测验/卡片/术语）装配成知识库产物：
- 向 chapters/*.md 注入自测题（占位符 <!--QUIZ:chNN-->）
- 生成 quiz.md / flashcards.md / glossary.md
- 生成 manifest.json
用法: python3 build_content.py <书目录>
"""
import json
import os
import re
import sys
import glob

TYPE_LABEL = {"single": "单选", "multi": "多选", "blank": "填空"}
OPT = ["A", "B", "C", "D", "E"]


def load_data(book_dir):
    files = sorted(glob.glob(os.path.join(book_dir, "_work", "data", "ch*.json")))
    out = {}
    for f in files:
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        out[d["id"]] = d
    return out


def render_quiz_block(qs, start_idx=1):
    lines = []
    for i, q in enumerate(qs, start_idx):
        lab = TYPE_LABEL[q.get("type", "single")]
        lines.append("%d. （%s）%s" % (i, lab, q["question"]))
        opts = q.get("options") or []
        if opts:
            lines.append("   " + "  ".join("%s. %s" % (OPT[j], o) for j, o in enumerate(opts)))
        ans = q["answer"]
        if isinstance(ans, list):
            ans_txt = "、".join(OPT[a] for a in ans)
        elif isinstance(ans, int):
            ans_txt = OPT[ans]
        else:
            ans_txt = str(ans)
        lines.append("   **答案**：%s；**解析**：%s" % (ans_txt, q["explain"]))
        lines.append("")
    return "\n".join(lines)


def main(book_dir):
    book_dir = os.path.abspath(book_dir)
    data = load_data(book_dir)
    ch_files = sorted(glob.glob(os.path.join(book_dir, "chapters", "ch*.md")))

    chapters, quizzes, cards, glossary = [], [], [], []
    for f in ch_files:
        cid = re.search(r"(ch\d{2})", os.path.basename(f)).group(1)
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        m = re.search(r"^# (.*)$", text, re.M)
        title = m.group(1).strip()
        diff_m = re.search(r"\*\*难度\*\*：(\S+)", text)
        diff = diff_m.group(1).count("★") if diff_m else 1
        d = data.get(cid, {})

        def _svg(m):
            p = os.path.join(os.path.dirname(book_dir), "_build", "svg", m.group(1) + ".svg")
            return open(p, encoding="utf-8").read() if os.path.exists(p) else m.group(0)

        if "<!--SVG" in text:
            text = re.sub(r"<!--SVG:([a-z0-9_]+)-->", _svg, text)
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(text)

        if "<!--QUIZ" in text:
            block = render_quiz_block(d.get("quiz", []))
            text = re.sub(r"<!--QUIZ:.*?-->", block.rstrip(), text)
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(text)
        chapters.append({
            "id": cid,
            "title": title,
            "file": "chapters/%s" % os.path.basename(f),
            "difficulty": diff,
        })
        for q in d.get("quiz", []):
            quizzes.append(dict(q, id="q%02d" % (d.get("quiz", []).index(q) + 1), chapterId=cid))
        for c in d.get("cards", []):
            cards.append({
                "id": "f-%s-%02d" % (cid, d.get("cards", []).index(c) + 1),
                "chapterId": cid, "front": c["front"], "back": c["back"],
                "tags": c.get("tags", []),
            })
        for t in d.get("terms", []):
            glossary.append({"term": t["term"], "def": t["def"], "chapterId": cid})

    # quiz.md
    qmd = ["# 测验与答案\n", "每章的题都附答案与解析。先答再看，别顺着读。\n"]
    for ch in chapters:
        qmd.append("\n## %s（%s）\n" % (ch["title"], ch["id"]))
        qmd.append(render_quiz_block(js_list(quizzes, ch["id"])))
    comp = os.path.join(book_dir, "_work", "comprehensive.md")
    if os.path.exists(comp):
        with open(comp, encoding="utf-8") as fh:
            qmd.append("\n" + fh.read())
    with open(os.path.join(book_dir, "quiz.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(qmd))

    # flashcards.md
    fmd = ["# 抽认卡\n", "正面只给问题。先自己答，再翻背面。每天都过一遍不熟的，隔天、3 天、7 天各复习一次。\n"]
    for ch in chapters:
        fmd.append("\n## %s\n" % ch["title"])
        for c in [x for x in cards if x["chapterId"] == ch["id"]]:
            fmd.append("### %s\n- **背面**：%s\n- **标签**：%s\n- **章节**：%s\n" % (
                c["front"], c["back"], "、".join(c["tags"]), c["chapterId"]))
    with open(os.path.join(book_dir, "flashcards.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(fmd))

    # glossary.md
    gmd = ["# 术语表\n", "| 术语 | 白话定义 | 首次出现 |\n|---|---|---|"]
    for g in glossary:
        gmd.append("| %s | %s | %s |" % (g["term"], g["def"], g["chapterId"]))
    with open(os.path.join(book_dir, "glossary.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(gmd) + "\n")

    # manifest.json
    man_path = os.path.join(book_dir, "manifest.json")
    with open(man_path, encoding="utf-8") as fh:
        man = json.load(fh)
    man["chapters"] = chapters
    man["quizzes"] = quizzes
    man["flashcards"] = cards
    man["glossary"] = glossary
    with open(man_path, "w", encoding="utf-8") as fh:
        json.dump(man, fh, ensure_ascii=False, indent=2)
    print("%s: 章 %d, 题 %d, 卡 %d, 术语 %d" % (book_dir, len(chapters), len(quizzes), len(cards), len(glossary)))


def js_list(xs, cid):
    return [x for x in xs if x["chapterId"] == cid]


if __name__ == "__main__":
    main(sys.argv[1])
