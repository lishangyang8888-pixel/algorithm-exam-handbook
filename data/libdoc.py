# -*- coding: utf-8 -*-
"""
附录数据：沿用分组、导入提示、签名和行为标记。
常用组整组展示；每项说明至少包含一条「| 代码 -> 结果」示例。
输入输出模板单独放在 data/acm.py。
"""

# 每个函数的行为类型，渲染成语法行末尾的小徽章。
#   原地        改的是原对象，返回值一般是 None
#   原地+返回   既改原对象，又把被删/被弹的东西返回
#   返回        不改原对象，返回新值或新对象
#   输出        写到 stdout，不改也不返回
#   属性 / 参数  不是普通函数调用
# 不在这里的函数一律按「返回」处理。
KINDS: dict[str, str] = {'append': '原地',
 'insert': '原地',
 'add': '原地',
 'discard': '原地',
 'sort': '原地',
 'appendleft': '原地',
 'heapify': '原地',
 'heappush': '原地',
 'd[key] = val': '原地',
 'setrecursionlimit': '设置',
 'pop': '原地+返回',
 'popleft': '原地+返回',
 'heappop': '原地+返回',
 'heapreplace': '原地+返回',
 'print': '输出',
 'stdin': '属性',
 'inf': '属性',
 'key': '参数',
 'extend': '原地',
 'remove': '原地',
 'clear': '原地',
 'reverse': '原地',
 'update': '原地',
 'dict.pop': '原地+返回',
 'set.pop': '原地+返回',
 'deque.pop': '原地+返回',
 'deque.append': '原地',
 'setdefault': '原地+返回',
 '局部变量': '作用域',
 'nonlocal': '作用域',
 'global': '作用域',
 '修改容器': '作用域',
 '赋值': '赋值',
 '优先级': '规则',
 'if': '流程控制',
 'for': '流程控制',
 'while': '流程控制',
 'continue': '流程控制',
 'break': '流程控制',
 'return': '流程控制',
 '循环 else': '流程控制',
 'pass': '流程控制'}

