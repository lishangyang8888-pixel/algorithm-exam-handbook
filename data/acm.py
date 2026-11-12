# -*- coding: utf-8 -*-
"""
笔记最开头的「ACM 输入输出」页。

原来是附录里的一个分组，用户 2026-11-06 要求单独拎出来放最前面，
因为机考每道题都要自己读 stdin、写 stdout，翻附录太靠后。
同一天又删掉通用骨架，改成每条模板自己标注要不要 import。

结构：
    SECTIONS  输入 / 输出 两大类，每类下面若干 case
每个 case：
    title    场景名，一句话
    imp      要 import 什么；None 表示全是内置，什么都不用写
    sample   真实的 stdin / stdout 长相，用于对照题目样例
    code     模板，行宽控制在 58 列以内（两栏排版，超了会折行）
    result   这段代码跑完得到什么（输入给变量值，输出给对应的数据）
    note     一句话说明坑在哪，没有就不写
"""

SECTIONS: list[dict] = [{'id': 'acm-in',
  'name': '输入',
  'kind': '输入样例',
  'note': '先看题面按行还是按 token 分隔。整行字符串保留空白；数字、单词可按 token '
          '取。空数组是否占行按题面，不能统一多读或少读一行。卡片内的其他格式按题面选用，不与主代码同时执行。',
  'cases': [{'title': '一行两个整数',
             'imp': None,
             'sample': '3 5',
             'code': 'a, b = map(int, input().split())',
             'result': 'a = 3，b = 5',
             'note': 'split() 不带参数，按任意空白切，多个空格、Tab 都能吃。'},
            {'title': '先给 n，下一行给 n 个数',
             'imp': None,
             'sample': '5\n1 2 3 4 5',
             'code': 'n = int(input())\nnums = list(map(int, input().split()))',
             'result': 'n = 5，nums = [1, 2, 3, 4, 5]',
             'note': '下一行恰好 n 个数时用主代码。n = 0 时，只有题面仍给一空行才读该行；若省略数组行，或字段任意折行，用③。',
             'variants': [{'title': 'n 和数组在同一行',
                           'sample': '3 1 2 3',
                           'code': 'n, *nums = map(int, input().split())',
                           'result': 'n = 3，nums = [1, 2, 3]',
                           'note': '这一行必须恰有 n + 1 个整数；输入只有 0 时得到空数组，不能把后续字段也放进这一行。',
                           'imp': None},
                          {'title': '完整 ACM 示例：读入、调用函数、输出',
                           'imp': None,
                           'sample': '3\n4 -1 2',
                           'code': 'def solve(nums):\n'
                                   '    return sum(nums)\n'
                                   '\n'
                                   'n = int(input())\n'
                                   'nums = list(map(int, input().split()))\n'
                                   'print(solve(nums))',
                           'result': '标准输出为 5，末尾换行。',
                           'note': '本例规定第二行恰有 n 个整数。套用手册里的类方法时，先复制题解，再把 solve(nums) 换成 '
                                   'Solution().方法名(nums)，参数和输出格式按题面调整。'}]},
            {'title': '按个数读 n 个数（允许折行）',
             'imp': 'import sys',
             'sample': '5\n1 2 3\n4 5',
             'code': 'data = (x for line in sys.stdin for x in line.split())\n'
                     'n = int(next(data))\n'
                     'nums = [int(next(data)) for _ in range(n)]',
             'result': 'n = 5，nums = [1, 2, 3, 4, 5]',
             'note': ('逐行生成 token，不一次读完。n 可独占一行，也可与数组同一行；n = 0 不取数组元素。后续字段继续 next(data)，例如再读一个整数可写 k = '
                      'int(next(data))。不要混用 input()；空白有意义的字符串不能这样读。')},
            {'title': 'n 行，每行一个',
             'imp': None,
             'sample': '3\n10\n20\n30',
             'code': 'n = int(input())\nnums = [int(input()) for _ in range(n)]',
             'result': 'n = 3，nums = [10, 20, 30]',
             'note': '整数也能用 read().split() 一次读取。若每行是字符串，把 int(input()) 整体换成 '
                     'input()；只有题面允许忽略首尾空白时才加 .strip()。'},
            {'title': '逗号整数 / JSON 数组',
             'imp': None,
             'sample': '1,2,3',
             'code': 's = input().strip()\n'
                     "nums = list(map(int, s.split(','))) if s else []",
             'result': 'nums = [1, 2, 3]',
             'note': '主代码约定空行表示空数组；否则输入为无括号、无空字段的逗号整数。int() 接受两侧空格。1,,2 '
                     '或末尾逗号仍会报错，不擅自删空项。带括号看下面的 JSON 写法。',
             'variants': [{'title': '带括号的 JSON 数组',
                           'sample': '[1, true, null, "中"]',
                           'code': 'nums = json.loads(input())',
                           'result': "nums = [1, True, None, '中']",
                           'note': ('按标准 JSON 写：字符串用双引号，布尔值和空值写 true / false / null；单引号、True、None、nums = '
                                    '[...] 都不是此格式。多行单一 JSON 文档可用 json.load(sys.stdin)，需另 import sys。'),
                           'imp': 'import json'}]},
            {'title': '浮点数',
             'imp': None,
             'sample': '2.5 3.25',
             'code': 'x, y = map(float, input().split())',
             'result': 'x = 2.5，y = 3.25',
             'note': '部分浮点运算有表示误差，如 0.1 + 0.2。print 不会额外制造误差；输出精度和小数位数按题面设置，不统一保留两位。'},
            {'title': '第一行 T 组数据',
             'imp': None,
             'sample': '2\n3 5\n4 1',
             'code': 'T = int(input())\n'
                     'for _ in range(T):\n'
                     '    a, b = map(int, input().split())\n'
                     '    print(a + b)',
             'result': '屏幕依次打出 8、5',
             'note': '主代码每组一行、恰好两个整数。变长数组用下面的 token 写法；示例用求和代替实际算法。',
             'variants': [{'title': 'T 组，每组先给 n 再给 n 个数',
                           'sample': '3\n3 1 2 3\n0\n2 -1 4',
                           'code': 'data = (x for line in sys.stdin for x in '
                                   'line.split())\n'
                                   'T = int(next(data))\n'
                                   'for _ in range(T):\n'
                                   '    n = int(next(data))\n'
                                   '    nums = [int(next(data)) for _ in range(n)]\n'
                                   '    print(sum(nums))',
                           'result': '屏幕依次输出 6、0、3',
                           'note': '字段可任意折行；n = 0 时没有数组 token。T = 0 不输出；一组已开始却缺少数据属于不完整输入。',
                           'imp': 'import sys'}]},
            {'title': '多组数据，读到文件尾（EOF）',
             'imp': 'import sys',
             'sample': '3 5\n4 1\n4 4',
             'code': 'for line in sys.stdin:\n'
                     '    if not line.strip():\n'
                     '        continue\n'
                     '    a, b = map(int, line.split())\n'
                     '    print(a + b)',
             'result': '屏幕依次打出 8、5、8',
             'note': '主代码每个非空行恰好两个整数；空行跳过，EOF 自动结束。每组含变长数组时用下面的按数量读取。',
             'variants': [{'title': '无 T，每组先给 n，读到 EOF',
                           'sample': '3 1 2 3\n0\n2 -1 4',
                           'code': 'data = (x for line in sys.stdin for x in '
                                   'line.split())\n'
                                   'for first in data:\n'
                                   '    n = int(first)\n'
                                   '    nums = [int(next(data)) for _ in range(n)]\n'
                                   '    print(sum(nums))',
                           'result': '屏幕依次输出 6、0、3',
                           'note': 'for 每次取得下一组的 n，组内继续从同一迭代器取数。n = 0 输出 '
                                   '0；空输入不输出；不能忽略一组中途缺失的数。',
                           'imp': 'import sys'}]},
            {'title': '读到哨兵值结束',
             'imp': 'import sys',
             'sample': '3 5\n4 1\n0 0',
             'code': 'for line in sys.stdin:\n'
                     '    if not line.strip():\n'
                     '        continue\n'
                     '    a, b = map(int, line.split())\n'
                     '    if a == 0 and b == 0:\n'
                     '        break\n'
                     '    print(a + b)',
             'result': '屏幕打出 8、5，读到 0 0 就停',
             'note': '每个非空行恰好两个整数，遇 0 0 或 EOF 都结束。若终止行只有 -1 或 0，须在解包前判断 '
                     'line.strip()，不能先读成两个数。'},
            {'title': '矩阵 / 网格',
             'imp': None,
             'sample': '2 3\n1 2 3\n4 5 6',
             'code': 'n, m = map(int, input().split())\n'
                     'g = [list(map(int, input().split())) for _ in range(n)]',
             'result': 'g = [[1, 2, 3], [4, 5, 6]]，g[1][2] = 6',
             'note': '主代码每行 m 个空白分隔整数。下方是边表转邻接表；无空格字符网格看⑪。',
             'variants': [{'title': '图：边表转邻接表',
                           'sample': '3 2\n1 2\n2 3',
                           'code': 'n, m = map(int, input().split())\n'
                                   'g = [[] for _ in range(n)]\n'
                                   'for _ in range(m):\n'
                                   '    u, v = map(int, input().split())\n'
                                   '    u -= 1\n'
                                   '    v -= 1\n'
                                   '    g[u].append(v)\n'
                                   '    g[v].append(u)',
                           'result': 'g = [[1], [0, 2], [1]]',
                           'note': '此例无向、无权，输入编号 1..n，内部改为 0..n-1。有向图不加反向边；带权图读 u, v, w，再存 '
                                   '(v, w)。不要写 [[]] * n。',
                           'imp': None}]},
            {'title': '字符网格（首行 n m）',
             'imp': None,
             'sample': '2 3\n.#.\n#..',
             'code': 'n, m = map(int, input().split())\n'
                     'g = [list(input()) for _ in range(n)]',
             'result': "g = [['.', '#', '.'], ['#', '.', '.']]",
             'note': ('每行恰好 m 个字符，首尾空格若为有效格子也保留。若首行只有 n，只把第一行改成 n = int(input())。input() 去掉末尾的换行符。若输入可能是 '
                      'CRLF，逐行去掉行尾后再转 list，参见⑫。')},
            {'title': '整行字符串（空格要保留）',
             'imp': None,
             'sample': 'hello world',
             'code': 's = input()              # 原样整行',
             'result': "s = 'hello world'",
             'note': 'input() 去掉末尾的换行符，保留其他空白；遇 EOF 抛 EOFError。若输入可能是 CRLF，使用下方的去行尾写法。',
             'variants': [{'title': '读到 EOF，保留空行和首尾空格',
                           'sample': ' a \n\nb',
                           'code': 'lines = []\n'
                                   'for line in sys.stdin:\n'
                                   "    if line.endswith('\\r\\n'):\n"
                                   '        line = line[:-2]\n'
                                   "    elif line.endswith('\\n'):\n"
                                   '        line = line[:-1]\n'
                                   '    lines.append(line)',
                           'result': "lines = [' a ', '', 'b']",
                           'note': ('for 读到 EOF 自动结束，空行仍会读到。代码只去掉 LF 或 CRLF，保留其他空白，最后一行没有换行也能读。若改用 '
                                    "readline()，返回 '' 才是 EOF。"),
                           'imp': 'import sys'}]},
            {'title': '整行字符串并去掉首尾空白',
             'imp': None,
             'sample': '   hello world   ',
             'code': 's = input().strip()      # 两端空白全去',
             'result': "s = 'hello world'",
             'note': 'strip() 去掉首尾空白，保留中间空格；题目要求原样保留时用上一条。纯空白行判空可写 if not s.strip():。'},
            {'title': '批量读取（数值 / 单词）',
             'imp': 'import sys',
             'sample': '5\n1 2 3 4 5',
             'code': 'data = iter(sys.stdin.buffer.read().split())\n'
                     'n = int(next(data))\n'
                     'nums = [int(next(data)) for _ in range(n)]',
             'result': 'n = 5，nums = [1, 2, 3, 4, 5]',
             'note': '主代码按 token 一次读完，需额外内存；数据量大不一定应全读，可用③逐行生成 token。后续继续 next(data)，不要混用 '
                     'input()。整行空白有意义、或交互题不能这样读。',
             'variants': [{'title': '批量读取 UTF-8 单词',
                           'sample': '2 hello 世界',
                           'code': 'data = iter(sys.stdin.buffer.read().split())\n'
                                   'n = int(next(data))\n'
                                   "words = [next(data).decode('utf-8') for _ in range(n)]",
                           'result': "words = ['hello', '世界']",
                           'note': ('buffer 读出 bytes，split() 按 ASCII 空白分词。int() 可直接转数值，文本要 decode。这里约定 '
                                    "UTF-8；其他编码按题面。str(b'abc') 不是解码；字段内空格不能靠 split 保留。"),
                           'imp': 'import sys'}]}]},
 {'id': 'acm-out',
  'name': '输出',
  'kind': '屏幕输出',
  'note': '输出格式逐字按题面：空格、换行、大小写、括号和精度都属于答案。空结果是否输出空行按题面；卡片给定变量需先由算法算出。',
  'cases': [{'title': '一个值',
             'imp': None,
             'sample': '8',
             'code': 'print(ans)',
             'result': 'ans = 8',
             'note': 'print(ans) 适合标量结果；一维空格分隔看②，矩阵看③/⑥。题面要求 JSON 时用下面的写法，不能直接输出 Python '
                     '容器表示。',
             'variants': [{'title': '题面要求 JSON 格式的结果',
                           'sample': '[["中"], true, null]',
                           'code': 's = json.dumps(ans, ensure_ascii=False, allow_nan=False)\nprint(s)',
                           'result': "ans = [['中'], True, None]",
                           'note': ("JSON 使用双引号、true / false / null。若要求紧凑格式，设 separators=(',', "
                                    "':')；allow_nan=False 会拒绝 NaN 和无穷值，输出保持标准 JSON。普通空格数组或矩阵不使用此格式。"),
                           'imp': 'import json'}]},
            {'title': '一行空格分隔',
             'imp': None,
             'sample': '1 2 3',
             'code': 'print(*nums)              # 空格分隔\n'
                     "# print(*nums, sep=', ')  # 逗号分隔：替换上一行\n"
                     "# print(*nums, sep='', end='')  # 拼接且不换行",
             'result': 'nums = [1, 2, 3]',
             'note': '备选写法只选一种；空列表用主代码会输出空行。end 控制末尾字符，sep 控制元素之间的分隔符。交互题按协议用 '
                     'flush=True；正式提交不输出提示或调试信息。'},
            {'title': '每行一个',
             'imp': None,
             'sample': '1\n2\n3',
             'code': 'for x in nums:\n    print(x)',
             'result': 'nums = [1, 2, 3]',
             'note': "空列表不输出。非空时也可写 print(*nums, sep='\\n')；该写法对空列表会多输出一个空行。",
             'variants': [{'title': '整数矩阵逐行输出',
                           'sample': '1 2\n3 4',
                           'code': 'for row in g:\n    print(*row)',
                           'result': 'g = [[1, 2], [3, 4]]',
                           'note': '每行空格分隔，行末不加多余空格；g 为空时不输出。空行是否为合法矩阵行按题面。',
                           'imp': None}]},
            {'title': '保留小数',
             'imp': None,
             'sample': '2.500000',
             'code': "print(f'{ans:.6f}')       # 小数点后 6 位",
             'result': 'ans = 2.5',
             'note': '示例按要求保留 6 位；位数按题面调整。固定小数位用 f-string；round() 返回数值，不保证显示末尾的 '
                     '0。格式化不能修复此前的计算误差。'},
            {'title': '布尔值（True / true / YES）',
             'imp': None,
             'sample': 'True',
             'code': 'print(ans)                         # True / False\n'
                     "# print('true' if ans else 'false')  # 要小写就换这句\n"
                     "# print('YES' if ans else 'NO')      # 判定题常用",
             'result': 'ans = True',
             'note': 'print(True) 打出首字母大写的 True；题面要 true 或 YES '
                     '就注释掉第一行、放开对应那行，大小写不一致等于答案错。'},
            {'title': '元素不是 int，拼成一行',
             'imp': None,
             'sample': 'a b c',
             'code': "print(' '.join(words))            # 全是 str\n"
                     "# print(' '.join(map(str, nums)))  # 有 int 先转",
             'result': "words = ['a', 'b', 'c']；nums = [1, 2, 3]",
             'note': 'join 只吃 str，混进 int 直接 TypeError；两行挑一行用。',
             'variants': [{'title': '字符矩阵逐行输出',
                           'sample': '.#.\n#..',
                           'code': "for row in g:\n    print(''.join(row))",
                           'result': "g = [['.', '#', '.'], ['#', '.', '.']]",
                           'note': '行内不插空格，每个元素必须是字符串。不要用 print(*row)，它默认插空格；g 为空时不输出。',
                           'imp': None}]},
            {'title': '多组结果按行输出',
             'imp': None,
             'sample': '8\n5',
             'code': 'out = []\n'
                     'for _ in range(T):\n'
                     '    out.append(str(solve()))\n'
                     'if out:\n'
                     "    print('\\n'.join(out))",
             'result': 'T = 2，solve() 依次返回 8、5',
             'note': 'solve() 需按题意实现，每次返回一个标量或已经按题意拼好的单行字符串；先转字符串再 join。T = 0 时不输出；批量输出额外占用内存。'},
            {'title': '带 Case 编号',
             'imp': None,
             'sample': 'Case #1: 8\nCase #2: 5',
             'code': "for i in range(1, T + 1):\n    print(f'Case #{i}: {solve()}')",
             'result': 'T = 2，solve() 依次返回 8、5',
             'note': 'solve() 需按题意实现；Case 编号从 1 开始，井号、冒号和空格严格按题面要求。'}]}]
