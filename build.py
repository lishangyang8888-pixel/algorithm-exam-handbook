#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 data/problems.py 渲染成单文件、A4 可直接打印的 index.html。

    python3 build.py           # 生成 index.html
    python3 build.py --check   # 只体检，不写文件

附录「库函数速查」由 ast 解析每道题的代码自动生成，
所以只要代码里用到了，附录就一定有条目，不会和正文脱节。

笔记最开头的「输入输出模板」来自 data/acm.py，那是机考每题都要用的东西，
不放附录（翻起来太靠后），单起一页排版在最前面。
"""

from __future__ import annotations

import ast
import html
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "problems.py"
LIBDOC = ROOT / "data" / "libdoc.py"
ACM = ROOT / "data" / "acm.py"
OUT = ROOT / "index.html"

MAX_CODE_COLS = 88
# 输入输出页是两栏并排，模板行必须更短，否则打印会折行
MAX_IO_COLS = 58

# 输入输出相关名字：不在附录里，单独在笔记开头成页，所以没有附录条目也正常
NO_APPX = {
    "input", "print", "stdin", "stdout", "read", "readline", "write", "buffer",
}

# 只认这些模块出的常量/属性，避免把 self.left 之类的属性误收进附录
MODULE_WHITELIST = {
    "math", "heapq", "bisect", "sys", "collections", "itertools",
    "functools", "operator", "string", "re", "copy", "random", "queue",
}

# 附录里各组的显示顺序（不在表里的组按数据文件顺序排在后面）
GROUP_ORDER = ['排序（不用 import）',
 '查找下标（str / list 不用 import）',
 '堆 heapq（import heapq）',
 '二分 bisect（import bisect）',
 '队列与计数 collections（import collections）',
 '列表 list（lst.xxx）',
 '字典 dict（d.xxx）',
 '字符串 str（s.xxx）',
 '集合 set（st.xxx）',
 '内置函数（不用 import）',
 '递归深度（import sys）',
 '数学 math（import math）',
 '运算符（不用 import）',
 '作用域（不用 import）',
 '流程控制（不用 import）',
 '随机 random（import random）']

# 这些组无论代码里有没有用到都显示
# 排序：几乎每题都可能要用，临时想不起来 key 怎么写
# 查找下标：找元素位置是高频动作，find / rfind / index 三者差别必须当场能查
ALWAYS_GROUPS = {'作用域（不用 import）',
 '流程控制（不用 import）',
 '内置函数（不用 import）',
 '列表 list（lst.xxx）',
 '字典 dict（d.xxx）',
 '字符串 str（s.xxx）',
 '排序（不用 import）',
 '数学 math（import math）',
 '查找下标（str / list 不用 import）',
 '运算符（不用 import）',
 '集合 set（st.xxx）'}

# 保留筛选接口；当前常用组整组展开，包含用户要求的相关基础方法
COMPACT_GROUPS = set()

# 组内需要置顶的条目（不写则按名字排序）。sorted / sort 是排序的主角，排在最前
ITEM_FIRST = {
    "流程控制（不用 import）": ["if", "for", "while", "continue", "break", "return", "循环 else", "pass"],
    "排序（不用 import）": ["sorted", "sort", "key"],
    "字符串 str（s.xxx）": ["split", "join"],
    "字典 dict（d.xxx）": ["d[key]", "d[key] = val", "key in d", "get"],
}

# 这些条目即使代码里没用到也显示（最基础，考场上一时想不起来一定会翻）
PIN_ITEMS = {"range", "split", "join", "bisect_left",
             "d[key]", "d[key] = val", "key in d", "get"}

CSS = r"""
* { box-sizing: border-box; }

body {
  margin: 0; background: #e9ebee; color: #15181d;
  font: 13.5px/1.7 -apple-system, "PingFang SC", "Hiragino Sans GB",
        "Microsoft YaHei", sans-serif;
  -webkit-font-smoothing: antialiased;
}
.sheet {
  max-width: 820px; margin: 0 auto; background: #fff;
  padding: 38px 46px 70px; box-shadow: 0 1px 4px rgba(0,0,0,.08);
}