GROUPS: list[tuple[str, str, dict[str, tuple[str, str]]]] = [('堆 heapq（import heapq）',
  '先 import heapq。为兼容较旧的考试环境，这里用小根堆；大根堆可存负数，弹出时取反。Python 3.14 起另有公开的大根堆接口。\n'
  '堆只保证堆顶最小，不保证整表有序。基础堆操作没有 key 参数；元组逐项比较，后续字段也必须可比较，或加入唯一计数器避免比较对象。',
  {'heapify': ('heapq.heapify(h)', '原地建小根堆，O(n)，返回 None。\n| h = [3, 1, 2]; heapq.heapify(h); h[0] -> 1'),
   'heappush': ('heapq.heappush(h, x)',
                '压入一个元素，O(log n)，返回 None。\n| h = [1, 3, 2]; heapq.heappush(h, 0); (h[0], len(h)) -> (0, 4)'),
   'heappop': ('heapq.heappop(h)',
               '移除并返回最小值，O(log n)；空堆抛 IndexError。\n| h = [1, 3, 2]; heapq.heappop(h) -> 1'),
   'heapreplace': ('heapq.heapreplace(h, x)',
                   '移除并返回旧堆顶，再压入 x；堆不能为空。\n'
                   '| h = [1, 3, 2]; heapq.heapreplace(h, 5) -> 1')}),
 ('排序（不用 import）',
  '默认升序，reverse=True 降序；两种排序都稳定，key 相同的元素保持原有先后。只能比较彼此可排序的元素。\n'
  '语法行展示常用参数；变量名是占位，实际调用看下一行示例。',
  {'sorted': ('sorted(iterable, key=None, reverse=False)',
              '返回排序后的新列表，不修改原容器；key、reverse 用关键字传入。\n| sorted([3, 1, 2]) -> [1, 2, 3]'),
   'sort': ('a.sort(key=None, reverse=False)',
            '列表原地排序，返回 None；不要写 a = a.sort()。\n| a = [3, 1, 2]; a.sort(); a -> [1, 2, 3]'),
   'key': ('key=lambda x: x[0]',
           '下标从 0 起：x[0] 是第一个字段，x[1] 是第二个。元组多关键字依次比较；数字前加负号可让该字段降序。\n'
           '| sorted([(1, 2), (1, 3)], key=lambda x: (x[0], -x[1])) -> [(1, 3), (1, 2)]\n'
           "| sorted(['bb', 'a'], key=len) -> ['a', 'bb']")}),
 ('查找下标（str / list 不用 import）',
  'find / rfind 用于字符串，找不到返回 -1；str.index / list.index 找不到抛 ValueError。\n'
  '可选起止下标是左闭右开，作为位置参数传入；有序数组找插入位置可用 bisect。',
  {'find': ('s.find(sub)',
            '返回子串第一次出现的下标；可写 s.find(sub, start, end)。\n'
            "| 'abcabc'.find('b') -> 1\n"
            "| 'abcabc'.find('z') -> -1"),
   'rfind': ('s.rfind(sub)',
             "返回子串最后一次出现的下标；可写 s.rfind(sub, start, end)。\n| 'abcabc'.rfind('b') -> 4"),
   'index': ('s.index(sub) / a.index(x)',
             '返回第一次出现的下标；可加起止下标。找不到抛 ValueError。\n'
             '| [3, 1, 3].index(3) -> 0\n'
             '| [1].index(9) -> ValueError')}),
 ('二分 bisect（import bisect）',
  '先 import bisect。列表必须已按升序排列；返回插入位置，可能等于 len(a)，不代表目标存在。',
  {'bisect_left': ('bisect.bisect_left(a, x)',
                   '返回第一个 >= x 的位置；可用 lo、hi 限定左闭右开区间。判存在还需比较值。\n'
                   '| bisect.bisect_left([1, 3, 3, 5], 3) -> 1\n'
                   '| a = [1, 3, 5]; i = bisect.bisect_left(a, 4); i < len(a) and a[i] == '
                   '4 -> False'),
   'bisect_right': ('bisect.bisect_right(a, x)',
                    '返回第一个 > x 的位置；右边界减左边界就是有序数组中 x 的个数。\n'
                    '| bisect.bisect_right([1, 3, 3, 5], 3) -> 3')}),
 ('队列与计数 collections（import collections）',
  '先 import collections。q 是 collections.deque 的实例；字典工厂用 collections.defaultdict。\n'
  '两端追加、弹出为 O(1)；中间下标访问可能为 O(n)。空队列弹出会抛 IndexError。',
  {'deque': ('collections.deque(iterable=(), maxlen=None)',
             '构造双端队列。maxlen 限长时，追加时若已满，append / appendleft 会挤掉另一端元素。\n'
             '| q = collections.deque([1, 2]); list(q) -> [1, 2]\n'
             '| q = collections.deque([1, 2], maxlen=2); q.append(3); list(q) -> [2, 3]'),
   'popleft': ('q.popleft()',
               '移除并返回左端元素；BFS 常用。\n| q = collections.deque([1, 2]); q.popleft() -> 1'),
   'appendleft': ('q.appendleft(x)',
                  '左端追加，返回 None。\n'
                  '| q = collections.deque([1, 2]); q.appendleft(0); list(q) -> [0, 1, 2]'),
   'defaultdict': ('collections.defaultdict(default_factory)',
                   '缺键时，d[key] 调工厂生成默认值并存入字典；get() 不触发工厂。工厂可用 int、list、set。\n'
                   "| d = collections.defaultdict(int); d['x'] += 1; dict(d) -> {'x': 1}\n"
                   "| d = collections.defaultdict(list); d['k'].append(1); dict(d) -> "
                   "{'k': [1]}"),
   'Counter': ('collections.Counter(iterable)',
               '先 import collections，也可 from collections import Counter。返回计数对象。用 c[key] 查缺失的键时返回 0，不会插入该键。Python 3.10 起可用 >= 逐项比较计数，缺项按 0 处理。\n'
               "| collections.Counter('aba')['a'] -> 2\n"
               "| collections.Counter('aba')['x'] -> 0\n"
               "| collections.Counter('aba') >= collections.Counter('aa') -> True"),
   'deque.append': ('q.append(x)',
                    '右端追加，返回 None。\n'
                    '| q = collections.deque([1, 2]); q.append(3); list(q) -> [1, 2, 3]'),
   'deque.pop': ('q.pop()', '移除并返回右端元素。\n| q = collections.deque([1, 2]); q.pop() -> 2')}),
 ('列表 list（lst.xxx）',
  'a 是列表。原地方法通常返回 None；pop 既修改列表又返回元素。copy 只做浅拷贝，嵌套对象仍共享。',
  {'append': ('a.append(x)', '尾部追加一个元素。\n| a = [1]; a.append([2, 3]); a -> [1, [2, 3]]'),
   'insert': ('a.insert(i, x)',
              '在下标 i 前插入，O(n)。\n| a = [1, 3]; a.insert(1, 2); a -> [1, 2, 3]'),
   'pop': ('a.pop() / a.pop(i)',
           '移除并返回下标 i 的元素；默认末尾，i 用位置参数传入。越界或空列表抛 IndexError。\n| a = [1, 2, 3]; a.pop() -> 3'),
   'extend': ('a.extend(iterable)',
              '把可迭代对象的元素逐个追加，区别于 append 整体追加。\n'
              '| a = [1]; a.extend([2, 3]); a -> [1, 2, 3]'),
   'remove': ('a.remove(x)',
              '移除第一个等于 x 的元素；不存在抛 ValueError。\n| a = [1, 2, 1]; a.remove(1); a -> [2, 1]'),
   'reverse': ('a.reverse()',
               '原地反转，返回 None；需要新列表可写 a[::-1]。\n'
               '| a = [1, 2, 3]; a.reverse(); a -> [3, 2, 1]'),
   'copy': ('a.copy()',
            '复制外层列表，内部可变对象仍共享。\n'
            '| a = [1, 2]; a.copy() -> [1, 2]\n'
            '| a = [[1]]; b = a.copy(); b[0].append(2); a -> [[1, 2]]'),
   'clear': ('a.clear()', '移除全部元素，返回 None。\n| a = [1, 2]; a.clear(); a -> []'),
   '切片': ('a[start:stop:step]',
           'stop 不包含在内。读取列表切片会创建新列表。a[:] = new 修改原列表，a = new 则重新绑定名字。\n'
           '| [0, 1, 2, 3][1:3] -> [1, 2]\n'
           '| a = [1, 2]; b = a; a[:] = [3]; b -> [3]'),
   '列表推导式': ('列表推导式  [表达式 for 变量 in 可迭代对象 if 条件]',
 '无需 import。按遍历顺序计算表达式，得到一个新列表。末尾的 if 条件可以省略。\n'
 '记忆句 `[表达式 for 变量 in 可迭代对象 if 条件]`\n'
 '遍历\n'
 '| nums = [1, 2, 3]; [i for i in nums] -> [1, 2, 3]\n'
 '筛选\n'
 '| nums = [1, 2, 3]; [i for i in nums if i > 1] -> [2, 3]\n'
 '转换\n'
 '| nums = [1, 2, 3]; [i * 2 for i in nums] -> [2, 4, 6]\n'
 '筛选 + 转换\n'
 '| nums = [1, 2, 3]; [i * 2 for i in nums if i > 1] -> [4, 6]')}),
 ('字典 dict（d.xxx）',
  'd 是字典。in 默认查键；查键和按键取值通常为平均 O(1)。遍历 items / keys / values 时不要增删字典条目。',
  {'d[key]': ('d[key]', "按键取值；缺键抛 KeyError。\n| {'a': 1}['a'] -> 1"),
   'd[key] = val': ('d[key] = val', "键存在就覆盖，不存在就新建。\n| d = {}; d['a'] = 1; d -> {'a': 1}"),
   'key in d': ('key in d', "判断键是否存在，不查值。\n| 'a' in {'a': 1} -> True"),
   'get': ('d.get(key) / d.get(key, default)', "按键取值，缺键返回默认值，不自动插入。默认值用位置参数传入。\n| {'a': 1}.get('b', 0) -> 0"),
   'items': ('d.items()', "返回键值对视图；需要列表时再 list()。\n| list({'a': 1}.items()) -> [('a', 1)]"),
   'values': ('d.values()', "返回值视图。\n| list({'a': 1}.values()) -> [1]"),
   'keys': ('d.keys()', "返回键视图；直接 for key in d 也会遍历键。\n| list({'a': 1}.keys()) -> ['a']"),
   'setdefault': ('d.setdefault(key) / d.setdefault(key, default)',
                  '存在就返回原值；缺键则插入并返回 default，省略时插入 None。参数按位置传入。\n'
                  "| d = {}; d.setdefault('x', []).append(1); d -> {'x': [1]}"),
   'dict.pop': ('d.pop(key) / d.pop(key, default)',
                '移除并返回键对应的值；default 可省，缺键且无默认值抛 KeyError。\n'
                "| d = {'a': 1}; d.pop('a') -> 1\n"
                "| {}.pop('x', 0) -> 0"),
   'update': ('d.update(other)',
              '用另一个映射或键值对序列更新字典；同键覆盖，返回 None。\n'
              "| d = {'a': 1}; d.update({'a': 2, 'b': 3}); d -> {'a': 2, 'b': 3}")}),
 ('字符串 str（s.xxx）',
  '不修改原字符串；split 返回 list，find / count 返回 int，join / strip 等返回 str，is... 方法返回 bool。\n'
  '字符判断方法识别 Unicode，不限于英文字母或 ASCII 数字；下列 is... 判断中，除 isascii 外，空串都返回 False。',
  {'split': ('s.split(sep=None, maxsplit=-1)',
             '省略 sep 按任意空白切分，并丢掉首尾空白及空分片。指定 sep 按该子串切分，连续分隔符保留空分片；maxsplit 限制切分次数。\n'
             "| '  a  b  '.split() -> ['a', 'b']\n"
             "| 'a,b,,c'.split(',') -> ['a', 'b', '', 'c']\n"
             "| 'a,b,c'.split(',', 1) -> ['a', 'b,c']"),
   'join': ('sep.join(iterable)',
            '用 sep 连接字符串；元素必须全是 str。join 不会自动把整数转成字符串。\n'
            "| ','.join(['a', 'b', 'c']) -> 'a,b,c'\n"
            "| ' '.join(map(str, [1, 2, 3])) -> '1 2 3'"),
   'bytes.decode': ("data.decode('utf-8')",
                    '按指定编码把 bytes 解码为 str。编码不匹配时默认抛 UnicodeDecodeError。\n'
                    "| b'abc'.decode('utf-8') -> 'abc'"),
   'strip': ('s.strip() / s.strip(chars)',
             '默认去掉两端空白；chars 指字符集合，不是完整子串。\n'
             "| '  a  '.strip() -> 'a'\n"
             "| 'xyaxy'.strip('xy') -> 'a'\n"
             "| ' a '.strip(chars=' ') -> TypeError"),
   'replace': ('s.replace(old, new) / s.replace(old, new, count)',
               '返回替换后的字符串；count 限制替换次数，省略或传 -1 则全部替换。为兼容旧版 Python，把 count 作为第三个位置参数。\n'
               "| 'a-b-c'.replace('-', '+', 1) -> 'a+b-c'"),
   'lower': ('s.lower()', "返回转小写后的字符串。\n| 'AbC'.lower() -> 'abc'"),
   'upper': ('s.upper()', "返回转大写后的字符串。\n| 'AbC'.upper() -> 'ABC'"),
   'isdigit': ('s.isdigit()',
               '非空且全是数字字符，包括部分上标数字。返回 True 也不保证 int() 能转换。\n'
               "| '123'.isdigit() -> True\n"
               "| '²'.isdigit() -> True\n"
               "| '-1'.isdigit() -> False\n"
               "| '1.5'.isdigit() -> False\n"
               "| int('²') -> ValueError"),
   'lstrip': ('s.lstrip() / s.lstrip(chars)', "只去掉左端指定字符或空白；保留行内和右端字符。\n| '  a  '.lstrip() -> 'a  '"),
   'rstrip': ('s.rstrip() / s.rstrip(chars)',
              "只去掉右端指定字符或空白；chars 是字符集合。若只应去掉一组 LF 或 CRLF，见输入⑫的去行尾模板。\n| 'a\\n'.rstrip('\\n') -> 'a'"),
   'isdecimal': ('s.isdecimal()',
                 '非空且全是十进制数字字符；比 isdigit 更窄。只接受 ASCII 数字可同时判断 isascii()。\n'
                 "| '²'.isdecimal() -> False\n"
                 "| s = '123'; s.isascii() and s.isdecimal() -> True"),
   'isnumeric': ('s.isnumeric()',
                 '非空且全是 Unicode 数值字符；范围比 isdigit 更宽，包含部分分数。True 不保证 int() 能转换。\n'
                 "| '½'.isnumeric() -> True"),
   'isalpha': ('s.isalpha()',
               '非空且全是 Unicode 字母，中文也可通过；不代表仅 a-z / A-Z。\n'
               "| '中文'.isalpha() -> True\n"
               "| 'a1'.isalpha() -> False"),
   'isalnum': ('s.isalnum()',
               "非空且全是字母或数值字符；下划线不算。\n| 'a1'.isalnum() -> True\n| 'a_1'.isalnum() -> False"),
   'isspace': ('s.isspace()',
               '非空且全是空白字符，包含空格、Tab、换行。\n'
               "| ' \\t'.isspace() -> True\n"
               "| ''.isspace() -> False"),
   'isascii': ('s.isascii()',
               '是否全部为 ASCII 字符；空串也返回 True。\n'
               "| 'abc123'.isascii() -> True\n"
               "| '中'.isascii() -> False"),
   'islower': ('s.islower()',
               '至少有一个区分大小写的字符，且这些字符全为小写；数字不影响判断。\n'
               "| 'abc1'.islower() -> True\n"
               "| '123'.islower() -> False"),
   'isupper': ('s.isupper()', "至少有一个区分大小写的字符，且这些字符全为大写。\n| 'ABC1'.isupper() -> True"),
   'startswith': ('s.startswith(prefix)',
                  "判断前缀；prefix 可是字符串或字符串元组。\n| 'hello.py'.startswith('hello') -> True"),
   'endswith': ('s.endswith(suffix)',
                "判断后缀；suffix 可是字符串或字符串元组。\n| 'hello.py'.endswith(('.py', '.txt')) -> True"),
   'count': ('s.count(sub)', "统计不重叠的子串出现次数；不是滑动重叠计数。\n| 'aaaa'.count('aa') -> 2")}),
 ('集合 set（st.xxx）',
  'st 是集合，元素必须可哈希；集合无序，不能用下标访问。空集合写 set()，{} 是空字典。成员判断平均 O(1)。',
  {'add': ('st.add(x)', '加入一个元素；已有元素不重复添加，返回 None。\n| st = {1}; st.add(2); st -> {1, 2}'),
   'discard': ('st.discard(x)',
               '移除元素，不存在也不报错，返回 None。\n| st = {1, 2}; st.discard(9); st -> {1, 2}'),
   'remove': ('st.remove(x)',
              '移除元素，不存在抛 KeyError，返回 None。\n| st = {1, 2}; st.remove(1); st -> {2}'),
   'set.pop': ('st.pop()', '移除并返回任意一个元素；不是按顺序弹出。空集合抛 KeyError。\n| st = {7}; st.pop() -> 7'),
   '集合运算': ('a & b / a | b / a - b / a ^ b',
            '分别返回交集、并集、差集、对称差集，不修改 a、b。\n'
            '| {1, 2} & {2, 3} -> {2}\n'
            '| {1, 2} | {2, 3} -> {1, 2, 3}\n'
            '| {1, 2} - {2, 3} -> {1}\n'
            '| {1, 2} ^ {2, 3} -> {1, 3}')}),
 ('内置函数（不用 import）',
  '无需 import。返回迭代器的函数不会自动产生列表，需要保存或显示所有元素时用 list()。迭代器通常只能消耗一次。',
  {'abs': ('abs(x)', '返回绝对值。\n| abs(-3) -> 3'),
   'chr': ('chr(i)', "Unicode 码点转单个字符；越界抛 ValueError。\n| chr(97) -> 'a'"),
   'dict': ('dict() / dict(pairs)',
            "构造字典；pairs 中每项是一个键值对。\n| dict(zip('ab', [1, 2])) -> {'a': 1, 'b': 2}"),
   'enumerate': ('enumerate(iterable, start=0)',
                 '返回逐项产生 (编号, 元素) 的迭代器。\n'
                 "| list(enumerate('ab', 1)) -> [(1, 'a'), (2, 'b')]"),
   'float': ('float(x)',
             "转换为浮点数；非法数字文本抛 ValueError。float('inf') 和 float('-inf') 分别返回正无穷和负无穷，可作为边界或不可达状态的初值。\n"
             "| float('1.5') -> 1.5\n"
             "| float('inf') > 10**308 -> True\n"
             "| float('-inf') < -100 -> True"),
   'int': ('int(x) / int(text, base)',
           '数字转整数向零截断；指定 base 时，输入须为 str、bytes 或 bytearray。\n'
           "| int('10', 2) -> 2\n"
           '| int(-3.9) -> -3'),
   'len': ('len(obj)', "返回内置容器元素数或字符串字符数；不是迭代器通用接口。\n| len('abc') -> 3"),
   'list': ('list(iterable=())', '构造列表；将迭代器的剩余元素物化。\n| list(range(3)) -> [0, 1, 2]'),
   'max': ('max(iterable, key=None) / max(a, b, ...)',
           '返回最大元素；空可迭代对象需给 default，否则 ValueError。default 只适用于单个 iterable 的形式。\n'
           '| max([1, 3, 2]) -> 3\n'
           '| max([], default=0) -> 0\n'
           '| max(2, 5) -> 5'),
   'min': ('min(iterable, key=None) / min(a, b, ...)',
           '返回最小元素；空输入、default 的规则同 max。\n| min([1, 3, 2]) -> 1'),
   'ord': ('ord(c)', "单个 Unicode 字符转码点；字符串长度必须为 1。\n| ord('a') -> 97"),
   'range': ('range(stop) / range(start, stop, step=1)',
             '整数范围，左闭右开；step 可负但不能为 0。方向不匹配时为空。\n'
             '| list(range(3)) -> [0, 1, 2]\n'
             '| list(range(2, -1, -1)) -> [2, 1, 0]'),
   'set': ('set(iterable=())', '构造集合并去重；元素须可哈希。\n| set([1, 1, 2]) -> {1, 2}'),
   'str': ('str(obj)', "转换成字符串；容器转换不是按指定分隔符连接，要连接元素用 join。\n| str(12) + '3' -> '123'"),
   'sum': ('sum(iterable, start=0)',
           '累加数值；不用于连接字符串。二维列表展平优先用推导式，避免反复复制。\n'
           '| sum([1, 2, 3]) -> 6\n'
           '| g = [[1, 2], [3]]; [x for row in g for x in row] -> [1, 2, 3]'),
   '生成器表达式': ('(表达式 for 变量 in 可迭代对象 if 条件)',
                   '生成器按需计算，用 next() 或循环消费，一般只能遍历一遍。与列表推导式相比，不会一次建好结果列表。\n'
                   '| g = (x * x for x in [1, 2, 3])\n'
                   '| (next(g), list(g), list(g)) -> (1, [4, 9], [])'),
   'zip': ('zip(*iterables)',
           '返回按位置配对的迭代器，默认到最短输入结束；转置要求矩阵各行等长。\n'
           "| list(zip('ab', [1, 2])) -> [('a', 1), ('b', 2)]"),
   'map': ('map(func, iterable)',
           "返回逐个应用 func 的迭代器；多输入时到最短输入结束。\n| list(map(int, ['1', '2'])) -> [1, 2]"),
   'filter': ('filter(func, iterable)',
              '返回仅保留判断为真的元素的迭代器；func 为 None 时按元素自身真假筛选。\n'
              '| list(filter(lambda x: x > 0, [-1, 0, 2])) -> [2]'),
   'any': ('any(iterable)',
           '任意元素为真则 True，短路；空输入为 False。\n| any([False, True]) -> True\n| any([]) -> False'),
   'all': ('all(iterable)',
           '所有元素为真则 True，短路；空输入为 True。\n| all([True, False]) -> False\n| all([]) -> True'),
   'reversed': ('reversed(seq)',
                '返回逆序迭代器，不修改原序列。\n| list(reversed([1, 2, 3])) -> [3, 2, 1]'),
   'divmod': ('divmod(a, b)', '返回 (a // b, a % b)；整数除数不能为 0。\n| divmod(7, 3) -> (2, 1)'),
   'round': ('round(number, ndigits=None)',
             '返回舍入后的数值，不保证显示固定小数位。恰好中点时取偶数；浮点表示可能影响十进制预期。\n'
             '| round(2.5) -> 2\n'
             '| round(3.5) -> 4'),
   'iter': ('iter(iterable)', '创建迭代器；next() 每次消耗一个元素。\n| it = iter([4, 5]); next(it) -> 4'),
   'next': ('next(iterator) / next(iterator, default)',
            '取下一项；default 可省，按位置传入，耗尽且无默认值抛 StopIteration。\n| next(iter([]), None) -> None'),
   'pow': ('pow(base, exp, mod=None)',
           '两参数时与 base ** exp 同义；三个整数参数可直接计算模幂，mod 不能为 0。\n'
           '| pow(2, 3) -> 8\n'
           '| pow(2, 10, 7) -> 2')}),
 ('递归深度（import sys）',
  '先 import sys。只在确需更深递归时调整；过高的上限不保证能安全递归到该深度，深链可改用显式栈。',
  {'getrecursionlimit': ('sys.getrecursionlimit()',
                         '返回当前解释器的递归深度上限。先读出再决定是否提高。\n'
                         '| sys.getrecursionlimit() > 0 -> True'),
   'setrecursionlimit': ('sys.setrecursionlimit(n)',
                         '设置解释器递归深度上限，返回 None；不是预分配或保证可用的栈空间。\n'
                         '| old = sys.getrecursionlimit()\n'
                         '| sys.setrecursionlimit(max(old, 2000))\n'
                         '| changed = sys.getrecursionlimit()\n'
                         '| sys.setrecursionlimit(old)\n'
                         '| changed >= 2000 -> True')}),
 ('链表节点（判题平台提供）',
  '普通链表题使用 ListNode。随机链表题使用带 random 的 Node。判题平台提供这两种定义，本地运行时可先复制对应定义。LRU 的双向 Node 见题内代码。',
  {'ListNode': ('ListNode(val=0, next=None)',
                '返回单链表节点。val 是值，next 是下一个节点或 None。\n'
                '| class ListNode:\n'
                '|     def __init__(self, val=0, next=None):\n'
                '|         self.val = val\n'
                '|         self.next = next\n'
                '| head = ListNode(1, ListNode(2))\n'
                '| (head.val, head.next.val, head.next.next) -> (1, 2, None)'),
   'Node': ('Node(x, next=None, random=None)',
            '返回带随机指针的节点。val 保存 x，next 和 random 都可以是节点或 None。\n'
            '| class Node:\n'
            '|     def __init__(self, x, next=None, random=None):\n'
            '|         self.val = x\n'
            '|         self.next = next\n'
            '|         self.random = random\n'
            '| head = Node(7)\n'
            '| head.random = head\n'
            '| (head.val, head.next, head.random is head) -> (7, None, True)')}),
 ('二叉树节点（判题平台提供）',
  'LeetCode 的二叉树题已提供 TreeNode。下面是本地运行示例时可用的最小定义。',
  {'TreeNode': ('TreeNode(val=0, left=None, right=None)',
                '返回一个树节点，val 是节点值，left 和 right 是子节点或 None。\n'
                '| class TreeNode:\n'
                '|     def __init__(self, val=0, left=None, right=None):\n'
                '|         self.val = val\n'
                '|         self.left = left\n'
                '|         self.right = right\n'
                '| root = TreeNode(1, TreeNode(2))\n'
                '| (root.val, root.left.val, root.right) -> (1, 2, None)')}),
 ('数学 math（import math）',
  'math.xxx 先 import math。整数平方根用 isqrt，普通 sqrt 返回浮点数；乘方 ** 见运算符组。',
  {'inf': ('math.inf', '正无穷；负无穷写 -math.inf，常用作边界初值。\n| math.inf > 10**308 -> True'),
   'gcd': ('math.gcd(a, b)', '返回非负最大公约数。\n| math.gcd(12, 18) -> 6'),
   'isqrt': ('math.isqrt(n)',
             '返回非负整数 n 的平方根向下取整值，结果为 int；负数抛 ValueError。枚举 j**2 <= n，可写 range(1, '
             'math.isqrt(n) + 1)。\n'
             '| math.isqrt(10) -> 3\n'
             '| math.isqrt(16) -> 4'),
   'sqrt': ('math.sqrt(x)', '返回平方根浮点值；负数在实数域抛 ValueError。\n| math.sqrt(9) -> 3.0'),
   'ceil': ('math.ceil(x)', '向正无穷取整。\n| math.ceil(-1.2) -> -1'),
   'floor': ('math.floor(x)', '向负无穷取整；区别于 int() 的向零截断。\n| math.floor(-1.2) -> -2')}),
 ('随机 random（import random）',
  '先 import random。randint 的左右端点都包含；随机结果不固定。',
  {'randint': ('random.randint(a, b)',
               '返回闭区间 [a, b] 中的随机整数。\n| x = random.randint(1, 6); 1 <= x <= 6 -> True')}),
 ('运算符（不用 import）',
  '以下语法行是写法示意，等宽示例可直接运行。算术、比较、逻辑和位运算均不用 import。',
  {'+ - *': ('a + b、a - b、a * b',
             '数值加、减、乘。\n'
             '| 2 + 3 -> 5\n'
             '| 7 - 4 -> 3\n'
             '| 3 * 4 -> 12'),
   '/': ('a / b', '真除法；两个整数相除也返回 float。除数不能为 0。\n| 7 / 2 -> 3.5\n| 6 / 2 -> 3.0'),
   '//': ('a // b',
          '向负无穷取整的除法，不是向零截断。整数输入得到 int；有浮点输入时结果为 float。除数不能为 0。\n'
          '| 7 // 3 -> 2\n'
          '| -7 // 3 -> -3'),
   '%': ('a % b',
         '取余；非零余数与除数同号。整数满足 a == (a // b) * b + a % b；除数不能为 0。\n'
         '| 7 % 2 -> 1\n'
         '| -7 % 3 -> 2\n'
         '| 7 % -3 -> -2'),
   '**': ('a ** b（平方：j ** 2）',
          '乘方，不用 import；j ** 2 是平方。^ 是按位异或，不能当作平方或乘方。\n'
          '| 3 ** 2 -> 9\n'
          '| 2 ** 3 -> 8\n'
          '| 3 ^ 2 -> 1'),
   '比较': ('==、!=、<、<=、>、>=',
              '内置数值和字符串的比较返回 bool；支持连续比较。赋值 = 不等于比较 ==。\n'
              '| 3 == 3 -> True\n'
              '| 3 != 4 -> True\n'
              '| 1 < 2 <= 2 -> True'),
   'and': ('a and b',
           '逻辑与，短路；a 为假时直接返回 a，否则求值并返回 b，不保证返回 bool。\n| 0 and 5 -> 0\n| 2 and 5 -> 5'),
   'or': ('a or b', '逻辑或，短路；a 为真时直接返回 a，否则求值并返回 b。左侧为真时不会求值右侧，不保证返回 bool。\n| 0 or 5 -> 5\n| 2 or 5 -> 2'),
   'not': ('not a', '对对象的真假取反，返回 bool；0、空容器、None 为假。\n| not [] -> True\n| not 3 -> False'),
   '位运算': ('a & b、a | b、a ^ b、~a',
           '这里是整数的按位与、或、异或、取反；不是逻辑 and / or。集合的 &、| 另见集合组。\n'
           '| 5 & 3 -> 1\n'
           '| 5 | 3 -> 7\n'
           '| 5 ^ 3 -> 6\n'
           '| ~5 -> -6'),
   '移位': ('a << k、a >> k',
          '整数左移、右移，k 不能为负。左移相当于乘 2**k，右移相当于 // 2**k。\n'
          '| 3 << 2 -> 12\n'
          '| 12 >> 1 -> 6\n'
          '| -3 >> 1 -> -2'),
   '成员判断': ('x in obj、x not in obj',
            "判断成员是否存在；字典默认查键，字符串查子串。\n| 2 in [1, 2] -> True\n| 'a' in {'a': 1} -> True"),
   '身份判断': ('a is b、a is not b',
            '判断是否同一对象，不等于数值或内容相等；判断空值常写 x is None。\n'
            '| a = [1]; b = [1]; a == b -> True\n'
            '| a = [1]; b = [1]; a is b -> False'),
   '赋值': ('=、+=、-=、*=、/=、//=、%=',
              '给变量赋值会绑定名字，也可以给下标或属性赋值；增强赋值的行为取决于类型。整数 += 重新绑定，列表 += 可原地扩展并影响别名。\n'
              '| x = 2; x += 3; x -> 5\n'
              '| a = [1]; b = a; a += [2]; b -> [1, 2]'),
   '条件表达式': ('a if condition else b',
             "按条件选择一个结果，只求值选中的分支。\n| 'yes' if 3 > 2 else 'no' -> 'yes'"),
   '优先级': ('括号、乘方、乘除取余、加减',
           '常用顺序按此排列，复杂表达式用括号说明意图。** 右结合；负号与乘方一起使用时注意括号。\n'
           '| 2 + 3 * 4 -> 14\n'
           '| (2 + 3) * 4 -> 20\n'
           '| 2 ** 3 ** 2 -> 512\n'
           '| -2 ** 2 -> -4\n'
           '| (-2) ** 2 -> 4')}),
 ('作用域（不用 import）',
  '以下是作用域语法，不是库函数，不用 import。代码例子中的缩进必须保留；单独读取外层变量不需要声明。',
  {'局部变量': ('函数内赋值',
            '函数内重新绑定名字默认创建局部变量；外层同名变量不会因此改变。\n'
            '| x = 7\n'
            '| def f():\n'
            '|     x = 2\n'
            '|     return x\n'
            '| (f(), x) -> (2, 7)'),
   'nonlocal': ('nonlocal name',
                '在嵌套函数中，重新绑定最近外层函数已经存在的变量。不能用来指向模块全局，也不能凭空创建外层变量；声明应在使用该名字之前。\n'
                '| def outer():\n'
                '|     flag = False\n'
                '|     def inner():\n'
                '|         nonlocal flag\n'
                '|         flag = True\n'
                '|     inner()\n'
                '|     return flag\n'
                '| outer() -> True'),
   'global': ('global name',
              '在函数中声明名字属于模块全局作用域；与 nonlocal 指向外层函数不同。\n'
              '| count = 0\n'
              '| def add():\n'
              '|     global count\n'
              '|     count += 1\n'
              '| add()\n'
              '| count -> 1'),
   '修改容器': ('path.append(x)、path.pop()',
            '修改外层列表对象本身不需 nonlocal；对 path 重新赋值才是重新绑定名字。\n'
            '| def outer():\n'
            '|     path = []\n'
            '|     def add():\n'
            '|         path.append(1)\n'
            '|     add()\n'
            '|     return path\n'
            '| outer() -> [1]')}),
 ('流程控制（不用 import）',
 '本组收录条件分支、循环和退出语句。用缩进确定语句所属的代码块。',
 {'if': ('if 条件: … elif 条件: … else: …',
         '按顺序判断条件，只执行首个为真的分支。前面的条件全为假时执行 else。elif 和 else 都可省略。\n'
         '| x = 0\n'
         '| if x < 0:\n'
         "|     label = '负数'\n"
         '| elif x == 0:\n'
         "|     label = '零'\n"
         '| else:\n'
         "|     label = '正数'\n"
         "| label -> '零'"),
  'for': ('for 变量 in 可迭代对象: …',
          '依次取出元素并执行循环体。遍历索引可用 range，同时取下标和值可用 enumerate。\n'
          '| total = 0\n'
          '| for x in [1, 2, 3]:\n'
          '|     total += x\n'
          '| total -> 6'),
  'while': ('while 条件: …',
            '每轮开始前判断条件。条件为真才执行循环体，初始为假时执行零次。while True 常配合 break 或 return 结束。\n'
            '| n = 0\n'
            '| while n < 3:\n'
            '|     n += 1\n'
            '| n -> 3'),
  'continue': ('continue',
               '跳过最内层循环本轮剩余语句。for 接着取下一个元素，while 重新检查条件。while 中使用时，确认该分支也能推进循环条件。\n'
               '| even = []\n'
               '| for x in [1, 2, 3, 4]:\n'
               '|     if x % 2:\n'
               '|         continue\n'
               '|     even.append(x)\n'
               '| even -> [2, 4]'),
  'break': ('break',
            '立即结束最内层循环，执行循环之后的代码。该循环若带有 else，会跳过 else。\n'
            '| visited = []\n'
            '| for x in [1, 2, 3, 4]:\n'
            '|     if x == 3:\n'
            '|         break\n'
            '|     visited.append(x)\n'
            '| visited -> [1, 2]'),
  'return': ('return 表达式',
             '立即退出当前函数，结束其中正在执行的循环，并把表达式的值交给调用者。单写 return 或执行到函数末尾时，返回 None。\n'
             '| def first_even(nums):\n'
             '|     for x in nums:\n'
             '|         if x % 2 == 0:\n'
             '|             return x\n'
             '| (first_even([1, 4, 6]), first_even([1, 3])) -> (4, None)'),
  '循环 else': ('for …: … else: … / while …: … else: …',
              'else 与 for 或 while 对齐。for 耗尽元素、while 条件变假时执行 else，零次循环也算正常结束。continue '
              '后若正常结束，仍执行 else。break、return 或异常使循环提前退出时，跳过 else。\n'
              '| def contains_two(nums):\n'
              '|     for x in nums:\n'
              '|         if x == 2:\n'
              '|             break\n'
              '|     else:\n'
              '|         return False\n'
              '|     return True\n'
              '| (contains_two([1, 2]), contains_two([1, 3]), contains_two([])) -> (True, '
              'False, False)\n'
              '| def finish(n):\n'
              '|     while n < 3:\n'
              '|         if n == 1:\n'
              '|             break\n'
              '|         n += 1\n'
              '|     else:\n'
              "|         return '条件变假'\n"
              "|     return '遇到 break'\n"
              "| (finish(0), finish(2), finish(3)) -> ('遇到 break', '条件变假', '条件变假')"),
  'pass': ('pass',
           '空操作。需要占一个语句位置时可用，例如暂未实现的函数体。执行后继续运行后续语句。\n'
           '| def placeholder():\n'
           '|     pass\n'
           '| placeholder() -> None')})]
