# 算法机考开卷手册 / Algorithm Exam Handbook

LeetCode Hot 100 开卷手册：Python · 按官方分类 · 17 类 / 共 100 题。
单文件 HTML，A4 直接打印，机考开卷可查。

## 特点

- **单文件 `index.html`**：无外部依赖，浏览器打开即用，Ctrl+P 可直接打印成 PDF
- **按官方分类组织**：哈希 / 双指针 / 滑动窗口 / 子串 / 普通数组 / 矩阵 / 链表 / …… 共 17 类 100 题
- **输入输出模板前置**：机考每题都要用的 ACM 输入输出模板（14 条输入 + 8 条输出）单独排在最前
- **库函数速查自动生成**：附录由 AST 解析每题代码自动提取——代码里用到的库函数，附录一定有条目，不会与正文脱节
- **纯 Python 数据驱动**：题解、模板、库函数说明都是普通 `.py` 文件，改完跑一下 `build.py` 即可重新生成

## 使用

浏览器打开 [`index.html`](index.html) 即可；打印选择 A4 纵向。

或者自己生成 PDF 版：

```bash
python3 build.py           # 生成 index.html
python3 build.py --check   # 只体检，不写文件
```

## 仓库结构

```
├── build.py              # 渲染脚本：把 data/*.py 渲染成单文件 index.html
├── data/
│   ├── problems.py       # 100 题题解（按分类组织）
│   ├── acm.py            # 机考输入输出模板
│   └── libdoc.py         # 库函数速查文档
├── index.html            # 生成产物（单文件，可直接打开/打印）
└── 算法机考开卷手册.pdf   # A4 打印版
```

## License

MIT