/* 封面 */
header { border-bottom: 2px solid #1f4e79; padding-bottom: 11px; }
h1 { font-size: 23px; margin: 0 0 5px; }
.sub { color: #5b6069; font-size: 12px; }
.sub .dot { margin: 0 7px; color: #b8bec6; }

/* 目录 */
h2.sec {
  font-size: 11px; letter-spacing: .18em; color: #6b727c;
  margin: 26px 0 10px; font-weight: 700;
}
.toc { columns: 2; column-gap: 30px; font-size: 12.5px; }
.toc-block { break-inside: avoid; page-break-inside: avoid; margin-bottom: 10px; }
.toc-topic {
  display: block; font-weight: 600; color: #15181d; text-decoration: none;
  border-bottom: 1px solid #e4e7eb; padding-bottom: 2px; margin-bottom: 2px;
}
.toc-topic .n { color: #1f4e79; margin-right: 6px; }
.toc-topic .prog {
  float: right; font-size: 10.5px; color: #aab0b8;
  font-variant-numeric: tabular-nums; font-weight: 400;
}
.toc-problems { list-style: none; margin: 0; padding: 0 0 0 5px; }
.toc-problems li { margin: 1px 0; line-height: 1.5; }
.toc-problems a { color: #4a5058; text-decoration: none; }

/* 专题：有答案卡片的才另起一页，纯待录入清单连排，省纸 */
section.has-cards,
section#appendix,
section#acm-io { page-break-before: always; break-before: page; }
h2.topic {
  font-size: 17.5px; margin: 0 0 14px; padding: 8px 12px;
  background: #eef3f9; border-left: 4px solid #1f4e79;
  page-break-after: avoid; break-after: avoid;
}
h2.topic .n { color: #1f4e79; margin-right: 9px; }
h2.topic .prog {
  float: right; font-size: 11px; font-weight: 400; color: #8b929b;
  font-variant-numeric: tabular-nums; padding-top: 4px;
}

/* 待录入清单：一行一题，两列，紧凑 */
.pending { margin: 2px 0 22px; }
.pending-h {
  font-size: 11.5px; color: #8b929b; margin: 0 0 7px;
  letter-spacing: .04em; page-break-after: avoid; break-after: avoid;
}
.plist {
  list-style: none; margin: 0; padding: 0;
  display: grid; grid-template-columns: 1fr 1fr; column-gap: 26px;
}
.plist li {
  display: flex; gap: 9px; align-items: baseline;
  padding: 3px 0; border-bottom: 1px dotted #e7eaee;
  font-size: 12.4px; page-break-inside: avoid; break-inside: avoid;
}
.plist .no {
  flex: 0 0 42px; color: #9aa1aa; font-size: 11.6px;
  font-variant-numeric: tabular-nums; text-align: right;
}
.plist .nm { color: #333a42; }

/* 题目卡片：只有 标题 / 一句说明 / 代码 */
.problem { margin: 0 0 22px; page-break-inside: avoid; break-inside: avoid; }
.problem h3 {
  font-size: 14.5px; margin: 0 0 3px; font-weight: 600;
  border-bottom: 1px solid #e8ebef; padding-bottom: 3px;
}
.problem h3 .no { color: #1f4e79; margin-right: 7px; }
.problem h3 .src {
  font-size: 11px; font-weight: 400; color: #8b929b; margin-left: 8px;
}
.problem h3 .tag {
  font-size: 10.5px; font-weight: 400; color: #96631a; background: #fbf1de;
  border-radius: 3px; padding: 1px 6px; margin-left: 7px; letter-spacing: .02em;
}
.note { margin: 5px 0 0; color: #333a42; font-size: 12.8px; }

/* 小题示例：一行输入 → 一行输出，考场上先对样例再看代码 */
.eg {
  margin: 3px 0 0; font-size: 11.3px; color: #4a5058; line-height: 1.5;
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  page-break-after: avoid; break-after: avoid;
}
.eg-l {
  display: inline-block; margin-right: 7px; padding: 0 4px;
  font-size: 9.6px; color: #1f4e79; background: #eaf1f8; border-radius: 3px;
  vertical-align: 1px;
}

/* 题旁批注：同一件事的两种写法、可替换的库函数 */
.tip {
  margin: 6px 0 0; padding: 5px 9px; background: #fbf8f1;
  border-left: 2px solid #d9c08a; border-radius: 0 3px 3px 0;
  font-size: 11.4px; color: #5b5342; line-height: 1.55;
}
.tip-l {
  display: inline-block; margin-right: 7px; padding: 0 4px;
  font-size: 9.6px; color: #8a6a2f; background: #f3e8cf; border-radius: 3px;
  vertical-align: 1px;
}
.tip code {
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  font-size: 10.8px; color: #6b5320; background: #f6efdf;
  padding: 0 3px; border-radius: 2px;
}

.alt-h {
  margin: 13px 0 0; font-size: 11.5px; color: #6b727c;
  letter-spacing: .02em; page-break-after: avoid; break-after: avoid;
}

/* 专题小结：专题收尾时一段话串起每题思路，末尾点出这一类的核心思想 */
.summary {
  margin: 6px 0 20px; padding: 10px 14px 11px;
  background: #f1f5fa; border: 1px solid #dbe5ef; border-left: 3px solid #1f4e79;
  border-radius: 0 4px 4px 0;
  page-break-inside: avoid; break-inside: avoid;
}
.summary p.summary-h {
  margin: 0 0 5px; font-size: 10.3px; font-weight: 700;
  letter-spacing: .16em; color: #6b727c;
}
.summary p { margin: 0; font-size: 12.2px; color: #2c333b; line-height: 1.66; }
.summary p + p { margin-top: 7px; }
.summary p.sum-core { padding-top: 7px; border-top: 1px dotted #cdd8e4; }
.summary p.sum-core::before {
  content: "核心"; display: inline-block; margin-right: 7px;
  font-size: 9.6px; color: #1f4e79; background: #e2ecf6;
  border-radius: 3px; padding: 0 5px; vertical-align: 1px;
}
.summary code {
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  font-size: 10.9px; color: #1b5c85; background: #e6eef6;
  padding: 0 3px; border-radius: 2px;
}

pre.code {
  margin: 7px 0 0; padding: 9px 12px;
  background: #f5f6f8; border-left: 3px solid #1f4e79; border-radius: 0 4px 4px 0;
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  font-size: 11.4px; line-height: 1.55;
  white-space: pre; overflow-x: auto;
  page-break-inside: avoid; break-inside: avoid;
}
pre.code code { font: inherit; }

/* 输入输出模板（笔记最开头） */
.io-skel-note { margin: 0 0 7px; color: #6b727c; font-size: 11.8px; }
.io-h {
  font-size: 13.5px; margin: 20px 0 3px; color: #1f4e79; font-weight: 700;
  border-bottom: 1px solid #dfe3e9; padding-bottom: 3px;
  page-break-after: avoid; break-after: avoid;
}
.io-h .imp { float: right; font-size: 10.5px; font-weight: 400; color: #9aa1aa; }
.io-note {
  margin: 0 0 9px; font-size: 10.9px; color: #7a818a; line-height: 1.55;
  page-break-after: avoid; break-after: avoid;
}
.io-case {
  margin: 0 0 11px; padding: 0 0 9px; border-bottom: 1px dotted #e7eaee;
  page-break-inside: avoid; break-inside: avoid;
}
.io-t {
  font-size: 12.2px; font-weight: 600; color: #333a42; margin: 0 0 4px;
  page-break-after: avoid; break-after: avoid;
}
.io-t .n {
  display: inline-block; width: 17px; color: #1f4e79;
  font-variant-numeric: tabular-nums;
}
/* 每条模板的 import 标注 */
.io-imp {
  float: right; font-size: 9.6px; font-weight: 400; letter-spacing: .02em;
  color: #5d646e; background: #eef0f3; border-radius: 3px;
  padding: 0 6px; line-height: 1.6;
}
.io-imp.need { color: #92500a; background: #fcefdc; }
.io-body { display: grid; grid-template-columns: 33% 1fr; gap: 12px; align-items: start; }
.io-sample {
  margin: 0; padding: 6px 9px; background: #f7f8fa; border-radius: 3px;
  border-left: 2px solid #c9d2dc;
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  font-size: 10.6px; line-height: 1.5; color: #333a42;
  white-space: pre-wrap; word-break: break-all;
}
.io-sample b {
  display: block; font-size: 9.2px; font-weight: 400; color: #9aa1aa;
  letter-spacing: .08em; margin-bottom: 3px;
}
.io-case pre.code { margin: 0; }
.io-n {
  margin: 4px 0 0; font-size: 10.7px; color: #6b727c; line-height: 1.55;
}
.io-res {
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  color: #1f4e79; background: #eef3f9; border-radius: 2px;
  padding: 0 5px; margin-right: 4px;
}
.io-res::before { content: "→ "; color: #7ba0bd; }
.io-res.alt::before { content: "给定 "; }
.io-tip::before { content: "｜"; color: #c9ced6; margin-right: 5px; }

/* 附录 */
.apx-note { margin: 0 0 14px; color: #6b727c; font-size: 11.8px; }
.lib-group { margin: 0 0 15px; }
.lib-gt {
  font-size: 12px; margin: 0 0 4px; color: #1f4e79; font-weight: 700;
  letter-spacing: .05em; border-bottom: 1px solid #dfe3e9; padding-bottom: 3px;
  page-break-after: avoid; break-after: avoid;
}
.lib-gt .imp { color: #9aa1aa; font-weight: 400; font-size: 10.8px; letter-spacing: 0; }
.lib-gn {
  margin: 0 0 5px; font-size: 10.8px; color: #7a818a; line-height: 1.5;
  padding-left: 1px; page-break-after: avoid; break-after: avoid;
}
.lib {
  display: flex; align-items: baseline; gap: 12px;
  padding: 3px 0; border-bottom: 1px dotted #e7eaee;
  page-break-inside: avoid; break-inside: avoid;
}
.lib .sig {
  flex: 0 0 auto; font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: 11.4px; color: #15181d; white-space: nowrap;
}
.lib .sig b { color: #1f4e79; font-weight: 600; }
/* 行为徽章：原地改 / 返回新对象 / 其他 */
.kind {
  display: inline-block; font-size: 9.3px; font-weight: 400;
  padding: 0 4px; border-radius: 3px;
  vertical-align: 1px; letter-spacing: .02em; white-space: nowrap;
}
.lib .kind { flex: 0 0 auto; }              /* 单行条目：徽章排在最右，成一列 */
.lib.long .kind { margin-left: 7px; }       /* 长条目：跟在语法后面 */
.kind.inplace { color: #92500a; background: #fcefdc; }
.kind.ret { color: #1b5c85; background: #e8f1f8; }
.kind.misc { color: #5d646e; background: #eef0f3; }
.lib .d {
  flex: 1 1 auto; text-align: right; color: #6b727c; font-size: 11px;
  line-height: 1.45;
}
/* 多条说明：语法独占一行，说明在下面左对齐逐行展开 */
.lib.long { display: block; padding: 5px 0 7px; }
.lib.long .sig {
  display: block; white-space: normal; margin-bottom: 3px; color: #1f4e79;
}
.lib.long .sig b { color: #1f4e79; }
.lib.long .d { display: block; text-align: left; color: #4a5058; line-height: 1.5; }
.lib.long .ex {
  display: inline-block; font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: 10.6px; color: #1f4e79; background: #f4f6f9;
  padding: 0 5px; border-radius: 2px; margin: 1px 0;
}
/* 带准备步骤的示例分开显示程序与结果。 */
.lib.long .ex-case {
  display: block; margin: 5px 0 7px; border: 1px solid #dce5ee;
  border-radius: 5px; overflow: hidden; break-inside: avoid;
}
.lib.long .ex-case + br { display: none; }
.lib.long .ex-program { display: block; padding: 6px 10px 7px; background: #f4f7fa; }
.lib.long .ex-label { font-size: 10px; font-weight: 600; color: #536b82; }
.lib.long .ex-program .ex-label { display: block; margin-bottom: 3px; }
.lib.long .ex-case code {
  font-size: 10.6px; line-height: 1.45; padding: 0; background: transparent;
  overflow-wrap: anywhere;
}
.lib.long .ex-source { display: block; white-space: pre-wrap; tab-size: 4; }
.lib.long .ex-evaluation {
  display: flex; flex-wrap: wrap; align-items: baseline; gap: 3px 8px;
  padding: 5px 10px; border-top: 1px solid #dce5ee; background: #fff;
}
.lib.long .ex-expression { white-space: pre-wrap; }
.lib.long .ex-arrow { color: #657d93; }
.lib.long .ex-case .ex-value { color: #216052; font-weight: 600; white-space: pre-wrap; }

/* 说明文字里用反引号标出来的代码 */
.lib .d code, .lib-gn code {
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: 10.4px; color: #1b5c85; background: #eef2f7;
  padding: 0 3px; border-radius: 2px;
}

/* 打印 */
@page { size: A4; margin: 13mm 12mm; }

@media print {
  body { background: #fff; font-size: 10.2pt; line-height: 1.58;
         -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .sheet { max-width: none; margin: 0; padding: 0; box-shadow: none; }
  a { color: inherit; text-decoration: none; }
  h1 { font-size: 19pt; }
  h2.topic { font-size: 13.5pt; }
  .problem h3 { font-size: 11pt; }
  .note { font-size: 9.8pt; }
  .summary p { font-size: 9.7pt; line-height: 1.6; }
  .summary code { font-size: 8.8pt; }
  pre.code { font-size: 8.5pt; line-height: 1.48; background: #f5f6f8 !important; }
  .toc { font-size: 9.6pt; }
  .plist li { font-size: 9.4pt; }
  .plist .no { font-size: 8.8pt; }
  .lib { font-size: 9.6pt; }
  .lib .sig { font-size: 8.8pt; }
  .lib .d { font-size: 8.6pt; }
}
"""


def esc(value: object) -> str:
    return html.escape(str(value), quote=False)


def esc_code(text: str) -> str:
    """行内反引号包起来的部分渲染成等宽代码，其余照常转义。"""
    parts = esc(text).split("`")
    return "".join(f'<code>{p}</code>' if i % 2 else p for i, p in enumerate(parts))


def load_module(path: Path, ns_name: str) -> dict:
    if not path.exists():
        raise SystemExit(f"找不到文件：{path}")
    ns: dict = {"__file__": str(path), "__name__": ns_name}
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), ns)
    return ns


def collect_calls(code: str, docs: dict) -> set[str]:
    """拿到这段代码用到的库函数/方法名（调用、模块常量、from-import 三条路），
    去掉自己定义的函数和类。"""
    tree = ast.parse(code)
    defined = {
        n.name for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }
    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name):
                used.add(f.id)
            elif isinstance(f, ast.Attribute):
                used.add(f.attr)
        elif isinstance(node, ast.Attribute):
            # math.inf、sys.maxsize 这类不带括号的
            recv = node.value
            if isinstance(recv, ast.Name) and recv.id in MODULE_WHITELIST and node.attr in docs:
                used.add(node.attr)
        elif isinstance(node, ast.ImportFrom):
            # from heapq import heapify
            for alias in node.names:
                name = alias.asname or alias.name
                if name in docs:
                    used.add(name)
    return used - defined


def visible_topics(topics: list[dict]) -> list[dict]:
    return [t for t in topics if t.get("problems") or t.get("pending")]


def pending_rows(topic: dict) -> list[tuple[int, str]]:
    """还没录入答案的题。已经在 problems 里出现过的题号自动跳过。"""
    done = set()
    for p in topic.get("problems") or []:
        m = re.search(r"\d+", str(p.get("source", "")))
        if m:
            done.add(int(m.group()))
    return [(no, name) for no, name in topic.get("pending") or [] if no not in done]


def hot_done(topic: dict) -> int:
    """本类已录入的 Hot 100 题数。带 tag 的附加题（如 LC 704）不计入进度。"""
    return len([p for p in topic.get("problems") or [] if not p.get("tag")])


def render_toc(topics: list[dict], acm: dict | None = None) -> str:
    buf = ['<nav class="toc">']
    if acm:
        buf.append('<div class="toc-block">'
                   '<a class="toc-topic" href="#acm-io">'
                   '<span class="n">0</span>输入输出模板</a>'
                   '<ol class="toc-problems">')
        for sec in acm.get("SECTIONS", []):
            anchor = esc(sec["id"])
            buf.append(f'<li><a href="#{anchor}">{esc(sec["name"])}模板'
                       f'（{len(sec["cases"])} 条）</a></li>')
        buf.append('</ol></div>')
    for ti, topic in enumerate(topics, 1):
        probs = topic.get("problems") or []
        done = hot_done(topic)
        left = len(pending_rows(topic))
        total = done + left
        buf.append('<div class="toc-block">')
        prog = f'<span class="prog">{done}/{total}</span>' if total else ''
        buf.append(
            f'<a class="toc-topic" href="#{esc(topic["id"])}">'
            f'<span class="n">{ti}</span>{esc(topic["name"])}{prog}</a>'
        )
        if probs:
            buf.append('<ol class="toc-problems">')
            for pi, p in enumerate(probs, 1):
                buf.append(f'<li><a href="#p-{esc(topic["id"])}-{pi}">'
                           f'{ti}.{pi} {esc(p["title"])}</a></li>')
            buf.append('</ol>')
        buf.append('</div>')
    buf.append('</nav>')
    return "".join(buf)


def problem_code_entries(p: dict) -> list[tuple[str, str]]:
    """主解、原有补充写法和备注代码统一参与检查与附录函数收集。"""
    entries = [(name, p[name]) for name in ("code", "alt_code") if p.get(name)]
    entries.extend((f'备注 {i}', note["code"])
                   for i, note in enumerate(p.get("remarks", []), 1) if note.get("code"))
    return entries


def render_problem(ti: int, pi: int, topic_id: str, p: dict) -> str:
    buf = [f'<article class="problem" id="p-{esc(topic_id)}-{pi}">']
    head = f'<h3><span class="no">{ti}.{pi}</span>{esc(p["title"])}'
    if p.get("source"):
        head += f'<span class="src">{esc(p["source"])}</span>'
    if p.get("tag"):
        head += f'<span class="tag">{esc(p["tag"])}</span>'
    buf.append(head + '</h3>')
    if p.get("note"):
        buf.append(f'<p class="note">{esc(p["note"])}</p>')
    if p.get("example"):
        buf.append(f'<p class="eg"><span class="eg-l">例</span>{esc(p["example"])}</p>')
    if p.get("code"):
        code = p["code"].strip("\n")
        buf.append(f'<pre class="code"><code>{esc(code)}</code></pre>')
    if p.get("tips"):
        body = "<br>".join(esc_code(t) for t in p["tips"])
        buf.append(f'<p class="tip"><span class="tip-l">注</span>{body}</p>')
    if p.get("alt_code"):
        if p.get("alt_title"):
            buf.append(f'<p class="alt-h">{esc(p["alt_title"])}</p>')
        buf.append(f'<pre class="code"><code>{esc(p["alt_code"].strip(chr(10)))}</code></pre>')
    for remark in p.get("remarks", []):
        buf.append(f'<p class="alt-h">{esc(remark["title"])}</p>')
        if remark.get("note"):
            buf.append('<p class="tip"><span class="tip-l">注</span>'
                       + esc_code(remark["note"]) + '</p>')
        if remark.get("code"):
            buf.append(f'<pre class="code"><code>{esc(remark["code"].strip(chr(10)))}</code></pre>')
    buf.append('</article>')
    return "".join(buf)


def render_summary(topic: dict) -> str:
    """专题收尾的一段话。summary 可写一条字符串，也可写多条（最后一条自动
    标「核心」），支持的 `反引号` 会渲染成等宽代码。"""
    lines = topic.get("summary")
    if not lines:
        return ""
    if isinstance(lines, str):
        lines = [lines]
    buf = ['<aside class="summary">', '<p class="summary-h">专题小结</p>']
    last = len(lines) - 1
    for i, line in enumerate(lines):
        cls = ' class="sum-core"' if last and i == last else ''
        body = esc_code(line).replace("\n", "<br>")   # 一题一行，扫读快
        buf.append(f'<p{cls}>{body}</p>')
    buf.append('</aside>')
    return "".join(buf)


def render_topic(ti: int, topic: dict) -> str:
    probs = topic.get("problems") or []
    left = pending_rows(topic)
    cls = "topic-sec has-cards" if probs else "topic-sec"
    buf = [f'<section class="{cls}" id="{esc(topic["id"])}">']
    head = f'<h2 class="topic"><span class="n">{ti}</span>{esc(topic["name"])}'
    total = hot_done(topic) + len(left)
    if total:
        head += f'<span class="prog">{hot_done(topic)}/{total}</span>'
    buf.append(head + '</h2>')
    for pi, p in enumerate(probs, 1):
        buf.append(render_problem(ti, pi, topic["id"], p))
    buf.append(render_summary(topic))
    if left:
        buf.append('<div class="pending">')
        buf.append(f'<p class="pending-h">待录入 · 共 {len(left)} 题</p>')
        buf.append('<ul class="plist">')
        for no, name in left:
            buf.append(f'<li><span class="no">{no}</span>'
                       f'<span class="nm">{esc(name)}</span></li>')
        buf.append('</ul>')
        buf.append('</div>')
    buf.append('</section>')
    return "".join(buf)


def render_acm(acm: dict) -> str:
    """笔记最开头那一页：输入模板 + 输出模板，每条自己标 import。"""
    if not acm:
        return ""
    buf = ['<section id="acm-io">',
           '<h2 class="topic"><span class="n">0</span>ACM 输入输出模板</h2>',
           '<p class="io-skel-note">左边是样例，右边是对应代码；下方给出变量结果或输出所需的变量。'
           '每张卡片的其他格式单独标 import、样例和结果，按题面替换，不与主代码一起执行。'
           '函数判题提交指定类/函数；ACM 模式自行读取、调用算法并输出。'
           '示例 solve() 需按题意实现并返回答案，不能只定义 class Solution 而不调用。</p>']
    for sec in acm.get("SECTIONS", []):
        variant_count = sum(len(c.get("variants", [])) for c in sec["cases"])
        buf.append(f'<h3 class="io-h" id="{esc(sec["id"])}">{esc(sec["name"])}模板'
                   f'<span class="imp">{len(sec["cases"])} 张卡片，另有 {variant_count} 个变体</span></h3>')
        if sec.get("note"):
            buf.append(f'<p class="io-note">{esc(sec["note"])}</p>')
        marks = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
        for ci, case in enumerate(sec["cases"]):
            mark = marks[ci] if ci < len(marks) else f'{ci + 1}'
            imp = case.get("imp")
            badge = (f'<span class="io-imp need">{esc(imp)}</span>' if imp
                     else '<span class="io-imp">不用 import</span>')
            buf.append('<div class="io-case">')
            buf.append(f'<p class="io-t"><span class="n">{mark}</span>'
                       f'{esc(case["title"])}{badge}</p>')
            buf.append('<div class="io-body">')
            sample = case.get("sample", "")
            lines = sample.count("\n") + 1
            label = case.get("kind") or sec.get("kind", "样例")
            buf.append(f'<pre class="io-sample"><b>{esc(label)} · {lines} 行</b>'
                       f'{esc(sample)}</pre>')
            code = case["code"].strip("\n")
            buf.append(f'<pre class="code"><code>{esc(code)}</code></pre>')
            buf.append('</div>')
            tail = ""
            if case.get("result"):
                # 输入：跑完得到什么用「→」；输出：这段代码给定什么数据用「给定」
                cls = "io-res alt" if sec["id"].endswith("out") else "io-res"
                tail += f'<span class="{cls}">{esc(case["result"])}</span>'
            if case.get("note"):
                tail += f'<span class="io-tip">{esc(case["note"])}</span>'
            if tail:
                buf.append(f'<p class="io-n">{tail}</p>')
            for alt in case.get("variants", []):
                imp = alt.get("imp")
                badge = (f'<span class="io-imp need">{esc(imp)}</span>' if imp
                         else '<span class="io-imp">不用 import</span>')
                buf.append(f'<p class="io-t">其他格式 · {esc(alt["title"])}{badge}</p>')
                sample = alt["sample"]
                lines = sample.count("\n") + 1
                buf.append('<div class="io-body">')
                buf.append(f'<pre class="io-sample"><b>{esc(label)} · {lines} 行</b>'
                           f'{esc(sample)}</pre>')
                buf.append(f'<pre class="code"><code>{esc(alt["code"].strip(chr(10)))}</code></pre>')
                buf.append('</div>')
                cls = "io-res alt" if sec["id"].endswith("out") else "io-res"
                buf.append(f'<p class="io-n"><span class="{cls}">{esc(alt["result"])}</span>'
                           f'<span class="io-tip">{esc(alt["note"])}</span></p>')
            buf.append('</div>')
    buf.append('</section>')
    return "".join(buf)



def kind_class(kind: str) -> str:
    if kind.startswith("原地"):
        return "inplace"
    if kind == "返回":
        return "ret"
    return "misc"


def render_appendix_example(example: str) -> str:
    """将准备语句与最后用于查看结果的表达式分开。"""
    code, arrow, expected = example.rpartition(" -> ")
    if arrow:
        try:
            statements = ast.parse(code).body
        except SyntaxError:
            statements = []
        if len(statements) > 1 and isinstance(statements[-1], ast.Expr):
            program = "\n".join(ast.get_source_segment(code, stmt) for stmt in statements[:-1])
            expression = ast.get_source_segment(code, statements[-1])
            return (
                '<span class="ex-case">'
                '<span class="ex-program"><span class="ex-label">程序</span>'
                f'<code class="ex-source">{esc(program)}</code></span>'
                '<span class="ex-evaluation"><span class="ex-label">查看结果</span>'
                f'<code class="ex-expression">{esc(expression)}</code>'
                '<span class="ex-arrow">→</span>'
                f'<code class="ex-value">{esc(expected)}</code></span></span>'
            )
    style = ' style="white-space:pre-wrap"' if "\n" in example else ''
    return f'<span class="ex"{style}>{esc(example)}</span>'


def render_appendix(used: set[str], groups: list, kinds: dict) -> str:
    """按既有分组展示；常用组及正文用到的模块整组展开。"""
    rank = {name: i for i, name in enumerate(GROUP_ORDER)}
    ordered = sorted(groups, key=lambda g: rank.get(g[0], len(rank)))

    buf = ['<section id="appendix">',
           '<h2 class="topic"><span class="n">A</span>库函数速查</h2>',
           '<p class="apx-note">按模块分组，组名后面标了要 import 什么。'
           '语法末尾的小徽章是行为标记：<b>原地</b>＝修改原对象，返回 None；'
           '<b>返回</b>＝取得结果或迭代器；取用迭代器会推进位置；<b>原地+返回</b>＝可能修改原对象，同时给出结果。'
           '赋值、作用域、流程控制、规则徽章表示语法用途，不是函数返回值。'
           '示例结果若是异常名称，表示运行该表达式会抛出该异常。'
           '先按组内提示导入。带准备步骤的例子先运行「程序」，再求值「查看结果」中的表达式。箭头右侧是预期结果。'
           '输入输出在第 0 专题。'
           '常用组含相关基础方法；其余模块随正文需要显示。</p>']
    for title, note, items in ordered:
        has_pin = any(n in items for n in PIN_ITEMS)
        if title not in ALWAYS_GROUPS and not has_pin and not any(n in items for n in used):
            continue
        names = sorted(items, key=str.lower)
        first = ITEM_FIRST.get(title, [])       # 需要置顶的条目放最前，其余按名字排
        if first:
            names = sorted(names, key=lambda n: (first.index(n) if n in first else len(first),
                                                 n.lower()))
        if title in COMPACT_GROUPS:
            names = [n for n in names if n in used or n in PIN_ITEMS]
        buf.append('<div class="lib-group">')
        if "（" in title:                      # 括号里的 import 提示压灰，弱化
            head, tail = title.split("（", 1)
            buf.append(f'<h3 class="lib-gt">{esc(head)}<span class="imp">（{esc(tail)}</span></h3>')
        else:
            buf.append(f'<h3 class="lib-gt">{esc(title)}</h3>')
        if note:
            buf.append('<p class="lib-gn">'
                       + "<br>".join(esc_code(part) for part in note.split("\n")) + '</p>')
        for name in names:
            syntax, desc = items[name]
            sig = esc(syntax)
            display_name = name.rsplit(".", 1)[-1]
            pos = sig.find(display_name)
            if pos != -1:                      # 把函数名本身加粗，方便扫读
                sig = f'{sig[:pos]}<b>{esc(display_name)}</b>{sig[pos + len(display_name):]}'
            kind = kinds.get(name, "返回")      # 原地改 / 返回新对象
            badge = f'<span class="kind {kind_class(kind)}">{esc(kind)}</span>'
            # 说明里行首写 "| " 的行按等宽字体渲染，用来放小例子
            parts = []
            example_lines = []
            def flush_example():
                if not example_lines:
                    return
                parts.append(render_appendix_example("\n".join(example_lines)))
                example_lines.clear()
            for line in desc.split("\n"):
                if line.startswith("| "):
                    example_lines.append(line[2:])
                    if " -> " in line:
                        flush_example()
                else:
                    flush_example()
                    parts.append(esc_code(line))
            flush_example()
            body = "<br>".join(parts)
            if "\n" in desc:
                # 多条说明：块级排版，徽章跟在语法行末尾
                buf.append(f'<div class="lib long"><span class="sig">{sig}{badge}</span>'
                           f'<span class="d">{body}</span></div>')
            else:
                # 单行说明：徽章放到行末，整组徽章成一列，右边界对齐
                buf.append(f'<div class="lib"><span class="sig">{sig}</span>'
                           f'<span class="d">{body}</span>{badge}</div>')
        buf.append('</div>')
    buf.append('</section>')
    return "".join(buf)


def render_page(meta: dict, topics: list[dict], used: set[str], groups: list,
                kinds: dict, acm: dict) -> str:
    title = meta.get("title", "算法机考开卷手册")
    subtitle = meta.get("subtitle", "")
    done = sum(hot_done(t) for t in topics)
    left = sum(len(pending_rows(t)) for t in topics)
    meta_line = (f'<div class="sub">{esc(subtitle)}<span class="dot">·</span>'
                 f'{len(topics)} 类 / 共 {done + left} 题，已录入 {done}'
                 f'<span class="dot">·</span>{date.today().isoformat()}</div>')

    body = [
        f'<header><h1>{esc(title)}</h1>{meta_line}</header>',
        '<h2 class="sec">目录</h2>',
        render_toc(topics, acm) if topics else '<p class="sub">还没有题目。</p>',
        render_acm(acm),
    ]
    body.extend(render_topic(ti, t) for ti, t in enumerate(topics, 1))
    body.append(render_appendix(used, groups, kinds))

    return (
        '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>{esc(title)}</title>\n<style>{CSS}</style>\n</head>\n'
        '<body>\n<div class="sheet">\n' + "\n".join(body) + '\n</div>\n</body>\n</html>\n'
    )


def check(topics: list[dict], docs: dict) -> tuple[list[str], set[str]]:
    warns: list[str] = []
    used: set[str] = set()
    titles: list[str] = []
    ids: list[str] = []
    pend_nos: list[int] = []

    for topic in topics:
        ids.append(topic.get("id", ""))
        for no, name in pending_rows(topic):
            if no in pend_nos:
                warns.append(f'待录入题号重复：LC {no}（{name}）')
            pend_nos.append(no)
        for p in topic.get("problems") or []:
            t = p.get("title", "")
            titles.append(t)
            if not t:
                warns.append(f'专题 {topic.get("id")} 有题目缺 title')
            if not p.get("note"):
                warns.append(f'{t}: 缺一句说明')
            if not p.get("example"):
                warns.append(f'{t}: 缺小题示例')
            if not p.get("code"):
                warns.append(f'{t}: 没有代码')
                continue
            for field, body in problem_code_entries(p):
                if not body:
                    continue
                try:
                    used |= collect_calls(body, docs)
                except SyntaxError as e:
                    warns.append(f'{t}（{field}）: 代码语法错误 — {e}')
                    continue
                for no, line in enumerate(body.splitlines(), 1):
                    if len(line) > MAX_CODE_COLS:
                        warns.append(
                            f'{t}（{field}）: 第 {no} 行 {len(line)} 列，打印会截断'
                        )

    for dup in sorted({x for x in ids if ids.count(x) > 1}):
        warns.append(f'专题 id 重复：{dup}（锚点会跳错）')
    for dup in sorted({x for x in titles if titles.count(x) > 1}):
        warns.append(f'题名重复：{dup}（搜索时会混）')

    return warns, used


def check_acm(acm: dict) -> list[str]:
    """检查每张卡片及卡片内的其他格式，避免漏验备选代码。"""
    warns: list[str] = []
    for sec in acm.get("SECTIONS", []):
        for case in sec.get("cases", []):
            for entry in [case, *case.get("variants", [])]:
                title = f'IO {sec["name"]}·{entry["title"]}'
                try:
                    ast.parse(entry["code"])
                except SyntaxError as e:
                    warns.append(f'{title}：语法错误 — {e}')
                for no, line in enumerate(entry["code"].splitlines(), 1):
                    if len(line) > MAX_IO_COLS:
                        warns.append(f'{title} 第 {no} 行 {len(line)} 列，'
                                     f'超出 {MAX_IO_COLS} 会折行')
                for field, label in [("sample", "样例"), ("result", "得到什么")]:
                    if not entry.get(field):
                        warns.append(f'{title}：缺{label}')
    return warns


def report_libs(topics: list[dict], docs: dict) -> None:
    """逐题列出代码里用到的库函数，并标出附录词典里还没有的。
    每录一题跑一次 python3 build.py --libs，确认没有「⚠ 缺」。"""
    for topic in topics:
        for p in topic.get("problems") or []:
            bodies = [body for _, body in problem_code_entries(p)]
            used: set[str] = set()
            for b in bodies:
                try:
                    used |= collect_calls(b, docs)
                except SyntaxError as e:
                    print(f'{p.get("source", "")}: 语法错误 — {e}')
            miss = sorted(n for n in used if n not in docs and n not in NO_APPX)
            mark = f'  ⚠ 缺词典：{"、".join(miss)}' if miss else ''
            print(f'{str(p.get("source", "")):8s} {str(p.get("title", ""))[:14]:16s}'
                  f'{" ".join(sorted(used))}{mark}')


def main() -> int:
    data = load_module(DATA, "problems_data")
    lib = load_module(LIBDOC, "libdoc_data")
    acm = load_module(ACM, "acm_data") if ACM.exists() else {}
    groups = lib.get("GROUPS", [])
    docs = {name: v for _, _, items in groups for name, v in items.items()}

    topics = visible_topics(data.get("TOPICS", []))
    warns, used = check(data.get("TOPICS", []), docs)
    warns += check_acm(acm)

    missing = sorted(n for n in used if n not in docs and n not in NO_APPX)
    if missing:
        print(f'附录缺条目（请补 data/libdoc.py）：{"、".join(missing)}')

    if "--libs" in sys.argv:
        report_libs(data.get("TOPICS", []), docs)
        return 0

    if warns:
        print(f'体检 {len(warns)} 处：')
        for w in warns:
            print('  -', w)
    else:
        print('体检通过。')

    if "--check" in sys.argv:
        return 1 if warns else 0

    OUT.write_text(render_page(data.get("META", {}), topics, used, groups,
                               lib.get("KINDS", {}), acm), encoding="utf-8")

    done = sum(hot_done(t) for t in topics)
    left = sum(len(pending_rows(t)) for t in topics)
    shown = [g for g in groups
             if g[0] in ALWAYS_GROUPS or any(n in g[2] for n in PIN_ITEMS)
             or any(n in g[2] for n in used)]
    n_items = sum(
        len([n for n in g[2] if n in used or n in PIN_ITEMS]) if g[0] in COMPACT_GROUPS
        else len(g[2])
        for g in shown
    )
    print(f'已生成 index.html：{len(topics)} 类 / 已录入 {done} 题 / 待录入 {left} 题 / '
          f'IO 模板 {sum(len(s["cases"]) for s in acm.get("SECTIONS", []))} 条 / '
          f'附录 {len(shown)} 组 {n_items} 条')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
