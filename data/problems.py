# -*- coding: utf-8 -*-
"""
题库。build.py 读取本文件生成 index.html。

一道题的字段：
    title     题名
    source    来源/题号，显示在题名右侧小字
    tag       可选，题名后的小标记，例："非 Hot100"
    note      一句话说明：输入是什么、要输出什么
    code      Python 答案，三引号原样写，关键行带中文注释

专题结构：
    {"id": "...", "name": "...",
     "problems": [...],     已录入答案的题，渲染成完整卡片
     "pending":  [(1, "两数之和"), ...],   待录入：(题号, 题名)
     "summary":  ["...", "..."]}   可选，专题收尾的小结

summary 在专题全部录完后补，渲染成题目下方一个浅蓝框：先一段话把每题
思路串起来，最后一段（自动标「核心」）点出这一类的共同思想。写两条最清楚，
只写一条也行；`反引号` 里的内容会渲染成等宽代码。

pending 里已经出现在 problems 中的题号会自动跳过，不用手动删。
录入一题 = 往 problems 里加一条，清单自动缩水。
"""

META = {
    "title": "算法机考开卷手册",
    "subtitle": "Python · Hot 100 · 按官方分类",
}

TOPICS = [{'id': 'hash',
  'name': '哈希',
  'problems': [{'title': '两数之和',
                'source': 'LC 1',
                'note': '在 nums 里找两个下标，使对应的数相加等于 target，返回这两个下标（答案唯一，同一个元素不能用两次）。',
                'example': 'nums = [2,7,11,15], target = 9  →  [1,0]（下标 0 的 2 加下标 1 的 '
                           '7；两个下标谁先谁后都算对）',
                'code': 'class Solution:\n'
                        '    def twoSum(self, nums, target):\n'
                        '        hash = {}                          # 键 = 见过的数字，值 = 它的下标\n'
                        '        for x in range(len(nums)):\n'
                        '            res = target - nums[x]         # 还差多少才凑成 target\n'
                        '            if res in hash:\n'
                        '                return [x, hash[res]]      # 差的那个见过，两个下标直接交\n'
                        '            else:\n'
                        '                hash[nums[x]] = x          # 没见过，把当前数字和坐标存进去'},
               {'title': '字母异位词分组',
                'source': 'LC 49',
                'note': '把 strs 里互为字母异位词的串分到同一组，返回所有组（组内顺序、组间顺序都随意）。',
                'example': 'strs = ["eat","tea","tan","ate","nat","bat"]  →  '
                           '[["eat","tea","ate"],["tan","nat"],["bat"]]',
                'code': 'from collections import defaultdict\n'
                        '\n'
                        'class Solution:\n'
                        '    def groupAnagrams(self, strs):\n'
                        '        d = defaultdict(list)              # 键 = 排好序的串，值 = '
                        '这一组的原串\n'
                        '        for i in strs:\n'
                        '            _ = "".join(sorted(i))         # 异位词排完序一模一样，拿它当组名\n'
                        '            d[_].append(i)                 # 组不存在时自动建空 list，直接塞\n'
                        '        return list(d.values())            # 只要各组，不要键',
                'tips': ['不用 `defaultdict` 也行：先 `if _ not in d: d[_] = []` 再 '
                         '`d[_].append(i)`，多写两行；`defaultdict(list)` 只是把「缺键先建空 '
                         'list」这一步替你做了。']},
               {'title': '最长连续序列',
                'source': 'LC 128',
                'note': '在 nums 里找最长的一段连续整数（值连续、位置不必相邻，重复的算一个），返回这段的长度；题目要求 O(n)，所以不能排序。',
                'example': 'nums = [100,4,200,1,3,2]  →  4（1,2,3,4 连成一串）',
                'code': 'class Solution:\n'
                        '    def longestConsecutive(self, nums):\n'
                        '        if not nums:                    # 空数组直接 0，否则下面 max 会炸\n'
                        '            return 0\n'
                        '        nums = set(nums)                # 去重，成员查询平均 O(1)\n'
                        '        hash = {}                       # 键 = 一段连续区的起点，值 = 这段多长\n'
                        '        for i in nums:\n'
                        '            if i - 1 in nums:           # 前面还有数，说明 i 不是起点，跳过\n'
                        '                continue\n'
                        '            a = 1                       # 从 i 开始往右数，先算它自己\n'
                        '            b = i\n'
                        '            while b + 1 in nums:\n'
                        '                b += 1\n'
                        '                a += 1\n'
                        '            hash[i] = a                 # 这一段以 i 打头，长度记成 a\n'
                        '        return max(list(hash.values()))',
                'tips': ['`max(list(hash.values()))` 里的 `list()` 可以省：`max` 直接吃 '
                         '`dict_values` 也行，写成 `max(hash.values())` 少一次拷贝，结果一样。']}],
  'summary': ['① 两数之和：一边走一边把见过的数记在本子上，每到一个新数就翻本子看「还差的那个」在不在，在就直接交答案——不用拿每个数去跟后面所有数试一遍。\n'
              '② 字母异位词分组：互为异位词的串，把字母排个序就长得一模一样，于是拿「排完序的串」当抽屉标签，原串往对应抽屉里一扔，最后把抽屉挨个倒出来就是答案。\n'
              '③ 最长连续序列：从头挨个往后数的话，同一段会被翻来覆去数很多遍；只从「前面没有邻居」的数开始数，每段就只数一次，数完把段长记下来取最大。',
              '共同点是用哈希表或集合加快重复查询：两数之和按补数查下标，异位词按排序后的字符串分组，最长连续序列只从段首扩展。哈希查询通常为平均 '
              'O(1)，不是所有处理都为 O(n)：异位词分组仍需逐串排序；最长连续序列虽有内层 while，但每个不同整数只属于一段，因此总计平均 O(n)。'],
  'pending': [(1, '两数之和'), (49, '字母异位词分组'), (128, '最长连续序列')]},
 {'id': 'two-pointers',
  'name': '双指针',
  'problems': [{'title': '移动零',
  'source': 'LC 283',
  'note': '把 nums 中的所有 0 移到末尾，同时保持非零元素原有顺序；直接修改 nums，不返回数组。',
  'example': 'nums = [0,1,0,3,12]  →  nums 变为 [1,3,12,0,0]（返回值是 None）',
  'code': 'class Solution:\n'
          '    def moveZeroes(self, nums):\n'
          '        l = 0                              # 下一个非零元素应放的位置\n'
          '        r = 0                              # 当前扫描的位置\n'
          '        n = len(nums)\n'
          '        while r < n:\n'
          '            if nums[r] != 0:               # 遇到非零数，放进前面的有效区\n'
          '                nums[l], nums[r] = nums[r], nums[l]  # 原地交换，保留非零数先后顺序\n'
          '                l += 1                     # 非零区扩大一位\n'
          '            r += 1                         # 不论是否为零，都继续向右扫描'},
 {'title': '盛最多水的容器',
 'source': 'LC 11',
 'note': '给定非负整数数组 height，每个下标对应一条竖线。选两条线和横轴构成容器，返回能盛的最大水量。容器不能倾斜。',
 'example': 'height = [1,8,6,2,5,4,8,3,7]  →  49（下标 1 和 8）；height = [1,1]  →  1',
 'code': 'class Solution:\n'
         '    def maxArea(self, height):\n'
         '        n = len(height)\n'
         '        l = 0\n'
         '        r = n - 1\n'
         '        ans = 0\n'
         '        while l < r:\n'
         '            area = min(height[r], height[l]) * (r - l)\n'
         '            ans = max(area, ans)\n'
         '            if height[l] <= height[r]:\n'
         '                l += 1                    # 左侧较短或等高，舍弃左端\n'
         '            else:\n'
         '                r -= 1                    # 右侧较短，舍弃右端\n'
         '        return ans',
 'tips': ['面积是两端较短的高度乘宽度。若左端较短，固定左端再把右端往里移，宽度会变小，高度也不会超过原左端，所以这些组合都不可能更好，可以直接舍弃左端。',
          '右端较短时同理。两端等高时任选一侧移动，原稿选择移动左端。时间 O(n)，额外空间 O(1)。']},
 {'title': '三数之和',
 'source': 'LC 15',
 'note': '给定整数数组 nums，返回由三个不同下标组成、元素和为 0 的所有三元组。按值去重，结果顺序不限。',
 'example': 'nums = [-1,0,1,2,-1,-4]  →  [[-1,-1,2],[-1,0,1]]；nums = [0,0,0,0]  →  [[0,0,0]]',
 'code': 'class Solution:\n'
         '    def threeSum(self, nums):\n'
         '        n = len(nums)\n'
         '        nums.sort()\n'
         '        ans = []\n'
         '        for i in range(n):\n'
         '            if nums[i] > 0:\n'
         '                break                    # 后面的数都为正，三数和不可能为 0\n'
         '            if i > 0 and nums[i-1] == nums[i]:\n'
         '                continue                 # 同一个首项只处理一次\n'
         '            l = i + 1\n'
         '            r = n - 1\n'
         '            while l < r:\n'
         '                s = nums[i] + nums[l] + nums[r]\n'
         '                if s < 0:\n'
         '                    l += 1               # 和偏小，换更大的左值\n'
         '                elif s > 0:\n'
         '                    r -= 1               # 和偏大，换更小的右值\n'
         '                else:\n'
         '                    ans.append([nums[i], nums[l], nums[r]])\n'
         '                    r -= 1\n'
         '                    l += 1\n'
         '                    while l < r and nums[l-1] == nums[l]:\n'
         '                        l += 1           # 跳过刚用过的左值\n'
         '                    while l < r and nums[r+1] == nums[r]:\n'
         '                        r -= 1           # 跳过刚用过的右值\n'
         '        return ans',
 'tips': ['排序后固定 nums[i]，只在它右边用双指针寻找另两个数。和偏小就增大左值，和偏大就减小右值。',
          '两层都要去重。外层跳过重复首项，内层命中后把两端都移动，再跳过相同值。sort() 会修改输入数组。',
          '总时间 O(n²)。双指针扫描只用 O(1) 额外空间，Python 的 sort() 可能使用 O(n) 辅助空间，答案另计。']},
 {'title': '接雨水',
 'source': 'LC 42',
 'note': '给定非负整数数组 height，每个元素是一根宽度为 1 的柱子高度。返回下雨后能接住的雨水总量。',
 'example': 'height = [0,1,0,2,1,0,1,3,2,1,2,1]  →  6；height = [2,0,2]  →  2；height = [1,2,3]  →  0',
 'code': 'class Solution:\n'
         '    def trap(self, height):\n'
         '        n = len(height)\n'
         '        l = 0\n'
         '        r = n - 1\n'
         '        ans = 0\n'
         '        max_l = 0\n'
         '        max_r = 0\n'
         '        while l <= r:\n'
         '            if max_l < max_r:\n'
         '                if height[l] > max_l:\n'
         '                    max_l = height[l]\n'
         '                else:\n'
         '                    ans += max_l - height[l]  # 左侧已见最高柱决定水位\n'
         '                l += 1\n'
         '            else:\n'
         '                if height[r] > max_r:\n'
         '                    max_r = height[r]\n'
         '                else:\n'
         '                    ans += max_r - height[r]  # 右侧已见最高柱决定水位\n'
         '                r -= 1\n'
         '        return ans',
 'tips': ['max_l 和 max_r 记录两边已经处理过的最高柱。左边的最高柱较矮时，右边已经有足够高的挡板，左指针这一格就能结算。右侧较矮或两边一样高时，按原稿结算右边。',
          '例如左侧已见最高柱为 2，右侧为 4，左指针当前柱高为 1，那么这格接 2-1 = 1 单位水。若当前柱反而高过左侧最高柱，这格不接水，只更新左侧最高柱。',
          '这里每轮结算一个位置，所以 l == r 时也要处理。和盛水容器不同，本题比较的是两侧已见最高值，并逐格累加。时间 O(n)，额外空间 O(1)。']}],
  'pending': [(283, '移动零'), (11, '盛最多水的容器'), (15, '三数之和'), (42, '接雨水')],
  'summary': ['① 移动零\u3000快指针扫数组，慢指针指向下一个非零元素的位置。\n'
   '② 盛最多水的容器\u3000先算当前面积，舍弃较矮一端。\n'
   '③ 三数之和\u3000排序后固定一个数，按和的大小移动两端，命中后跳过重复值。\n'
   '④ 接雨水\u3000比较两侧已见最高柱，先结算受较低水位限制的一侧。',
   '先想清楚移动指针时排除了哪些候选，或者确定了哪个位置的答案。容器比较当前两根柱，接雨水比较两侧已见最高柱。']},
 {'id': 'sliding-window',
  'name': '滑动窗口',
  'problems': [{'title': '无重复字符的最长子串',
  'source': 'LC 3',
  'note': '给定字符串 s，返回不含重复字符的最长连续子串的长度。',
  'example': 's = "abcabcbb"  →  3；s = "abba"  →  2；s = ""  →  0',
  'code': 'class Solution:\n'
          '    def lengthOfLongestSubstring(self, s):\n'
          '        n = len(s)\n'
          '        l, r = -1, 0\n'
          '        last = {}\n'
          '        ans = 0\n'
          '        while r < n:\n'
          '            if s[r] not in last:\n'
          '                last[s[r]] = r\n'
          '                ans = max(ans, r - l)\n'
          '            elif last[s[r]] > l:\n'
          '                l = last[s[r]]          # 把窗口内的旧重复字符移到边界之外\n'
          '                last[s[r]] = r\n'
          '            elif last[s[r]] < l:\n'
          '                last[s[r]] = r          # 旧位置在窗口之外，可以直接扩张\n'
          '                ans = max(ans, r - l)\n'
          '            r += 1\n'
          '        return ans',
  'tips': ['窗口是 (l, r]，l 本身不在窗口里。字典记录字符最近出现的位置。遇到窗口内的重复字符时，左边界右移，这一轮的窗口长度不会超过上一轮，所以无需更新 ans。',
           '原稿的 last[s[r]] == l 不会出现。每次把 l 改成某字符的旧位置，同一轮也把该字符的记录更新为 r，旧位置不会再留在字典里。时间 O(n)，额外空间 O(d)，d 是不同字符数。']},
 {'title': '找到字符串中所有字母异位词',
  'source': 'LC 438',
  'note': '给定字符串 s 和非空字符串 p，返回 s 中所有与 p 字符次数完全相同的子串的起始下标。',
  'example': 's = "cbaebabacd"，p = "abc"  →  [0,6]；s = "baa"，p = "aa"  →  [1]',
  'code': 'from collections import Counter\n'
          '\n'
          'class Solution:\n'
          '    def findAnagrams(self, s, p):\n'
          '        cnt = Counter(p)\n'
          '        ans = []\n'
          '        l = 0\n'
          '        for i in range(len(s)):\n'
          '            cnt[s[i]] -= 1\n'
          '            while cnt[s[i]] < 0:        # 右端字符超额，左端逐个退出\n'
          '                cnt[s[l]] += 1\n'
          '                l += 1\n'
          '            if i - l + 1 == len(p):\n'
          '                ans.append(l)\n'
          '        return ans',
  'tips': ['cnt[c] 表示 p 还允许窗口放入几个 c。每次只有右端新加入的字符可能使余额变负。恢复非负后，所有字符都没超额，窗口长度恰好等于 len(p) 时，字符次数就一定相同。',
           '左右端各走一遍。时间 O(len(s)+len(p))，额外空间为计数表大小，不计答案。']}],
  'pending': [(3, '无重复字符的最长子串'), (438, '找到字符串中所有字母异位词')],
  'summary': ['最长无重复子串记录上次出现的位置，找到异位词记录每种字符的余额。', '先明确窗口里允许什么，再决定左端何时移动和答案何时记录。']},
 {'id': 'substring',
  'name': '子串',
  'problems': [{'title': '和为 K 的子数组',
  'source': 'LC 560',
  'note': '给定非空整数数组 nums 和整数 k，返回和恰好等于 k 的非空连续子数组个数。',
  'example': 'nums = [1,1,1]，k = 2  →  2；nums = [1,-1,0]，k = 0  →  3',
  'code': 'from collections import defaultdict\n'
          '\n'
          'class Solution:\n'
          '    def subarraySum(self, nums, k):\n'
          '        n = len(nums)\n'
          '        pre = [0] * n\n'
          '        pre[0] = nums[0]\n'
          '        counts = defaultdict(int)\n'
          '        counts[0] = 1                  # 数组之前有一个和为 0 的空前缀\n'
          '        ans = 0\n'
          '        for i in range(1, n):\n'
          '            pre[i] = pre[i-1] + nums[i]\n'
          '        for i in range(n):\n'
          '            ans += counts[pre[i] - k]  # 只查当前下标之前的前缀\n'
          '            counts[pre[i]] += 1\n'
          '        return ans',
  'tips': ['pre[i] 包含 nums[i]。当前前缀减去某个旧前缀等于 k，就确定了一个以 i 结尾的子数组。空前缀可计入从下标 0 开始的答案。',
           '先查询再登记，避免 k 为 0 时把当前前缀和自己相减算成空子数组。时间 O(n)，额外空间 O(n)。']},
 {'title': '滑动窗口最大值',
  'source': 'LC 239',
  'note': '给定数组 nums 和窗口长度 k，返回窗口从左到右移动时每个窗口的最大值。',
  'example': 'nums = [1,3,-1,-3,5,3,6,7]，k = 3  →  [3,3,5,5,6,7]；nums = [2,2,1]，k = 2  →  [2,2]',
  'code': 'from collections import deque\n'
          '\n'
          'class Solution:\n'
          '    def maxSlidingWindow(self, nums, k):\n'
          '        q = deque()\n'
          '        n = len(nums)\n'
          '        ans = [0] * (n - k + 1)\n'
          '        for r in range(n):\n'
          '            l = r - k + 1\n'
          '            while q and q[0] == l - 1:\n'
          '                q.popleft()            # 删除刚离开窗口的队首\n'
          '            while q and nums[r] > nums[q[-1]]:\n'
          '                q.pop()                # 新值更大，又比队尾更晚过期\n'
          '            q.append(r)\n'
          '            if l >= 0:\n'
          '                ans[l] = nums[q[0]]    # 满 k 个元素后才记录\n'
          '        return ans',
  'tips': ['队列存下标，队首到队尾的值非递增。比如队尾有 4、2，新值是 3，就弹掉 2 并把 3 放到 4 后面。相同值都保留，较早的那个到期时从队首删除。',
           '每轮左边界只向右走一格，所以本轮刚过期的下标是 l-1。每个下标至多进出队各一次。时间 O(n)，辅助空间 O(k)。']},
 {'title': '最小覆盖子串',
  'source': 'LC 76',
  'note': '返回 s 中能覆盖 t 每种字符及其出现次数的最短连续子串。找不到时返回空字符串，题目保证 t 非空。',
  'example': 's = "ADOBECODEBANC"，t = "ABC"  →  "BANC"；s = "a"，t = "aa"  →  ""',
  'code': 'from collections import Counter\n'
          '\n'
          'class Solution:\n'
          '    def minWindow(self, s, t):\n'
          '        r, l = 0, 0\n'
          '        n = len(s)\n'
          '        start = 0\n'
          '        le = 10**9\n'
          '        cnt_base = Counter(t)\n'
          '        cnt_now = Counter()\n'
          '        target = len(cnt_base)\n'
          '        valid = 0\n'
          '        while r < n:\n'
          '            if s[r] in cnt_base:\n'
          '                cnt_now[s[r]] += 1\n'
          '                if cnt_now[s[r]] == cnt_base[s[r]]:\n'
          '                    valid += 1\n'
          '            while valid == target:\n'
          '                if s[l] in cnt_base:\n'
          '                    cnt_now[s[l]] -= 1\n'
          '                    if cnt_now[s[l]] < cnt_base[s[l]]:\n'
          '                        valid -= 1\n'
          '                if r - l + 1 <= le:\n'
          '                    le = r - l + 1     # l 还未移动，记录的是退出前的窗口\n'
          '                    start = l\n'
          '                l += 1\n'
          '            r += 1\n'
          '        if le > n:\n'
          '            return ""\n'
          '        return s[start:start+le]',
  'tips': ['valid 统计达到要求的字符种类数。例如 t = "AA"，窗口内有两个 A 时才把 A 算为满足，第三个 A 不再增加 valid。',
           '进入 while 时 [l, r] 已经覆盖 t。虽然先扣掉左端字符的计数，记录时用的仍是尚未移动的 l，所以记的是移除前的合法窗口。时间 O(len(s)+len(t))，计数表空间取决于 t '
           '的字符种类，不计返回的子串。']}],
  'pending': [(560, '和为 K 的子数组'), (239, '滑动窗口最大值'), (76, '最小覆盖子串')],
  'summary': ['和为 K 用前缀差统计次数。滑动窗口最大值用单调队列保留还可能成为最大值的下标。最小覆盖用字符次数决定什么时候收缩。', '子数组和可以因负数变小，和为 K 用前缀表。窗口最大值和字符覆盖各有能随左右端更新的状态。']},
 {'id': 'array',
  'name': '普通数组',
  'problems': [{'title': '最大子数组和',
  'source': 'LC 53',
  'note': '给定非空整数数组 nums，返回所有非空连续子数组中的最大和。',
  'example': 'nums = [-2,1,-3,4,-1,2,1,-5,4]  →  6（[4,-1,2,1]）；nums = [-3,-1,-2]  →  -1',
  'code': 'class Solution:\n'
          '    def maxSubArray(self, nums):\n'
          '        n = len(nums)\n'
          '        prex = 0\n'
          '        min_prex = 0\n'
          '        ans = -10**9\n'
          '        for i in range(n):\n'
          '            prex += nums[i]\n'
          '            min_prex = min(prex, min_prex)\n'
          '            if prex == min_prex:\n'
          '                ans = max(nums[i], ans)    # 当前差为 0 时不能把空段当答案\n'
          '            else:\n'
          '                ans = max(ans, prex - min_prex)\n'
          '        return ans',
  'tips': ['用当前前缀和减去最小前缀和来取较大的区间和。原稿先更新最小前缀，若两者相等，这一轮就不能得到正的区间和，只拿当前单元素更新。',
           '只要出现过正和，后面非正的区间就不会刷新最大值。若所有元素都非正，单元素分支会取到最大的那个数。时间 O(n)，额外空间 O(1)。']},
 {'title': '合并区间',
  'source': 'LC 56',
  'note': '给定非空的闭区间数组，合并所有重叠区间，返回合并后的区间。端点相接也算重叠。',
  'example': 'intervals = [[1,3],[2,6],[8,10],[15,18]]  →  [[1,6],[8,10],[15,18]]；[[1,4],[4,5]]  →  [[1,5]]',
  'code': 'class Solution:\n'
          '    def merge(self, intervals):\n'
          '        intervals = sorted(intervals, key=lambda x: x[0])\n'
          '        ans = []\n'
          '        start, end = intervals[0]\n'
          '        for i in range(1, len(intervals)):\n'
          '            if intervals[i][0] > end:\n'
          '                ans.append([start, end])   # 后面的起点更靠右，可以收尾\n'
          '                start = intervals[i][0]\n'
          '                end = intervals[i][1]\n'
          '            else:\n'
          '                end = max(end, intervals[i][1])\n'
          '        ans.append([start, end])           # 收集最后一个区间\n'
          '        return ans',
  'tips': ['按起点排序后，只需要维护当前区间的左右端点。遇到重叠时取较大的右端，避免把包含在里面的短区间当作新右端。时间 O(n log n)，排序和新列表额外空间 O(n)。']},
 {'title': '轮转数组',
  'source': 'LC 189',
  'note': '给定非空数组 nums 和非负整数 k，把数组原地向右轮转 k 步，函数返回 None。',
  'example': 'nums = [1,2,3,4,5,6,7]，k = 3  →  nums 变为 [5,6,7,1,2,3,4]，返回 None',
  'code': 'class Solution:\n'
          '    def rotate(self, nums, k):\n'
          '        def reverse(x, i, j):\n'
          '            while i < j:\n'
          '                x[i], x[j] = x[j], x[i]\n'
          '                i += 1\n'
          '                j -= 1\n'
          '\n'
          '        n = len(nums)\n'
          '        k %= n\n'
          '        reverse(nums, 0, n - 1)           # 整段反转，尾部 k 项来到前面\n'
          '        reverse(nums, 0, k - 1)           # 恢复前 k 项的原相对顺序\n'
          '        reverse(nums, k, n - 1)           # 恢复剩余项的原相对顺序',
  'tips': ['三次反转都直接交换原数组里的元素。k 先取模。k 为 0 时第一段为空，整段最终会反转回来。时间 O(n)，额外空间 O(1)。']},
 {'title': '除自身以外数组的乘积',
  'source': 'LC 238',
  'note': '返回数组 ans，其中 ans[i] 等于 nums 除下标 i 外其余元素的乘积。要求 O(n) 时间，不能用除法。',
  'example': 'nums = [1,2,3,4]  →  [24,12,8,6]；nums = [-1,1,0,-3,3]  →  [0,0,9,0,0]',
  'code': 'class Solution:\n'
          '    def productExceptSelf(self, nums):\n'
          '        n = len(nums)\n'
          '        pro = [1] * n\n'
          '        ans = [1] * n\n'
          '        pre = 1\n'
          '        for i in range(n - 1, 0, -1):\n'
          '            pro[i-1] = pro[i] * nums[i]   # i-1 右边所有数的乘积\n'
          '        for i in range(n):\n'
          '            ans[i] = pre * pro[i]\n'
          '            pre *= nums[i]               # 先算答案，再把当前位置算进前缀\n'
          '        return ans',
  'tips': ['pro[i] 是严格位于 i 右边的乘积，pre 在计算 ans[i] 时是严格位于 i 左边的乘积。空的一边乘积是 1。时间 O(n)，不计结果数组，后缀表额外空间 O(n)。']},
 {'title': '缺失的第一个正数',
  'source': 'LC 41',
  'note': '给定未排序的整数数组，返回数组里没出现过的最小正整数。要求 O(n) 时间和 O(1) 额外空间。',
  'example': 'nums = [3,4,-1,1]  →  2；nums = [1,1]  →  2；nums = [1,2,3]  →  4',
  'code': 'class Solution:\n'
          '    def firstMissingPositive(self, nums):\n'
          '        n = len(nums)\n'
          '        l = 0\n'
          '        while l < n:\n'
          '            x = nums[l]\n'
          '            if x == l + 1 or x > n or x <= 0 or nums[x-1] == x:\n'
          '                l += 1                    # 已归位、超范围，或目标位置已有同值\n'
          '            else:\n'
          '                nums[l], nums[x-1] = nums[x-1], nums[l]\n'
          '        for i in range(n):\n'
          '            if nums[i] != i + 1:\n'
          '                return i + 1\n'
          '        return n + 1',
  'tips': ['有效值 x 应该放到下标 x-1。短路判断先排除越界值，再访问 nums[x-1]。目标位已有同值时必须跳过，否则重复值会让交换停不下来。',
           '每次实际交换至少固定一个新位置。扫描指针最多前进 n 次，交换也最多 n 次。时间 O(n)，额外空间 O(1)。代码会重新排列输入数组。']}],
  'pending': [(53, '最大子数组和'),
              (56, '合并区间'),
              (189, '轮转数组'),
              (238, '除自身以外数组的乘积'),
              (41, '缺失的第一个正数')],
  'summary': ['最大子数组和看前缀差。合并区间排序后维护右端。轮转用三次反转。乘积用左右两侧的积。缺失正数把值放回对应下标。', '写数组题时先分清索引是位置还是值的目标位置。原地题要直接更新传入的对象。']},
 {'id': 'matrix',
  'name': '矩阵',
  'problems': [{'title': '矩阵置零',
  'source': 'LC 73',
  'note': '给定非空矩阵，只要原矩阵有一个 0，就把它所在行和列全部置 0。原地修改，返回 None。',
  'example': 'matrix = [[1,1,1],[1,0,1],[1,1,1]]  →  matrix 变为 [[1,0,1],[0,0,0],[1,0,1]]，返回 None',
  'code': 'class Solution:\n'
          '    def setZeroes(self, matrix):\n'
          '        m, n = len(matrix), len(matrix[0])\n'
          '        row_zero = False\n'
          '        line_zero = False\n'
          '        for i in range(n):\n'
          '            if matrix[0][i] == 0:\n'
          '                row_zero = True\n'
          '        for i in range(m):\n'
          '            if matrix[i][0] == 0:\n'
          '                line_zero = True\n'
          '\n'
          '        for i in range(1, m):\n'
          '            for j in range(1, n):\n'
          '                if matrix[i][j] == 0:\n'
          '                    matrix[i][0] = 0    # 用首列标记行\n'
          '                    matrix[0][j] = 0    # 用首行标记列\n'
          '        for j in range(1, n):\n'
          '            if matrix[0][j] == 0:\n'
          '                for i in range(1, m):\n'
          '                    matrix[i][j] = 0\n'
          '        for i in range(1, m):\n'
          '            if matrix[i][0] == 0:\n'
          '                for j in range(1, n):\n'
          '                    matrix[i][j] = 0\n'
          '\n'
          '        if row_zero:\n'
          '            for j in range(n):\n'
          '                matrix[0][j] = 0\n'
          '        if line_zero:\n'
          '            for i in range(m):\n'
          '                matrix[i][0] = 0',
  'tips': ['首行和首列要兼作标记，所以先记下它们自己是否原本就有 0，最后再处理它们。扫描和置零分开，避免把刚写入的 0 当作新的置零来源。时间 O(m × n)，额外空间 O(1)。']},
 {'title': '螺旋矩阵',
  'source': 'LC 54',
  'note': '给定矩形矩阵，从左上角开始顺时针向内读取，返回访问到的元素列表。',
  'example': 'matrix = [[1,2,3],[4,5,6]]  →  [1,2,3,6,5,4]；matrix = [[1],[2],[3]]  →  [1,2,3]',
  'code': 'class Solution:\n'
          '    def spiralOrder(self, matrix):\n'
          '        if not matrix:\n'
          '            return []\n'
          '        l, r, t, b = 0, len(matrix[0]) - 1, 0, len(matrix) - 1\n'
          '        res = []\n'
          '        while True:\n'
          '            for i in range(l, r + 1):\n'
          '                res.append(matrix[t][i])   # 上边，从左往右\n'
          '            t += 1\n'
          '            if t > b:\n'
          '                break\n'
          '            for i in range(t, b + 1):\n'
          '                res.append(matrix[i][r])   # 右边，从上往下\n'
          '            r -= 1\n'
          '            if l > r:\n'
          '                break\n'
          '            for i in range(r, l - 1, -1):\n'
          '                res.append(matrix[b][i])   # 下边，从右往左\n'
          '            b -= 1\n'
          '            if t > b:\n'
          '                break\n'
          '            for i in range(b, t - 1, -1):\n'
          '                res.append(matrix[i][l])   # 左边，从下往上\n'
          '            l += 1\n'
          '            if l > r:\n'
          '                break\n'
          '        return res',
  'tips': ['l、r、t、b 是未读取区域的四条闭区间边界。每走完一条边立刻收缩并检查，最后只剩一行或一列时就不会再读一遍。时间 O(m × n)，不计结果的额外空间 O(1)。']},
 {'title': '旋转图像',
  'source': 'LC 48',
  'note': '给定 n × n 方阵，将它原地顺时针旋转 90°。不另建矩阵，返回 None。',
  'example': 'matrix = [[1,2,3],[4,5,6],[7,8,9]]  →  matrix 变为 [[7,4,1],[8,5,2],[9,6,3]]，返回 None',
  'code': 'class Solution:\n'
          '    def rotate(self, matrix):\n'
          '        n = len(matrix)\n'
          '        for i in range(n):\n'
          '            for j in range(i + 1, n):\n'
          '                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]\n'
          '        for row in matrix:\n'
          '            row.reverse()               # 转置后再左右翻转每行',
  'tips': ['原位置 (i, j) 先经过转置到 (j, i)，再经过行内反转到 (j, n-1-i)。这与附件里的坐标映射相同。转置只遍历主对角线一侧，每对元素交换一次。时间 O(n²)，额外空间 O(1)。'],
  'remarks': [{'title': '备注 · 用新矩阵理解坐标映射',
               'note': '原稿把旧位置 (i, j) 直接写入新位置 (j, n-1-i)，旋转方向正确。matrix[:] 能更新调用者看到的列表，但已额外分配了 n × n '
                       '的矩阵。下面保留作坐标映射演示，提交时用上面的原地写法。',
               'code': 'class Solution:\n'
                       '    def rotate(self, matrix):\n'
                       '        n = len(matrix)\n'
                       '        matrix_new = [[0] * n for _ in range(n)]\n'
                       '        for i in range(n):\n'
                       '            for j in range(n):\n'
                       '                matrix_new[j][n - i - 1] = matrix[i][j]\n'
                       '        matrix[:] = matrix_new'}]},
 {'title': '搜索二维矩阵 II',
  'source': 'LC 240',
  'note': '给定非空矩阵，每行从左到右非递减，每列从上到下非递减。判断目标值 target 是否存在。',
  'example': 'matrix = [[1,4,7],[2,5,8],[3,6,9]]，target = 6  →  True；target = 10  →  False',
  'code': 'class Solution:\n'
          '    def searchMatrix(self, matrix, target):\n'
          '        m, n = len(matrix), len(matrix[0])\n'
          '        line, row = 0, n - 1\n'
          '        while line <= m - 1 and row >= 0:\n'
          '            if target < matrix[line][row]:\n'
          '                row -= 1                 # 当前列往下只会更大，排除这一列\n'
          '            elif target > matrix[line][row]:\n'
          '                line += 1                # 当前行往左只会更小，排除这一行\n'
          '            else:\n'
          '                return True\n'
          '        return False',
  'tips': ['从右上角开始，当前值过大就左移，过小就下移。line 是行下标，row 是列下标。每步排除一行或一列，时间 O(m+n)，额外空间 O(1)。',
           '和二分专题的 LC 74 不同，本题相邻两行的值域可以重叠，所以不能先按一行的首尾锁定唯一候选行。']}],
  'pending': [(73, '矩阵置零'), (54, '螺旋矩阵'), (48, '旋转图像'), (240, '搜索二维矩阵 II')],
  'summary': ['矩阵置零先做标记再修改。螺旋读取每走一边就更新边界。旋转图像用转置和行内反转。矩阵搜索从右上角逐步排除行列。', '先对照题意确认是否要原地改、是否能开新矩阵，以及行和列分别有哪些顺序保证。']},
 {'id': 'linked-list',
  'name': '链表',
  'problems': [{'title': '相交链表',
  'source': 'LC 160',
  'note': '给定两个无环单链表，返回它们共享的第一个节点。不相交时返回 None。',
  'example': 'A = [4,1,8,4,5]，B = [5,6,1,8,4,5]，从第一个 8 开始共用同一段节点  →  返回那个 8 的节点；A = [1]，B = [1]（两个独立节点）  →  None',
  'code': 'class Solution:\n'
          '    def getIntersectionNode(self, headA, headB):\n'
          '        p, q = headA, headB\n'
          '        while True:\n'
          '            if p == q:\n'
          '                return p              # 同一个节点，或同时为 None\n'
          '            p = p.next if p else headB\n'
          '            q = q.next if q else headA',
  'tips': ['两个指针走到空位就换到另一条链表。若有公共尾段，两个指针换头后会走过相同的总步数，到达同一个交点。若没有，最终同时到 None。',
           '判题提供的 ListNode 按对象身份比较。值相等不代表相交，也不能只靠两条值序列构造相交用例。时间 O(m+n)，额外空间 O(1)。']},
 {'title': '反转链表',
  'source': 'LC 206',
  'note': '给定单链表头节点 head，原地反转链表的指向，返回新的头节点。',
  'example': 'head = [1,2,3]  →  [3,2,1]；head = []  →  []',
  'code': 'class Solution:\n'
          '    def reverseList(self, head):\n'
          '        cur, pre = head, None\n'
          '        while cur:\n'
          '            tmp = cur.next            # 改指针前先存好剩余链表的入口\n'
          '            cur.next = pre\n'
          '            pre = cur\n'
          '            cur = tmp\n'
          '        return pre                    # 最后处理的节点就是新头',
  'tips': ['pre 指向已反转部分的头，cur 指向下一个待处理节点。原来的头第一次反转后指向 None，最后成为尾节点。时间 O(n)，额外空间 O(1)。']},
 {'title': '回文链表',
  'source': 'LC 234',
  'note': '判断单链表的节点值从前向后与从后向前是否相同。',
  'example': 'head = [1,2,2,1]  →  True；head = [1,2,3]  →  False；head = [1,2,1]  →  True',
  'code': 'import sys\n'
          '\n'
          'if sys.getrecursionlimit() < 51000:\n'
          '    sys.setrecursionlimit(51000)\n'
          '\n'
          'class Solution:\n'
          '    def isPalindrome(self, head):\n'
          '        def reverse(cur, pre):\n'
          '            if not cur:\n'
          '                self.ans = pre        # 已走到原链尾，pre 是反转后的头\n'
          '                return\n'
          '            reverse(cur.next, cur)\n'
          '            cur.next = pre            # 在递归返回时改指针\n'
          '            return\n'
          '\n'
          '        slow = fast = head\n'
          '        while fast and fast.next:\n'
          '            slow = slow.next\n'
          '            fast = fast.next.next\n'
          '\n'
          '        reverse(slow, None)\n'
          '        a = head\n'
          '        while self.ans:\n'
          '            if self.ans.val == a.val:\n'
          '                self.ans = self.ans.next\n'
          '                a = a.next\n'
          '            else:\n'
          '                return False\n'
          '        return True',
  'tips': ['快指针每次走两步，慢指针每次走一步。偶数长度时 slow 指向后半段的首节点，奇数长度时指向正中间，最后一次比较会用同一个中点的值。',
           '原稿会反转后半段，比较结束后不恢复链表。时间 O(n)，反转用递归栈，额外空间 O(n)。',
           '题面允许长链。运行这段代码时，仅在当前解释器的递归上限不足时调高它。']},
 {'title': '环形链表',
  'source': 'LC 141',
  'note': '判断沿 next 一直走是否会回到已访问过的节点。',
  'example': 'head = [3,2,0,-4]，pos = 1  →  True；head = [1]，pos = -1  →  False',
  'code': 'class Solution:\n'
          '    def hasCycle(self, head):\n'
          '        cur = head\n'
          '        steps = 0\n'
          '        while cur:\n'
          '            cur = cur.next\n'
          '            steps += 1\n'
          '            if steps > 10000:\n'
          '                return True            # 超过题目允许的节点数，必然走过重复节点\n'
          '        return False',
  'tips': ['题目保证最多 10,000 个节点。无环一定在这一步数以内走到 None，有环会继续走到第 10,001 步。pos 是判题用的环入口下标，-1 表示无环，方法只接收 head。',
           '这份写法依赖题目的长度上限。放到任意长度的链表上，超过 10,000 个节点的无环链也会被误判。设 B 是题目给定的节点上限，最坏时间 O(B)，额外空间 O(1)。']},
 {'title': '环形链表 II',
  'source': 'LC 142',
  'note': '返回环开始的节点，无环时返回 None。',
  'example': 'head = [3,2,0,-4]，pos = 1  →  返回下标 1、值为 2 的节点；head = [1]，pos = -1  →  None',
  'code': 'class Solution:\n'
          '    def detectCycle(self, head):\n'
          '        seen = set()\n'
          '        cur = head\n'
          '        while cur:\n'
          '            if cur not in seen:\n'
          '                seen.add(cur)          # 保存节点对象\n'
          '            else:\n'
          '                return cur             # 第一次重复访问的就是入环点\n'
          '            cur = cur.next\n'
          '        return None',
  'tips': ['从头走到环入口后，会先绕环一整圈，再次抵达入口。集合记录的是节点身份，相同值的不同节点可以同时存在。时间 O(n)，额外空间 O(n)。']},
 {'title': '合并两个有序链表',
  'source': 'LC 21',
  'note': '把两个非递减单链表合并为一条非递减链表，返回合并后的头节点。',
  'example': 'list1 = [1,2,4]，list2 = [1,3,4]  →  [1,1,2,3,4,4]；list1 = []，list2 = [0]  →  [0]',
  'code': 'class Solution:\n'
          '    def mergeTwoLists(self, list1, list2):\n'
          '        left, right = list1, list2\n'
          '        tail = ListNode()\n'
          '        dummy = tail\n'
          '        while left and right:\n'
          '            if left.val <= right.val:\n'
          '                tail.next = left\n'
          '                left = left.next\n'
          '                tail = tail.next\n'
          '            else:\n'
          '                tail.next = right\n'
          '                right = right.next\n'
          '                tail = tail.next\n'
          '        if left:\n'
          '            tail.next = left           # 一条耗尽后，接上另一条的剩余部分\n'
          '        if right:\n'
          '            tail.next = right\n'
          '        return dummy.next',
  'tips': ['dummy 固定留在结果头之前，tail 随着接入节点向后走。合并直接复用原节点。时间 O(m+n)，额外空间 O(1)。ListNode 由判题平台提供。']},
 {'title': '两数相加',
  'source': 'LC 2',
  'note': '两个非空链表分别表示非负整数，每个节点是一位数字，最低位在链表头。按同样的逆序方式返回两数之和。',
  'example': 'l1 = [2,4,3]，l2 = [5,6,4]  →  [7,0,8]；l1 = [9]，l2 = [1]  →  [0,1]',
  'code': 'class Solution:\n'
          '    def addTwoNumbers(self, l1, l2, s=0):\n'
          '        if l1 is None and l2 is None and s == 0:\n'
          '            return None\n'
          '        if l1:\n'
          '            s += l1.val\n'
          '            l1 = l1.next\n'
          '        if l2:\n'
          '            s += l2.val\n'
          '            l2 = l2.next\n'
          '        return ListNode(s % 10, self.addTwoNumbers(l1, l2, s // 10))',
  'tips': ['进入递归时 s 是上一位的进位，加上当前两位后，s % 10 写入新节点，s // 10 传给下一层。两条链都走完仍有进位时，还要创建一个节点。',
           '时间和递归额外空间均为 O(max(m,n))。输出使用新建节点。']},
 {'title': '删除链表的倒数第 N 个结点',
  'source': 'LC 19',
  'note': '给定非空链表和合法的 n，删除倒数第 n 个节点并返回更新后的头。',
  'example': 'head = [1,2,3,4,5]，n = 2  →  [1,2,3,5]；head = [1]，n = 1  →  []',
  'code': 'class Solution:\n'
          '    def removeNthFromEnd(self, head, n):\n'
          '        a, b = head, head\n'
          '        if head:\n'
          '            x = 0\n'
          '        else:\n'
          '            x = -1\n'
          '        while a:\n'
          '            a = a.next\n'
          '            x += 1\n'
          '\n'
          '        m = x - n                     # 要删除节点的下标，从 0 开始\n'
          '        if m == 0:\n'
          '            return head.next           # 删头时直接返回新头\n'
          '        elif m == x - 1:\n'
          '            k = 1\n'
          '            while k < x - 1:\n'
          '                head = head.next\n'
          '                k += 1\n'
          '            head.next = None           # 删尾时把倒数第二个节点设为新尾\n'
          '            return b\n'
          '        else:\n'
          '            k = 1\n'
          '            while k < x - n:\n'
          '                head = head.next\n'
          '                k += 1\n'
          '            head.next = head.next.next\n'
          '            return b',
  'tips': ['先算长度 x，再把倒数第 n 个换成正向下标 x-n。删头优先判断，所以单节点链表也能正确返回 None。其他情况先走到要删除节点的前一个位置。',
           '原稿保留了删头、删尾、删中间的三个分支。题目保证链表非空且 n 合法。时间 O(x)，额外空间 O(1)。']},
 {'title': '两两交换链表中的节点',
  'source': 'LC 24',
  'note': '把链表中相邻的两个节点成对交换，返回新头。最后剩一个节点时保留原位。',
  'example': 'head = [1,2,3,4,5]  →  [2,1,4,3,5]；head = []  →  []',
  'code': 'class Solution:\n'
          '    def swapPairs(self, head):\n'
          '        dummy = ListNode(0)\n'
          '        dummy.next = head\n'
          '        temp = dummy\n'
          '        while temp.next and temp.next.next:\n'
          '            node1 = temp.next\n'
          '            node2 = temp.next.next\n'
          '            temp.next = node2          # 前一段接到这一对的新头\n'
          '            node1.next = node2.next   # 原第一节点接到下一对\n'
          '            node2.next = node1\n'
          '            temp = node1               # 移到这一对的新尾\n'
          '        return dummy.next',
  'tips': ['每轮同时处理两个节点。虚拟头让第一对和后面的对使用相同的接线方式。改的是 next 指针。时间 O(n)，额外空间 O(1)。']},
 {'title': 'K 个一组翻转链表',
  'source': 'LC 25',
  'note': '每 k 个节点为一组，原地反转各组并返回新头。末尾不足 k 个节点时保持原顺序。',
  'example': 'head = [1,2,3,4,5]，k = 2  →  [2,1,4,3,5]；k = 3  →  [3,2,1,4,5]',
  'code': 'import sys\n'
          '\n'
          'if sys.getrecursionlimit() < 6000:\n'
          '    sys.setrecursionlimit(6000)\n'
          '\n'
          'class Solution:\n'
          '    def reverseKGroup(self, head, k):\n'
          '        x = 1\n'
          '        a = head\n'
          '        while x < k and a:\n'
          '            a = a.next\n'
          '            x += 1\n'
          '        if not a:\n'
          '            return head                # 剩余节点不足 k 个\n'
          '\n'
          '        c = a.next                     # 先保存下一组的头\n'
          '        prev, cur = None, head\n'
          '        for _ in range(k):\n'
          '            nxt = cur.next\n'
          '            cur.next = prev\n'
          '            prev = cur\n'
          '            cur = nxt\n'
          '        head.next = self.reverseKGroup(c, k)  # 原组头成了组尾\n'
          '        return prev',
  'tips': ['先检查这一组是否满 k 个，再改指针。反转后 prev 是新组头，原来的 head 变成尾，用它接上下一个递归结果。',
           '时间 O(n)，递归深度 O(1+n/k)。k = 1 时仍然按原写法逐节点递归。',
           '题面允许长链。运行这段代码时，仅在当前解释器的递归上限不足时调高它。']},
 {'title': '随机链表的复制',
  'source': 'LC 138',
  'note': '每个节点除了 next，还带有可指向任意原节点或 None 的 random。返回深拷贝的头，复制出来的指针都指向新节点或 None。',
  'example': 'head = [[7,null],[13,0]]  →  [[7,null],[13,0]]（新节点）；每项为 [值, random 指向的下标]',
  'code': 'import sys\n'
          '\n'
          'if sys.getrecursionlimit() < 2000:\n'
          '    sys.setrecursionlimit(2000)\n'
          '\n'
          'class Solution:\n'
          '    def __init__(self):\n'
          '        self.hash = {}\n'
          '\n'
          '    def copyRandomList(self, head):\n'
          '        if not head:\n'
          '            return None\n'
          '        if head not in self.hash:\n'
          '            new_head = Node(head.val)\n'
          '            self.hash[head] = new_head       # 先登记，再递归处理两条边\n'
          '            new_head.next = self.copyRandomList(head.next)\n'
          '            new_head.random = self.copyRandomList(head.random)\n'
          '        return self.hash[head]',
  'tips': ['字典将每个原节点映射到一个新节点。random 可能回到自己或已经访问过的节点，先登记可以避免重复构造和无限递归。',
           '独立复制时使用新的 Solution 实例。同一个实例重复传入同一原节点会命中缓存。时间和额外空间均为 O(n)。带 random 的 Node 定义见附录。',
           '题面允许长链。运行这段代码时，仅在当前解释器的递归上限不足时调高它。']},
 {'title': '排序链表',
  'source': 'LC 148',
  'note': '将链表按节点值升序排序，返回排序后的头节点。',
  'example': 'head = [4,2,1,3]  →  [1,2,3,4]；head = []  →  []',
  'code': 'class Solution:\n'
          '    def sortList(self, head):\n'
          '        nodes = []\n'
          '        cur = head\n'
          '        while cur:\n'
          '            nodes.append(cur)          # 保存节点引用\n'
          '            cur = cur.next\n'
          '\n'
          '        new_nodes = sorted(nodes, key=lambda x: x.val)\n'
          '        dummy = ListNode()\n'
          '        p = dummy\n'
          '        for node in new_nodes:\n'
          '            p.next = node\n'
          '            p = p.next\n'
          '        p.next = None                  # 清掉末节点旧指针\n'
          '        return dummy.next',
  'tips': ['先收集原节点，再按值排序，最后重连。必须把新的尾节点指向 None，否则可能带上旧节点，甚至形成环。',
           '时间 O(n log n)，额外空间 O(n)。题面的常数额外空间是进阶要求，这份原解法使用了列表。']},
 {'title': '合并 K 个升序链表',
  'source': 'LC 23',
  'note': '给定 k 条非递减链表，合并成一条非递减链表并返回新头。',
  'example': 'lists = [[1,4,5],[1,3,4],[2,6]]  →  [1,1,2,3,4,4,5,6]；lists = []  →  []',
  'code': 'class Solution:\n'
          '    def mergeKLists(self, lists):\n'
          '        def merge(l1, l2):\n'
          '            dummy = ListNode()\n'
          '            cur = dummy\n'
          '            while l1 and l2:\n'
          '                if l1.val < l2.val:\n'
          '                    cur.next = l1\n'
          '                    l1 = l1.next\n'
          '                else:\n'
          '                    cur.next = l2\n'
          '                    l2 = l2.next\n'
          '                cur = cur.next\n'
          '            cur.next = l1 if l1 else l2\n'
          '            return dummy.next\n'
          '\n'
          '        n = len(lists)\n'
          '        mid = n // 2\n'
          '        if n == 0:\n'
          '            return None\n'
          '        if n == 1:\n'
          '            return lists[0]\n'
          '        left = self.mergeKLists(lists[:mid])\n'
          '        right = self.mergeKLists(lists[mid:])\n'
          '        return merge(left, right)',
  'tips': ['把链表头列表分成两半，递归得到两个有序结果，再用合并两个有序链表的写法合并。递归切片复制的是头节点引用。',
           '当 k ≥ 2 时，时间上界 O((N+k) log k)，N 是节点总数。切片峰值空间 O(k)，递归深度 O(log k)。']},
 {'title': 'LRU 缓存',
  'source': 'LC 146',
  'note': '实现容量固定的 LRUCache。get 取值，缺键返回 -1。put 插入或更新。每次访问都把键变为最近使用，超容量时淘汰最久未使用的键。',
  'example': '操作 = ["LRUCache","put","put","get","put","get","get"]；参数 = [[2],[1,1],[2,2],[1],[3,3],[2],[3]]  →  '
             '[null,null,null,1,null,-1,3]',
  'code': 'class Node:\n'
          '    def __init__(self, key=0, val=0, prev=None, next=None):\n'
          '        self.key = key\n'
          '        self.val = val\n'
          '        self.prev = prev\n'
          '        self.next = next\n'
          '\n'
          '\n'
          'class LRUCache:\n'
          '    def __init__(self, capacity):\n'
          '        self.size = 0\n'
          '        self.capacity = capacity\n'
          '        self.hash = {}\n'
          '        self.head = Node()\n'
          '        self.tail = Node()\n'
          '        self.head.next = self.tail\n'
          '        self.tail.prev = self.head\n'
          '\n'
          '    def get(self, key):\n'
          '        if key not in self.hash:\n'
          '            return -1\n'
          '        node = self.hash[key]\n'
          '        self.removenode(node)\n'
          '        self.addtohead(node)                 # 访问过的节点移到头部\n'
          '        return node.val\n'
          '\n'
          '    def put(self, key, val):\n'
          '        if key not in self.hash:\n'
          '            node = Node(key, val)\n'
          '            self.hash[key] = node\n'
          '            self.addtohead(node)\n'
          '            self.size += 1\n'
          '            if self.size > self.capacity:\n'
          '                node2 = self.removetail()    # 淘汰尾部的实际节点\n'
          '                self.hash.pop(node2.key)\n'
          '                self.size -= 1\n'
          '        else:\n'
          '            self.hash[key].val = val\n'
          '            self.removenode(self.hash[key])\n'
          '            self.addtohead(self.hash[key])\n'
          '\n'
          '    def removenode(self, node):\n'
          '        node.next.prev = node.prev\n'
          '        node.prev.next = node.next\n'
          '        node.prev = None\n'
          '        node.next = None\n'
          '\n'
          '    def addtohead(self, node):\n'
          '        node.next = self.head.next\n'
          '        self.head.next.prev = node\n'
          '        node.prev = self.head\n'
          '        self.head.next = node\n'
          '\n'
          '    def removetail(self):\n'
          '        node = self.tail.prev\n'
          '        self.removenode(node)\n'
          '        return node',
  'tips': ['字典按键定位节点，双向链表维护使用顺序。头尾都是哨兵，头后是最近使用，尾前是最久未用。淘汰时同时从字典和链表删掉节点。',
           '这里的 Node 是题内自定义的双向节点，含 key、val、prev、next。get、put 平均 O(1)，空间 O(capacity)。示例的 null 对应构造或无返回值的操作。']}],
  'pending': [(160, '相交链表'),
              (206, '反转链表'),
              (234, '回文链表'),
              (141, '环形链表'),
              (142, '环形链表 II'),
              (21, '合并两个有序链表'),
              (2, '两数相加'),
              (19, '删除链表的倒数第 N 个结点'),
              (24, '两两交换链表中的节点'),
              (25, 'K 个一组翻转链表'),
              (138, '随机链表的复制'),
              (148, '排序链表'),
              (23, '合并 K 个升序链表'),
              (146, 'LRU 缓存')],
  'summary': ['① 相交链表靠换头对齐路程。环形链表的计数法用到题面上限，环形链表 II 用集合找第一个重复节点。\n'
   '② 反转先存 next。回文先找中点，再反转后半段比较。两两交换和 K 个一组翻转都要接好组间指针。\n'
   '③ 合并有序链表每次选较小值。两数相加从低位往高位传进位。删除倒数节点先将位置换成正向下标。\n'
   '④ 随机链表先建立原节点到新节点的映射。排序链表先排序节点引用再重连。合并 K 条链表先分治再两两合并。\n'
   '⑤ LRU 用字典定位节点，用双向链表维护最近使用顺序。',
   '读题先分清返回的是节点还是值，是否要求原地改指针。重连前先保存后续入口。普通 ListNode、随机指针 Node 的定义见附录，LRU 的双向 Node 随题给出。']},
 {'id': 'binary-tree',
  'name': '二叉树',
  'problems': [{'title': '二叉树的中序遍历',
  'source': 'LC 94',
  'note': '给定二叉树的根节点 root，按左子树、根、右子树的顺序返回节点值。',
  'example': 'root = [1,null,2,3]  →  [1,3,2]；root = []  →  []',
  'code': 'class Solution:\n'
          '    def inorderTraversal(self, root):\n'
          '        stack = []\n'
          '        res = []\n'
          '        while stack or root:\n'
          '            if not root:\n'
          '                node = stack.pop()      # 左子树已处理，可以访问该节点\n'
          '                res.append(node.val)\n'
          '                root = node.right\n'
          '            else:\n'
          '                stack.append(root)      # 先记住节点，继续向左\n'
          '                root = root.left\n'
          '        return res',
  'tips': ['栈里存的是还没访问的节点。走不到更左的位置时弹栈，先访问节点，再从它的右子树继续。', '时间 O(n)，辅助空间 O(h)，h 为树高。']},
 {'title': '二叉树的最大深度',
  'source': 'LC 104',
  'note': '返回从根到最远叶子的最长路径上的节点数。空树的深度是 0。',
  'example': 'root = [3,9,20,null,null,15,7]  →  3；root = []  →  0',
  'code': 'import sys\n'
          '\n'
          'if sys.getrecursionlimit() < 11000:\n'
          '    sys.setrecursionlimit(11000)\n'
          '\n'
          'class Solution:\n'
          '    def maxDepth(self, root):\n'
          '        if not root:\n'
          '            return 0\n'
          '        left = self.maxDepth(root.left)\n'
          '        right = self.maxDepth(root.right)\n'
          '        return max(left, right) + 1      # 较深的子树再加当前节点',
  'tips': ['先递归得到左右子树的深度，再取较大的值加 1。时间 O(n)，递归栈空间 O(h)。',
           '极深的单链树可能触发 Python 的递归深度限制。代码在上限不足时调高它，保留原递归；该设置作用于当前解释器。']},
 {'title': '翻转二叉树',
  'source': 'LC 226',
  'note': '交换每个节点的左右子树，原地翻转整棵树并返回根节点。',
  'example': 'root = [4,2,7,1,3,6,9]  →  [4,7,2,9,6,3,1]；root = []  →  []',
  'code': 'class Solution:\n'
          '    def invertTree(self, root):\n'
          '        if not root:\n'
          '            return None\n'
          '\n'
          '        left = self.invertTree(root.left)\n'
          '        right = self.invertTree(root.right)\n'
          '        root.right = left               # 把翻转后的左子树放到右边\n'
          '        root.left = right\n'
          '        return root',
  'tips': ['先翻转左右子树，再交换它们的根引用。空树在 Python 中返回 None，层序示例写作 []。时间 O(n)，递归栈空间 O(h)。']},
 {'title': '对称二叉树',
  'source': 'LC 101',
  'note': '判断二叉树是否沿根节点的中轴线镜像对称。',
  'example': 'root = [1,2,2,3,4,4,3]  →  True；root = [1,2,2,null,3,null,3]  →  False',
  'code': 'class Solution:\n'
          '    def isSymmetric(self, root):\n'
          '        if not root:\n'
          '            return True\n'
          '\n'
          '        def mirror(left, right):\n'
          '            if not left and not right:\n'
          '                return True\n'
          '            if not left or not right:\n'
          '                return False\n'
          '            if left.val != right.val:\n'
          '                return False\n'
          '            # 镜像位置是左对右、右对左\n'
          '            return mirror(left.left, right.right) and mirror(left.right, right.left)\n'
          '\n'
          '        return mirror(root.left, root.right)',
  'tips': ['比较一对镜像节点时，先看空位是否一致，再看值是否相等。继续递归时交叉比较孩子。时间 O(n)，递归栈空间 O(h)。']},
 {'title': '二叉树的直径',
  'source': 'LC 543',
  'note': '返回树上任意两个节点之间最长简单路径的长度，按边数计。路径可以不经过根。',
  'example': 'root = [1,2,3,4,5]  →  3；root = [1]  →  0',
  'code': 'import sys\n'
          '\n'
          'if sys.getrecursionlimit() < 11000:\n'
          '    sys.setrecursionlimit(11000)\n'
          '\n'
          'class Solution:\n'
          '    def diameterOfBinaryTree(self, root):\n'
          '        self.ans = 0\n'
          '\n'
          '        def dfs(node):\n'
          '            if not node:\n'
          '                return 0\n'
          '            left = dfs(node.left)\n'
          '            right = dfs(node.right)\n'
          '            self.ans = max(self.ans, left + right)  # 经过当前节点的路径边数\n'
          '            return max(left, right) + 1            # 返回当前子树的高度\n'
          '\n'
          '        dfs(root)\n'
          '        return self.ans',
  'tips': ['dfs 返回从当前节点向下的高度，按节点数计。经过当前节点的路径边数恰好是两侧子树高度之和。往父节点继续延伸时只能带上一侧。时间 O(n)，递归栈空间 O(h)。',
           '极深的单链树可能触发 Python 的递归深度限制。代码在上限不足时调高它，保留原递归；该设置作用于当前解释器。']},
 {'title': '二叉树的层序遍历',
  'source': 'LC 102',
  'note': '从上到下逐层访问节点，同一层从左到右。返回每层节点值组成的列表。',
  'example': 'root = [3,9,20,null,null,15,7]  →  [[3],[9,20],[15,7]]；root = []  →  []',
  'code': 'class Solution:\n'
          '    def levelOrder(self, root):\n'
          '        if not root:\n'
          '            return []\n'
          '\n'
          '        res, queue = [], [root]\n'
          '        while queue:\n'
          '            tmp = []\n'
          '            for node in queue:           # 这一轮遍历的是开始时的列表\n'
          '                queue = queue[1:]        # 新列表去掉当前节点，再追加孩子\n'
          '                tmp.append(node.val)\n'
          '                if node.left:\n'
          '                    queue.append(node.left)\n'
          '                if node.right:\n'
          '                    queue.append(node.right)\n'
          '            res.append(tmp)\n'
          '        return res',
  'tips': ['for 已经拿到本轮原列表的迭代器，queue = queue[1:] 只是把变量绑定到新列表。因此新加入的孩子留到下一轮处理。',
           '每个节点都切片复制队列。若 w 是最大层宽，时间最坏 O(n × w)，辅助空间 O(w)。右视图题的写法可以另存下一层，省掉切片。']},
 {'title': '将有序数组转换为二叉搜索树',
  'source': 'LC 108',
  'note': '给定严格升序数组 nums，构造一棵高度平衡的二叉搜索树。每个节点的左右子树高度差至多为 1。',
  'example': 'nums = [-10,-3,0,5,9]  →  [0,-10,5,null,-3,null,9]（一种合法结果）',
  'code': 'class Solution:\n'
          '    def sortedArrayToBST(self, nums):\n'
          '        n = len(nums)\n'
          '        if n == 0:\n'
          '            return None\n'
          '\n'
          '        left, right = 0, n - 1\n'
          '        mid = (left + right) // 2\n'
          '        root = TreeNode(nums[mid])\n'
          '        root.left = self.sortedArrayToBST(nums[:mid])\n'
          '        root.right = self.sortedArrayToBST(nums[mid+1:])\n'
          '        return root',
  'tips': ['每次取中点为根，左边的数更小，右边的数更大，两段长度最多差 1。TreeNode 由判题平台提供。',
           '数组切片会复制。时间 O(n log n)，不计返回的树，切片峰值空间 O(n)，递归深度 O(log n)。']},
 {'title': '验证二叉搜索树',
  'source': 'LC 98',
  'note': '判断整棵树是否满足 BST 定义。每个节点的左子树所有值都更小，右子树所有值都更大。',
  'example': 'root = [2,1,3]  →  True；root = [2,2,3]  →  False',
  'code': 'import sys\n'
          '\n'
          'if sys.getrecursionlimit() < 11000:\n'
          '    sys.setrecursionlimit(11000)\n'
          '\n'
          'class Solution:\n'
          '    def isValidBST(self, root):\n'
          '        self.ans = []\n'
          '\n'
          '        def dfs(node):\n'
          '            if not node:\n'
          '                return\n'
          '            dfs(node.left)\n'
          '            self.ans.append(node.val)\n'
          '            dfs(node.right)\n'
          '\n'
          '        dfs(root)\n'
          '        for i in range(1, len(self.ans)):\n'
          '            if self.ans[i] <= self.ans[i-1]:\n'
          '                return False             # 中序序列必须严格递增\n'
          '        return True',
  'tips': ['看整棵树的中序序列。相邻值相等也不合法；只检查当前节点和它的两个直接孩子会漏掉更深处的违规值。时间 O(n)，辅助空间 O(n)。',
           '极深的单链树可能触发 Python 的递归深度限制。代码在上限不足时调高它，保留原递归；该设置作用于当前解释器。']},
 {'title': '二叉搜索树中第 K 小的元素',
  'source': 'LC 230',
  'note': '给定 BST 和合法的 k，返回按值从小到大排在第 k 位的节点值。k 从 1 开始。',
  'example': 'root = [3,1,4,null,2]，k = 1  →  1；k = 3  →  3',
  'code': 'import sys\n'
          '\n'
          'if sys.getrecursionlimit() < 11000:\n'
          '    sys.setrecursionlimit(11000)\n'
          '\n'
          'class Solution:\n'
          '    def kthSmallest(self, root, k):\n'
          '        self.k = k\n'
          '        self.ans = 0\n'
          '\n'
          '        def dfs(node):\n'
          '            if not node:\n'
          '                return\n'
          '            dfs(node.left)\n'
          '            if self.k > 1:\n'
          '                self.k -= 1\n'
          '            elif self.k == 1:\n'
          '                self.ans = node.val\n'
          '                self.k -= 1              # 变为 0，通知上层已经找到\n'
          '                return\n'
          '            else:\n'
          '                return\n'
          '            dfs(node.right)              # 只有还没找到才继续搜右子树\n'
          '\n'
          '        dfs(root)\n'
          '        return self.ans',
  'tips': ['中序遍历依次访问从小到大的值。k 每访问一个节点就减 1，减到 0 时保存答案。外层先运行 dfs，再返回 self.ans。时间 O(h + k)，递归栈空间 O(h)。',
           '极深的单链树可能触发 Python 的递归深度限制。代码在上限不足时调高它，保留原递归；该设置作用于当前解释器。']},
 {'title': '二叉树的右视图',
  'source': 'LC 199',
  'note': '从树的右侧观察，返回每一层最右边节点的值，按从上到下的顺序排列。',
  'example': 'root = [1,2,3,null,5,null,4]  →  [1,3,4]；root = []  →  []',
  'code': 'class Solution:\n'
          '    def rightSideView(self, root):\n'
          '        if not root:\n'
          '            return []\n'
          '        queue = [root]\n'
          '        ans = []\n'
          '        k = 0\n'
          '        while queue:\n'
          '            tmp = []\n'
          '            for i in range(len(queue)):\n'
          '                node = queue[i]\n'
          '                if i == len(queue) - 1:\n'
          '                    ans.append(node.val)    # 当前层最后一个节点\n'
          '                if node.left:\n'
          '                    tmp.append(node.left)\n'
          '                if node.right:\n'
          '                    tmp.append(node.right)\n'
          '            queue = tmp\n'
          '            k += 1\n'
          '        return ans',
  'tips': ['每层先把左孩子放入下一层，再放右孩子。因此每层最后访问的是最右节点。k 只记录层数，没有参与求解。时间 O(n)，辅助空间 O(w)，w 为最大层宽。']},
 {'title': '二叉树展开为链表',
  'source': 'LC 114',
  'note': '按前序顺序把原树展开成一条只走 right 指针的链。所有 left 都为 None，函数返回 None。',
  'example': 'root = [1,2,5,3,4,null,6]  →  原树变为 [1,null,2,null,3,null,4,null,5,null,6]，返回 None',
  'code': 'import sys\n'
          '\n'
          'if sys.getrecursionlimit() < 3000:\n'
          '    sys.setrecursionlimit(3000)\n'
          '\n'
          'class Solution:\n'
          '    def flatten(self, root):\n'
          '        self.ans = []\n'
          '\n'
          '        def dfs(node):\n'
          '            if not node:\n'
          '                return\n'
          '            self.ans.append(node)           # 保存原节点，保留前序顺序\n'
          '            dfs(node.left)\n'
          '            dfs(node.right)\n'
          '\n'
          '        dfs(root)\n'
          '        for i in range(len(self.ans) - 1):\n'
          '            self.ans[i].left = None\n'
          '            self.ans[i].right = self.ans[i+1]  # 指向前序中的下一个节点',
  'tips': ['先记住原节点，再逐一改指针。前序的最后一个节点必然是叶子，原来的左右指针都已经是 None。',
           '方法原地修改节点，省略 return 即返回 None。时间 O(n)，辅助列表和递归栈合计 O(n)。',
           '极深的单链树可能触发 Python 的递归深度限制。代码在上限不足时调高它，保留原递归；该设置作用于当前解释器。']},
 {'title': '从前序与中序遍历序列构造二叉树',
  'source': 'LC 105',
  'note': '给定同一棵树的前序序列 preorder 和中序序列 inorder，节点值互不相同。重建原树并返回根节点。',
  'example': 'preorder = [3,9,20,15,7]，inorder = [9,3,15,20,7]  →  [3,9,20,null,null,15,7]',
  'code': 'import sys\n'
          '\n'
          'if sys.getrecursionlimit() < 4000:\n'
          '    sys.setrecursionlimit(4000)\n'
          '\n'
          'class Solution:\n'
          '    def buildTree(self, preorder, inorder):\n'
          '        val_to_idx = {v: i for i, v in enumerate(inorder)}\n'
          '\n'
          '        def dfs(pre_l, pre_r, in_l, in_r):\n'
          '            if pre_l > pre_r:\n'
          '                return None\n'
          '            root_val = preorder[pre_l]        # 前序首元素是根\n'
          '            root_in = val_to_idx[root_val]\n'
          '            left_cnt = root_in - in_l         # 中序中根左边都是左子树\n'
          '            root = TreeNode(root_val)\n'
          '            root.left = dfs(pre_l+1, pre_l+left_cnt, in_l, root_in-1)\n'
          '            root.right = dfs(pre_l+left_cnt+1, pre_r, root_in+1, in_r)\n'
          '            return root\n'
          '\n'
          '        return dfs(0, len(preorder)-1, 0, len(inorder)-1)',
  'tips': ['四个下标表示前序和中序的两个闭区间。先在中序中算出左子树节点数，再用这个数量把前序分成根、左子树、右子树三段。',
           '字典让根在中序中的下标可以直接查到。时间 O(n)，不计结果树的额外空间 O(n)。',
           '极深的单链树可能触发 Python 的递归深度限制。代码在上限不足时调高它，保留原递归；该设置作用于当前解释器。']},
 {'title': '路径总和 III',
  'source': 'LC 437',
  'note': '统计节点值总和等于 targetSum 的向下路径。路径只沿父节点走向子节点，起终点可以是任意节点。',
  'example': 'root = [10,5,-3,3,2,null,11,3,-2,null,1]，targetSum = 8  →  3；root = []，targetSum = 0  →  0',
  'code': 'import sys\n'
          '\n'
          'if sys.getrecursionlimit() < 2000:\n'
          '    sys.setrecursionlimit(2000)\n'
          '\n'
          'from collections import defaultdict\n'
          '\n'
          'class Solution:\n'
          '    def pathSum(self, root, targetSum):\n'
          '        self.hash = defaultdict(int)\n'
          '        self.ans = 0\n'
          '        self.cur = 0\n'
          '        self.hash[0] = 1                 # 根节点之前有一个空前缀\n'
          '\n'
          '        def dfs(node):\n'
          '            if not node:\n'
          '                return\n'
          '            self.cur += node.val\n'
          '            self.ans += self.hash[self.cur - targetSum]\n'
          '            self.hash[self.cur] += 1     # 查完再登记，避免把空路径计进去\n'
          '            dfs(node.left)\n'
          '            dfs(node.right)\n'
          '            self.hash[self.cur] -= 1     # 离开时撤销前缀记录\n'
          '            self.cur -= node.val\n'
          '\n'
          '        dfs(root)\n'
          '        return self.ans',
  'tips': ['若当前前缀和是 cur，祖先路径上每出现一次 cur - targetSum，就对应一条以当前节点结尾的合法路径。',
           '进入节点时登记，退出时减回去，左右分支的前缀不会串起来。计数为 0 的键仍留在字典中，辅助空间最坏 O(n)，时间 O(n)。',
           '极深的单链树可能触发 Python 的递归深度限制。代码在上限不足时调高它，保留原递归；该设置作用于当前解释器。']},
 {'title': '二叉树的最近公共祖先',
  'source': 'LC 236',
  'note': '给定二叉树和其中两个不同的节点 p、q，返回它们最深的公共祖先。节点可以是自己的祖先。',
  'example': 'root = [3,5,1,6,2,0,8,null,null,7,4]，p = 5，q = 4  →  值为 5 的原节点',
  'code': 'import sys\n'
          '\n'
          'if sys.getrecursionlimit() < 101000:\n'
          '    sys.setrecursionlimit(101000)\n'
          '\n'
          'class Solution:\n'
          '    def lowestCommonAncestor(self, root, p, q):\n'
          '        self.path1 = []\n'
          '        self.path2 = []\n'
          '        self.cur = []\n'
          '\n'
          '        def dfs(node):\n'
          '            if not node:\n'
          '                return\n'
          '            self.cur.append(node)\n'
          '            if node == p:\n'
          '                self.path1 = self.cur[:]   # 保存从根到 p 的路径\n'
          '            if node == q:\n'
          '                self.path2 = self.cur[:]\n'
          '            dfs(node.left)\n'
          '            dfs(node.right)\n'
          '            self.cur.pop()\n'
          '\n'
          '        dfs(root)\n'
          '        ans = None\n'
          '        for i in range(min(len(self.path1), len(self.path2))):\n'
          '            if self.path1[i] == self.path2[i]:\n'
          '                ans = self.path1[i]       # 保留当前最深的共同节点\n'
          '            else:\n'
          '                break\n'
          '        return ans',
  'tips': ['从根到 p、q 的两条路径都从同一个根出发。比较共同前缀，最后一个相同节点就是答案。题目保证 p、q 存在，示例用值指明节点，函数实际返回节点对象。时间 O(n)，辅助空间 O(h)。',
           '极深的单链树可能触发 Python 的递归深度限制。代码在上限不足时调高它，保留原递归；该设置作用于当前解释器。']},
 {'title': '二叉树中的最大路径和',
  'source': 'LC 124',
  'note': '返回二叉树中任意一条非空简单路径的最大节点值之和。路径可以不经过根。',
  'example': 'root = [-10,9,20,null,null,15,7]  →  42；root = [-3]  →  -3',
  'code': 'import sys\n'
          '\n'
          'if sys.getrecursionlimit() < 31000:\n'
          '    sys.setrecursionlimit(31000)\n'
          '\n'
          'class Solution:\n'
          '    def maxPathSum(self, root):\n'
          '        max_sum = -10**9\n'
          '\n'
          '        def dfs(node):\n'
          '            nonlocal max_sum\n'
          '            if not node:\n'
          '                return 0\n'
          '            left = max(dfs(node.left), 0)\n'
          '            right = max(dfs(node.right), 0)\n'
          '            max_sum = max(max_sum, node.val + left + right)  # 此处可接两边\n'
          '            return node.val + max(left, right)              # 向上只能接一边\n'
          '\n'
          '        dfs(root)\n'
          '        return max_sum',
  'tips': ['和直径题一样，要分开看「在当前节点合并两侧」和「向父节点上报一侧」。负收益取 0 表示不接那条子路径。',
           '路径至少有一个节点，答案不能从 0 起步。题目保证节点值不低于 -1000，原稿的 -10**9 足够小。时间 O(n)，递归栈空间 O(h)。',
           '极深的单链树可能触发 Python 的递归深度限制。代码在上限不足时调高它，保留原递归；该设置作用于当前解释器。']}],
  'pending': [(94, '二叉树的中序遍历'),
              (104, '二叉树的最大深度'),
              (226, '翻转二叉树'),
              (101, '对称二叉树'),
              (543, '二叉树的直径'),
              (102, '二叉树的层序遍历'),
              (108, '将有序数组转换为二叉搜索树'),
              (98, '验证二叉搜索树'),
              (230, '二叉搜索树中第 K 小的元素'),
              (199, '二叉树的右视图'),
              (114, '二叉树展开为链表'),
              (105, '从前序与中序遍历序列构造二叉树'),
              (437, '路径总和 III'),
              (236, '二叉树的最近公共祖先'),
              (124, '二叉树中的最大路径和')],
  'summary': ['① 中序遍历用栈保存还未访问的节点。最大深度向上返回较大高度加 1。翻转先处理子树再交换，对称则交叉比较两边。\n'
   '② 直径在当前节点合并两侧高度。最大路径和合并两侧非负收益，向父节点只能交出一侧。\n'
   '③ 层序遍历收集每层所有节点，右视图只收每层最后一个。\n'
   '④ 有序数组建 BST 取中点。验证 BST 检查中序是否严格递增，第 K 小在中序中按访问次序计数。\n'
   '⑤ 展开用前序保存原节点，再改指针。前序加中序建树时，先从中序算左子树大小。\n'
   '⑥ 路径总和 III 用当前前缀减目标值查次数。最近公共祖先找两条根路径的最后一个共同节点。',
   '先区分要返回节点、节点值还是 None。写递归时先确定返回给父节点的量，再判断哪些答案需要在当前节点更新。树的示例统一用层序数组表示，null 是缺失的子节点，末尾的 null 可以省略。']},
 {'id': 'graph',
  'name': '图论',
  'problems': [{'title': '岛屿数量',
  'source': 'LC 200',
  'note': '给定由字符 "1"（陆地）和 "0"（水）组成的网格。上下左右相邻的陆地属于同一座岛，返回岛屿数量。',
  'example': 'grid = [["1","0"],["0","1"]]  →  2（对角不相连）；grid = [["0"]]  →  0',
  'code': 'class Solution:\n'
          '    def numIslands(self, grid):\n'
          '        m = len(grid)\n'
          '        n = len(grid[0])\n'
          '\n'
          '        def dfs(grid, x, y):\n'
          '            stack = [(x, y)]\n'
          '            grid[x][y] = 0                  # 入栈时就标记，避免重复入栈\n'
          '            while stack:\n'
          '                x, y = stack.pop()\n'
          '                for a, b in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:\n'
          '                    if 0 <= a < m and 0 <= b < n and grid[a][b] == "1":\n'
          '                        grid[a][b] = 0\n'
          '                        stack.append((a, b))\n'
          '\n'
          '        ans = 0\n'
          '        for i in range(m):\n'
          '            for j in range(n):\n'
          '                if grid[i][j] == "1":\n'
          '                    dfs(grid, i, j)        # 一次 DFS 标记整座岛\n'
          '                    ans += 1\n'
          '        return ans',
  'tips': ['扫描时第一次遇到某座岛，就用 DFS 标记所有相连的陆地。代码沿用原稿，用整数 0 原地标记已访问的陆地，后续只认字符串 "1"。',
           '原稿的递归 DFS 在岛很长时可能触发 Python 的递归深度限制。显式栈仍做深度优先搜索，可处理题目允许的大网格。',
           '时间 O(m × n)，辅助栈最坏 O(m × n)。']},
 {'title': '腐烂的橘子',
  'source': 'LC 994',
  'note': '网格中 0 是空格，1 是新鲜橘子，2 是腐烂橘子。每分钟，所有腐烂橘子同时感染上下左右相邻的新鲜橘子。返回全部腐烂所需的分钟数，无法全部腐烂时返回 -1。',
  'example': 'grid = [[2,1,1],[1,1,0],[0,1,1]]  →  4；grid = [[1,0,2]]  →  -1；grid = [[0]]  →  0',
  'code': 'class Solution:\n'
          '    def orangesRotting(self, grid):\n'
          '        m = len(grid)\n'
          '        n = len(grid[0])\n'
          '        num = 0\n'
          '        queue = []\n'
          '        ans = 0\n'
          '        for i in range(m):\n'
          '            for j in range(n):\n'
          '                if grid[i][j] == 1:\n'
          '                    num += 1\n'
          '                elif grid[i][j] == 2:\n'
          '                    queue.append([i, j])   # 所有烂橘子同时作为起点\n'
          '\n'
          '        while queue:\n'
          '            tmp = []\n'
          '            for a, b in queue:\n'
          '                for x, y in [(a-1, b), (a+1, b), (a, b-1), (a, b+1)]:\n'
          '                    if 0 <= x < m and 0 <= y < n and grid[x][y] == 1:\n'
          '                        grid[x][y] = 2     # 立即标记，避免同一格重复计数\n'
          '                        tmp.append([x, y])\n'
          '                        num -= 1\n'
          '            queue = tmp\n'
          '            if tmp:\n'
          '                ans += 1                   # 本轮确实有新橘子变烂\n'
          '        return ans if not num else -1',
  'tips': ['这是多源 BFS。queue 放本轮要扩散的橘子，tmp 放这一轮刚变烂的橘子。tmp 要等到下一轮才继续扩散。',
           'num 始终是剩余新鲜橘子的数量。BFS 结束后还有新鲜橘子就返回 -1。代码会原地更新 grid。时间 O(m × n)，辅助空间 O(m × n)。'],
  'remarks': [{'title': '备注 · BFS 层数和分钟数',
               'note': '错点是把分钟数从 -1 开始，每处理一层就加 1。只要初始队列有烂橘子，这种写法可以抵消最后一轮没有新感染的加 1。可是全空网格 [[0]] '
                       '没有初始烂橘子，也没有新鲜橘子，循环一次都不会进，分钟数一直是 -1，正确结果是 0。改进是从 0 开始，只在 tmp 非空时加 1，让分钟数直接表示发生了几轮感染。以后先用 '
                       '[[0]]、[[2]]、[[1]]、[[2,1]] 手推，答案分别是 0、0、-1、1。检查初始队列为空、最后一轮没感染、只扩散一轮这几种情况。'}]},
 {'title': '课程表',
  'source': 'LC 207',
  'note': '共有 numCourses 门课，编号从 0 到 numCourses - 1。先修关系 [a,b] 表示先上 b 才能上 a。判断能否修完全部课程。',
  'example': 'numCourses = 2，prerequisites = [[1,0]]  →  True；prerequisites = [[1,0],[0,1]]  →  '
             'False；prerequisites = []  →  True',
  'code': 'from collections import defaultdict\n'
          '\n'
          'class Solution:\n'
          '    def canFinish(self, numCourses, prerequisites):\n'
          '        indegree = defaultdict(int)\n'
          '        next_courses = defaultdict(list)\n'
          '        ans = 0\n'
          '        queue = []\n'
          '        for course, prerequisite in prerequisites:\n'
          '            indegree[course] += 1\n'
          '            next_courses[prerequisite].append(course)  # 边：先修课 → 后续课\n'
          '        for course in range(numCourses):\n'
          '            if indegree[course] == 0:\n'
          '                ans += 1\n'
          '                queue.append(course)\n'
          '\n'
          '        while queue:\n'
          '            tmp = []\n'
          '            for course in queue:\n'
          '                for nxt in next_courses[course]:\n'
          '                    indegree[nxt] -= 1\n'
          '                    if indegree[nxt] == 0:\n'
          '                        ans += 1            # 所有先修课都已完成\n'
          '                        tmp.append(nxt)\n'
          '            queue = tmp\n'
          '        return ans == numCourses',
  'tips': ['入度表示还有多少先修课没有完成。先把入度为 0 的课放入队列。处理完一门课，就把它指向的课程的入度减 1。',
           '每门课在第一次变为可修时计数一次。队列空了却还有课程没计入，说明剩余依赖中有环。时间和辅助空间都是 O(V + E)，V 是课程数，E 是先修关系数。']},
 {'title': '实现 Trie (前缀树)',
  'source': 'LC 208',
  'note': '实现 Trie，支持插入单词、查询完整单词、查询是否存在给定前缀。',
  'example': '操作 = ["Trie","insert","search","search","startsWith","insert","search"]；参数 = '
             '[[],["apple"],["apple"],["app"],["app"],["app"],["app"]]  →  [null,null,true,false,true,null,true]',
  'code': 'class Trie:\n'
          '    def __init__(self):\n'
          '        self.root = Node()\n'
          '\n'
          '    def insert(self, word):\n'
          '        cur = self.root\n'
          '        for ch in word:\n'
          '            if ch not in cur.son:\n'
          '                cur.son[ch] = Node()       # 缺少这条字符边就新建节点\n'
          '            cur = cur.son[ch]\n'
          '        cur.end = True                    # 整个单词到这里结束\n'
          '\n'
          '    def search(self, word):\n'
          '        cur = self.root\n'
          '        for ch in word:\n'
          '            if ch not in cur.son:\n'
          '                return False\n'
          '            else:\n'
          '                cur = cur.son[ch]\n'
          '        return True if cur.end else False\n'
          '\n'
          '    def startsWith(self, prefix):\n'
          '        cur = self.root\n'
          '        for ch in prefix:\n'
          '            if ch not in cur.son:\n'
          '                return False\n'
          '            else:\n'
          '                cur = cur.son[ch]\n'
          '        return True                       # 前缀路径走通即可\n'
          '\n'
          '\n'
          'class Node:\n'
          '    def __init__(self):\n'
          '        self.son = dict()\n'
          '        self.end = False',
  'tips': ['son 把下一个字符映射到对应子节点，end 表示某个已插入的单词在这一格结束。只插入 apple 时，app 的路径存在，但 app 的 end 仍是 False。',
           'insert 会在原 Trie 上添加节点或标记词尾，返回 None。示例里的 null 对应构造或无返回值的操作。三种操作的时间都是 O(L)，L 是本次传入的单词或前缀长度。']}],
  'pending': [(200, '岛屿数量'), (994, '腐烂的橘子'), (207, '课程表'), (208, '实现 Trie (前缀树)')],
  'summary': ['① 岛屿数量\u3000遇到一块未访问陆地，就用 DFS 标记整座岛。\n'
   '② 腐烂的橘子\u3000所有初始烂橘子一起做 BFS，下一层有新感染才加一分钟。\n'
   '③ 课程表\u3000从入度为 0 的课程出发，逐步解除后续课程的先修限制。\n'
   '④ 前缀树\u3000顺着字符走，查完整单词还要检查词尾标记。',
   '网格题先定邻接方向和标记时机。分层搜索要分清队列里放的是哪一轮，以及哪次状态变化才应计入答案。']},
 {'id': 'backtracking',
  'name': '回溯',
  'problems': [{'title': '全排列',
  'source': 'LC 46',
  'note': '给定互不相同的整数数组 nums，返回由全部元素组成的所有排列。答案顺序不限。',
  'example': 'nums = [1,2,3]  →  [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]',
  'code': 'class Solution:\n'
          '    def permute(self, nums):\n'
          '        path, ans = [], []\n'
          '\n'
          '        def dfs():\n'
          '            if len(path) == len(nums):\n'
          '                ans.append(path[:])    # 保存快照，后续还要修改 path\n'
          '                return\n'
          '            for num in nums:\n'
          '                if num not in path:   # 当前排列里还没用过\n'
          '                    path.append(num)\n'
          '                    dfs()\n'
          '                    path.pop()         # 撤销这次选择\n'
          '\n'
          '        dfs()\n'
          '        return ans',
  'tips': ['每层决定排列的下一位。每一层都从整个 nums 里选，只跳过当前路径已经用过的值。这里用值判断是否用过，依赖 nums 中的元素互不相同。',
           '路径长到 n 才收集答案。列表里的成员检查需要扫描当前路径，时间上界 O(n² × n!)，不计答案的额外空间 O(n)。']},
 {'title': '子集',
  'source': 'LC 78',
  'note': '给定互不相同的整数数组 nums，返回它的所有子集，包括空集。每个子集只返回一次，答案顺序不限。',
  'example': 'nums = [1,2]  →  [[],[1],[1,2],[2]]',
  'code': 'class Solution:\n'
          '    def subsets(self, nums):\n'
          '        n = len(nums)\n'
          '        path, ans = [], []\n'
          '\n'
          '        def dfs(start):\n'
          '            ans.append(path[:])        # 到达每个节点时，路径已经是一个子集\n'
          '            for i in range(start, n):\n'
          '                path.append(nums[i])\n'
          '                dfs(i + 1)             # 下一次只能从更靠后的下标选\n'
          '                path.pop()\n'
          '\n'
          '        dfs(0)\n'
          '        return ans',
  'tips': ['根节点的路径为空，所以空集也会被收集。每层枚举下一个要选的下标，递归传 i+1。同一批元素只会按下标从小到大选出一次。',
           '全排列只在选满时收集，子集每到一个节点就收集。复制所有子集的总时间 O(n × 2ⁿ)，不计答案的额外空间 O(n)。']},
 {'title': '电话号码的字母组合',
  'source': 'LC 17',
  'note': '给定由数字 2 到 9 组成的非空字符串 digits，每位数字按电话键盘对应字母。每位选一个字母，返回所有组合。',
  'example': 'digits = "23"  →  ["ad","ae","af","bd","be","bf","cd","ce","cf"]；digits = "2"  →  ["a","b","c"]',
  'code': 'class Solution:\n'
          '    def letterCombinations(self, digits):\n'
          '        letters = {\n'
          '            "2": "abc", "3": "def", "4": "ghi", "5": "jkl",\n'
          '            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",\n'
          '        }\n'
          '        n = len(digits)\n'
          '        path, ans = [], []\n'
          '\n'
          '        def dfs(i):\n'
          '            if i == n:\n'
          '                ans.append("".join(path))  # 各位选完后再拼成字符串\n'
          '                return\n'
          '            for ch in letters[digits[i]]:\n'
          '                path.append(ch)\n'
          '                dfs(i + 1)                 # 处理下一位数字\n'
          '                path.pop()\n'
          '\n'
          '        dfs(0)\n'
          '        return ans',
  'tips': ['递归下标 i 指向当前处理的数字。每层只在这一位数字对应的字母里选。', '每位最多有 4 种选择，时间上界 O(n × 4ⁿ)，不计答案的额外空间 O(n)。']},
 {'title': '组合总和',
  'source': 'LC 39',
  'note': '给定互不相同的正整数 candidates 和正整数 target，返回所有和恰好为 target 的组合。同一个候选数可以重复选，组合顺序不限。',
  'example': 'candidates = [2,3,6,7], target = 7  →  [[2,2,3],[7]]；candidates = [2], target = 1  →  []',
  'code': 'class Solution:\n'
          '    def combinationSum(self, candidates, target):\n'
          '        n = len(candidates)\n'
          '        path, ans = [], []\n'
          '\n'
          '        def dfs(start):\n'
          '            total = sum(path)\n'
          '            if total == target:\n'
          '                ans.append(path[:])\n'
          '                return\n'
          '            if total > target:            # 候选数全是正数，再选只会更大\n'
          '                return\n'
          '            for i in range(start, n):\n'
          '                path.append(candidates[i])\n'
          '                dfs(i)                    # 允许下一次继续选 candidates[i]\n'
          '                path.pop()\n'
          '\n'
          '        dfs(0)\n'
          '        return ans',
  'tips': ['下一次从 i 开始，允许重复使用当前数。下标不会往回走，所以 [2,2,3] 和 [3,2,2] 只会收集其中一种。',
           '主解不排序。每进一层计算一次当前总和，超出 target 才返回。下面的剪枝版提前排除选了就会超出的分支。'],
  'remarks': [{'title': '备注 · 排序后按剩余目标剪枝',
               'note': '两种方法都枚举下一个数，并允许重复使用。主解用 sum(path) 计算已选总和，尝试选中后才知道是否超标。这里把剩余目标 left '
                       '传下去，省去重复求和。候选数排序后，发现当前数大于 left，就能跳过它和后面所有数。比如剩余 2，遇到 3 就直接结束本层循环。sort() 会原地改变 candidates '
                       '的顺序。',
               'code': 'class Solution:\n'
                       '    def combinationSum(self, candidates, target):\n'
                       '        candidates.sort()\n'
                       '        path, ans = [], []\n'
                       '\n'
                       '        def dfs(start, left):\n'
                       '            if left == 0:\n'
                       '                ans.append(path.copy())\n'
                       '                return\n'
                       '            for i in range(start, len(candidates)):\n'
                       '                num = candidates[i]\n'
                       '                if num > left:\n'
                       '                    break                 # 排过序，后面的数也太大\n'
                       '                path.append(num)\n'
                       '                dfs(i, left - num)        # 仍可选当前数，剩余目标减去 num\n'
                       '                path.pop()\n'
                       '\n'
                       '        dfs(0, target)\n'
                       '        return ans'}]},
 {'title': '括号生成',
  'source': 'LC 22',
  'note': '给定正整数 n，返回用 n 对圆括号组成的所有合法字符串。答案顺序不限。',
  'example': 'n = 3  →  ["((()))","(()())","(())()","()(())","()()()"]；n = 1  →  ["()"]',
  'code': 'class Solution:\n'
          '    def generateParenthesis(self, n):\n'
          '        path, ans = [], []\n'
          '\n'
          '        def dfs(i, left, right):\n'
          '            if i == 2 * n:\n'
          '                ans.append("".join(path))\n'
          '                return\n'
          '            if left < n:                 # 左括号还有剩余\n'
          '                path.append("(")\n'
          '                dfs(i + 1, left + 1, right)\n'
          '                path.pop()\n'
          '            if left > right:             # 有未配对的左括号才能放右括号\n'
          '                path.append(")")\n'
          '                dfs(i + 1, left, right + 1)\n'
          '                path.pop()\n'
          '\n'
          '        dfs(0, 0, 0)\n'
          '        return ans',
  'tips': ['left、right 分别是已经放进去的左右括号数。任意前缀都要满足 right ≤ left ≤ n。两种条件都满足时要分别试，所以用两个 if。',
           '路径达到 2n 时左右括号必然各有 n 个。不计答案的额外空间 O(n)。']},
 {'title': '单词搜索',
  'source': 'LC 79',
  'note': '给定非空的字符网格 board 和非空单词 word，判断是否能从某格出发，沿上下左右相邻格依次拼出 word。同一条路径中每个格子最多使用一次。',
  'example': 'board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]，word = "ABCCED"  →  True；word = '
             '"ABCB"  →  False',
  'code': 'class Solution:\n'
          '    def exist(self, board, word):\n'
          '        m, n = len(board), len(board[0])\n'
          '        visited = [[False] * n for _ in range(m)]\n'
          '        self.ans = False\n'
          '\n'
          '        def dfs(row, col, i):\n'
          '            if board[row][col] != word[i]:\n'
          '                return\n'
          '            if i == len(word) - 1:\n'
          '                self.ans = True\n'
          '                return\n'
          '            visited[row][col] = True    # 当前路径已经使用这一格\n'
          '            for r, c in ((row-1, col), (row+1, col), (row, col-1), (row, col+1)):\n'
          '                if 0 <= r < m and 0 <= c < n and not visited[r][c]:\n'
          '                    dfs(r, c, i + 1)\n'
          '                    if self.ans:\n'
          '                        return           # 已经找到，结束整次搜索\n'
          '            visited[row][col] = False   # 这一条路失败，撤销访问标记\n'
          '\n'
          '        for row in range(m):\n'
          '            for col in range(n):\n'
          '                if board[row][col] == word[0]:\n'
          '                    dfs(row, col, 0)\n'
          '                    if self.ans:\n'
          '                        return True\n'
          '        return False',
  'tips': ['递归下标 i 指向这一格要匹配的字符。主解用独立的 visited 矩阵防止同一路径重复使用格子，用 self.ans 把找到答案的消息传回上层。',
           '这一条路失败时解除访问标记，其他起点和路径还可以用这格。找到答案后会结束整次搜索，局部 visited 可以直接丢弃，棋盘本身没有被修改。'],
  'remarks': [{'title': '备注 · 字符计数、反向起搜与原地标记',
               'note': ('主解直接枚举起点，用独立矩阵标记访问状态，并用 self.ans '
                        '报告成功。优化版先数棋盘里每种字符够不够用。够用时再比较单词两端，若末尾字符在棋盘上更少，就把单词反过来，从更少的候选起点搜。路径能反向走，所以答案不变。递归直接返回布尔值，临时把已访问格改成空字符串。失败时恢复该格，找到答案就立即返回。因此成功时棋盘上的部分格子会保留为空字符串，之后复用棋盘时要留意。Counter '
                        '的逐项比较需要 Python 3.10 或更新版本。'),
               'code': 'from collections import Counter\n'
                       '\n'
                       'class Solution:\n'
                       '    def exist(self, board, word):\n'
                       '        counts = Counter(ch for row in board for ch in row)\n'
                       '        if not (counts >= Counter(word)):\n'
                       '            return False                    # 某种字符不够用\n'
                       '        if counts[word[-1]] < counts[word[0]]:\n'
                       '            word = word[::-1]               # 从棋盘上更少见的那一端起搜\n'
                       '\n'
                       '        m, n = len(board), len(board[0])\n'
                       '\n'
                       '        def dfs(row, col, i):\n'
                       '            if board[row][col] != word[i]:\n'
                       '                return False\n'
                       '            if i == len(word) - 1:\n'
                       '                return True\n'
                       '            board[row][col] = ""            # 临时标记这一格已用过\n'
                       '            for r, c in ((row, col-1), (row, col+1), (row-1, col), (row+1, col)):\n'
                       '                if 0 <= r < m and 0 <= c < n and dfs(r, c, i + 1):\n'
                       '                    return True\n'
                       '            board[row][col] = word[i]       # 失败后恢复这一格\n'
                       '            return False\n'
                       '\n'
                       '        return any(dfs(r, c, 0) for r in range(m) for c in range(n))'}]},
 {'title': '分割回文串',
  'source': 'LC 131',
  'note': '给定非空字符串 s，把它切成若干连续子串，每个子串都必须是回文。返回所有合法切法，答案顺序不限。',
  'example': 's = "aab"  →  [["a","a","b"],["aa","b"]]；s = "a"  →  [["a"]]',
  'code': 'class Solution:\n'
          '    def partition(self, s):\n'
          '        n = len(s)\n'
          '        path, ans = [], []\n'
          '\n'
          '        def dfs(i, pending):\n'
          '            piece = pending + s[i]       # 把当前字符接到尚未切下的一段\n'
          '            is_palindrome = piece == piece[::-1]\n'
          '            if i == n - 1:\n'
          '                if is_palindrome:       # 到末尾必须切下最后一段\n'
          '                    path.append(piece)\n'
          '                    ans.append(path[:])\n'
          '                    path.pop()\n'
          '                return\n'
          '\n'
          '            if is_palindrome:\n'
          '                path.append(piece)      # 选择在这里切\n'
          '                dfs(i + 1, "")\n'
          '                path.pop()\n'
          '            dfs(i + 1, piece)           # 选择先不切，下一位继续拼\n'
          '\n'
          '        dfs(0, "")\n'
          '        return ans',
  'tips': ['path 保存已经切好的回文段，pending 保存还没切的那一段。每个字符后都有机会切或不切。只有当前段为回文时才能切。',
           '当前段即使不是回文，也要保留继续拼的分支。例如 "ab" 还不是回文，再接一个 "a" 就成了 "aba"。最后一个字符后没有继续拼的选项。']},
 {'title': 'N 皇后',
  'source': 'LC 51',
  'note': '在 n × n 棋盘放置 n 个皇后，任意两个皇后不能同行、同列或同对角线。返回所有布局，每个布局用 n 个字符串表示，Q 是皇后，. 是空格。',
  'example': 'n = 4  →  [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]；n = 1  →  [["Q"]]',
  'code': 'class Solution:\n'
          '    def solveNQueens(self, n):\n'
          '        cols, diag_sum, diag_diff = set(), set(), set()\n'
          '        board = [["."] * n for _ in range(n)]\n'
          '        ans = []\n'
          '\n'
          '        def dfs(row, col):\n'
          '            if row == n:\n'
          '                ans.append(["".join(line) for line in board])\n'
          '                return\n'
          '            if col in cols or row + col in diag_sum or row - col in diag_diff:\n'
          '                return\n'
          '            board[row][col] = "Q"\n'
          '            cols.add(col)\n'
          '            diag_sum.add(row + col)\n'
          '            diag_diff.add(row - col)\n'
          '\n'
          '            for next_col in range(n):\n'
          '                if row == n - 1:\n'
          '                    dfs(row + 1, next_col)  # 棋盘已放满，只记录一次\n'
          '                    break\n'
          '                dfs(row + 1, next_col)      # 下一行逐列试放\n'
          '\n'
          '            board[row][col] = "."\n'
          '            cols.remove(col)\n'
          '            diag_sum.remove(row + col)\n'
          '            diag_diff.remove(row - col)\n'
          '\n'
          '        for col in range(n):\n'
          '            dfs(0, col)\n'
          '        return ans',
  'tips': ['每次递归试放当前行的一个位置，下一层换到下一行，所以不会同行。同列的 col 相同，两种对角线分别用 row+col、row-col 判断。',
           '最后一行放好后，只调用一次下一层。下一层发现 row == n，就保存当前棋盘。回溯时移走皇后，并从三个集合里撤销对应记录。']}],
  'pending': [(46, '全排列'),
              (78, '子集'),
              (17, '电话号码的字母组合'),
              (39, '组合总和'),
              (22, '括号生成'),
              (79, '单词搜索'),
              (131, '分割回文串'),
              (51, 'N 皇后')],
  'summary': ['① 全排列\u3000每层选下一位，选满才收集。\n'
              '② 子集\u3000每到一个节点就收集，从 i+1 继续选。\n'
              '③ 电话号码\u3000每层选一位数字的一个字母。\n'
              '④ 组合总和\u3000从 i 继续选，允许重复使用。\n'
              '⑤ 括号生成\u3000左括号有余额就能放，右括号必须有左括号可配。\n'
              '⑥ 单词搜索\u3000沿相邻格匹配，只限制当前路径的访问。\n'
              '⑦ 分割回文串\u3000每位决定切不切，只有回文才能切。\n'
              '⑧ N 皇后\u3000逐行放，用列和两种对角线排除冲突。',
              '写递归前先定好每层做什么选择、什么时候收集答案。退出某个分支后如果还要继续搜，要恢复共用的路径、标记和棋盘。保存列表答案时要复制。']},
 {'id': 'binary-search',
  'name': '二分查找',
  'problems': [{'title': '二分查找（闭区间模板）',
                'source': 'LC 704',
                'tag': '非 Hot100',
                'note': '升序无重复数组 nums 中找 target，返回下标，不存在返回 -1。',
                'example': 'nums = [-1,0,3,5,9,12], target = 9  →  4（nums[4] 就是 9）',
                'code': 'class Solution:\n'
                        '    def search(self, nums, target):\n'
                        '        left, right = 0, len(nums) - 1   # 搜索区间 [left, '
                        'right]，两端都可能是答案\n'
                        '        while left <= right:             # 闭区间非空就继续\n'
                        '            mid = left + (right - left) // 2\n'
                        '            if nums[mid] == target:\n'
                        '                return mid\n'
                        '            if nums[mid] < target:\n'
                        '                left = mid + 1           # mid 已判过，排除\n'
                        '            else:\n'
                        '                right = mid - 1\n'
                        '        return -1',
                'tips': ['闭区间模板。`[left, right]` 中的两个端点都还可能是答案，循环条件是 `left <= right`。',
 '命中就返回 mid。中点值偏小，丢掉 mid 及它左边的部分，写 `left = mid + 1`。中点值偏大，写 `right = mid - 1`。区间为空就返回 -1。']},
 {'title': '搜索插入位置',
 'source': 'LC 35',
 'note': '给定升序且无重复元素的数组 nums 和目标值 target。找到就返回下标，否则返回按升序插入的位置。',
 'example': 'nums = [1,3,5,6], target = 5  →  2；target = 2  →  1；target = 7  →  4',
 'code': 'class Solution:\n'
         '    def searchInsert(self, nums, target):\n'
         '        left, right = 0, len(nums) - 1\n'
         '        while left <= right:\n'
         '            mid = (left + right) // 2\n'
         '            if target < nums[mid]:\n'
         '                right = mid - 1\n'
         '            elif target > nums[mid]:\n'
         '                left = mid + 1\n'
         '            else:\n'
         '                return mid\n'
         '        return left  # 没找到时，left 就是插入位置',
 'tips': ['和模板一样，搜索闭区间 `[left, right]`，命中立即返回下标。模板找不到时返回 -1，本题返回 `left`。',
          '找不到时，循环结束于 `left == right + 1`。left 左边的值都比 target 小，从 left 开始的值都比 target 大。插在最前面返回 0，插在末尾返回 len(nums)。',
          '时间 O(log n)，额外空间 O(1)。']},
 {'title': '搜索二维矩阵',
 'source': 'LC 74',
 'note': '给定非空矩形矩阵 matrix，每行非递减，下一行的首元素严格大于上一行的尾元素。判断 target 是否在矩阵中。',
 'example': 'matrix = [[1,3,5],[7,9,11]], target = 9  →  True；target = 4  →  False；target = 6  →  False',
 'code': 'class Solution:\n'
         '    def searchMatrix(self, matrix, target):\n'
         '        m, n = len(matrix), len(matrix[0])\n'
         '        top, bottom = 0, m - 1\n'
         '        while top <= bottom:\n'
         '            mid = (top + bottom) // 2\n'
         '            if target < matrix[mid][0]:\n'
         '                bottom = mid - 1     # 目标在本行首元素之前\n'
         '            elif target > matrix[mid][n-1]:\n'
         '                top = mid + 1        # 目标在本行尾元素之后\n'
         '            else:\n'
         '                top = mid            # 唯一可能含有目标的行\n'
         '                break\n'
         '        if top > bottom:\n'
         '            return False\n'
         '\n'
         '        left, right = 0, n - 1\n'
         '        while left <= right:\n'
         '            mid = (left + right) // 2\n'
         '            if target == matrix[top][mid]:\n'
         '                return True\n'
         '            if target < matrix[top][mid]:\n'
         '                right = mid - 1\n'
         '            else:\n'
         '                left = mid + 1\n'
         '        return False',
 'tips': ['模板直接在一个数组里找下标。本题先用行首、行尾对行号做闭区间二分，再按模板在选中的行里找元素，最后返回布尔值。',
          '落在某行首尾之间，只说明目标可能在这一行。比如 4 落在 [1,3,5] 的首尾之间，但行里没有 4。若目标落在两行之间的空档，第一轮就找不到候选行。',
          '时间 O(log m + log n)，额外空间 O(1)。']},
 {'title': '在排序数组中查找元素的第一个和最后一个位置',
 'source': 'LC 34',
 'note': '给定非递减数组 nums 和目标值 target，返回 target 首次和最后一次出现的下标。目标不存在或数组为空时，返回 [-1,-1]。',
 'example': 'nums = [5,7,7,8,8,10], target = 8  →  [3,4]；target = 6  →  [-1,-1]；nums = [], target = 0  →  [-1,-1]',
 'code': 'class Solution:\n'
         '    def searchRange(self, nums, target):\n'
         '        def first_position():\n'
         '            found = False\n'
         '            left, right = 0, len(nums) - 1\n'
         '            while left <= right:\n'
         '                mid = (left + right) // 2\n'
         '                if nums[mid] == target:\n'
         '                    found = True\n'
         '                    right = mid - 1     # 命中后继续向左找\n'
         '                elif nums[mid] > target:\n'
         '                    right = mid - 1\n'
         '                else:\n'
         '                    left = mid + 1\n'
         '            return left if found else -1\n'
         '\n'
         '        def last_position():\n'
         '            found = False\n'
         '            left, right = 0, len(nums) - 1\n'
         '            while left <= right:\n'
         '                mid = (left + right) // 2\n'
         '                if nums[mid] == target:\n'
         '                    found = True\n'
         '                    left = mid + 1      # 命中后继续向右找\n'
         '                elif nums[mid] > target:\n'
         '                    right = mid - 1\n'
         '                else:\n'
         '                    left = mid + 1\n'
         '            return right if found else -1\n'
         '\n'
         '        return [first_position(), last_position()]',
 'tips': ['模板命中就返回。本题允许重复，命中时先记下 found，再继续缩区间。找第一个位置时把相等归到左搜，退出后 left 指向第一个大于等于 target 的位置。找最后一个位置时把相等归到右搜，退出后 right '
          '指向最后一个小于等于 target 的位置。',
          '两个边界下标只有在找到过 target 时才是答案。found 为 False 就返回 -1，空数组也走这一分支。',
          '两次二分合计 O(log n)，额外空间 O(1)。']},
 {'title': '搜索旋转排序数组',
 'source': 'LC 33',
 'note': '给定一个由无重复的升序数组旋转得到的数组 nums，也可能未旋转。返回 target 的下标，不存在时返回 -1。',
 'example': 'nums = [4,5,6,7,0,1,2], target = 0  →  4；target = 3  →  -1',
 'code': 'class Solution:\n'
         '    def search(self, nums, target):\n'
         '        left, right = 0, len(nums) - 1\n'
         '        while left <= right:\n'
         '            mid = (left + right) // 2\n'
         '            if nums[mid] == target:\n'
         '                return mid\n'
         '            if nums[left] <= nums[mid]:         # 左半段有序\n'
         '                if nums[left] <= target < nums[mid]:\n'
         '                    right = mid - 1\n'
         '                else:\n'
         '                    left = mid + 1\n'
         '            else:                              # 右半段有序\n'
         '                if nums[mid] < target <= nums[right]:\n'
         '                    left = mid + 1\n'
         '                else:\n'
         '                    right = mid - 1\n'
         '        return -1',
 'tips': ['和模板一样用闭区间，命中返回下标，找不到返回 -1。模板的整个区间都升序，比较 nums[mid] 和 target 就能选方向。旋转后要先用端点找出有序半段，再看 target 是否落在这半段的值域内。',
          '有序半段的外侧端点要计入值域。mid 已经判过，所以靠 mid 的一侧用严格不等号。无重复元素保证这里能判断哪一半有序。',
          '时间 O(log n)，额外空间 O(1)。']},
 {'title': '寻找旋转排序数组中的最小值',
 'source': 'LC 153',
 'note': '给定非空数组 nums，它由无重复的升序数组旋转得到，也可能未旋转。返回最小元素。',
 'example': 'nums = [4,5,6,7,0,1,2]  →  0；nums = [1,2,3]  →  1；nums = [7]  →  7',
 'code': 'class Solution:\n'
         '    def findMin(self, nums):\n'
         '        left, right = 0, len(nums) - 1\n'
         '        while left < right:                  # 只剩一个候选位置时结束\n'
         '            mid = (left + right) // 2\n'
         '            if nums[mid] <= nums[right]:\n'
         '                right = mid                  # mid 本身可能是最小值\n'
         '            else:\n'
         '                left = mid + 1               # 右边至少有一个更小的值\n'
         '        return nums[left]',
 'tips': ['模板比较 nums[mid] 和 target。本题没有 target，改比 nums[mid] 和 '
          'nums[right]。中点值比右端小，说明中点到右端这一段有序，最小值在中点或其左边。中点值比右端大，说明最小值在中点右边。',
          '模板两边都排除已检查的 mid。本题缩右端时保留 mid，写 `right = mid`。循环用 `left < right`，候选缩到一个位置就返回该位置的值。',
          '时间 O(log n)，额外空间 O(1)。']},
 {'title': '寻找两个正序数组的中位数',
 'source': 'LC 4',
 'note': '给定两个非递减数组 nums1、nums2，至少有一个非空。返回合在一起后的中位数。总长度为奇数时取中间值，为偶数时取中间两值的平均数。',
 'example': 'nums1 = [1,3], nums2 = [2]  →  2；nums1 = [1,2], nums2 = [3,4]  →  2.5；nums1 = [], nums2 = [4]  →  4',
 'code': 'class Solution:\n'
         '    def findMedianSortedArrays(self, nums1, nums2):\n'
         '        m, n = len(nums1), len(nums2)\n'
         '        half = (m + n + 1) // 2              # 左半边需要放的元素个数\n'
         '\n'
         '        def val(nums, i):\n'
         '            if i < 0:\n'
         '                return float("-inf")         # 左边没有元素\n'
         '            if i >= len(nums):\n'
         '                return float("inf")          # 右边没有元素\n'
         '            return nums[i]\n'
         '\n'
         '        left, right = 0, m - 1\n'
         '        while left <= right:\n'
         '            mid = (left + right) // 2\n'
         '            take1 = mid + 1\n'
         '            take2 = half - take1\n'
         '            if val(nums1, mid) <= val(nums2, take2):\n'
         '                left = mid + 1               # 还能尝试从 nums1 多取一些\n'
         '            else:\n'
         '                right = mid - 1              # nums1 取太多，向左收缩\n'
         '\n'
         '        take1 = right + 1                    # nums1 最多能放进左半边的个数\n'
         '        take2 = half - take1\n'
         '        left_max = max(val(nums1, take1 - 1), val(nums2, take2 - 1))\n'
         '        if (m + n) % 2 != 0:\n'
         '            return left_max\n'
         '        right_min = min(val(nums1, take1), val(nums2, take2))\n'
         '        return (left_max + right_min) / 2',
 'tips': ['模板二分的是 target 的下标。本题二分的是分割位置。若从 nums1 左边取 i 个，就必须从 nums2 左边取 j = half - i 个。两个左段合起来放满左半边。',
          '比较 nums1 左边最后一个和 nums2 右边第一个。前者 ≤ 后者时，继续尝试多取一个。随着 i 增大，前者不会变小、后者不会变大，所以能用二分找到最后一个满足条件的位置。如果 nums1 还能取，再取一个就会让 nums1 '
          '右边第一个大于 nums2 左边最后一个，因此当前分割也满足另一侧的大小关系。若 nums1 已取完，它的右边按正无穷处理。',
          '和模板命中即返回不同，本题循环结束后用 right + 1 得到 nums1 左段长度。缺少左侧元素按负无穷处理，缺少右侧元素按正无穷处理。奇数取左半最大值，偶数再和右半最小值求平均。',
          '在 nums1 上做二分，耗时 O(1 + log(m + 1))，额外空间 O(1)。nums1 为空时直接由边界算出结果。']}],
  'pending': [(35, '搜索插入位置'),
              (74, '搜索二维矩阵'),
              (34, '在排序数组中查找元素的第一个和最后一个位置'),
              (33, '搜索旋转排序数组'),
              (153, '寻找旋转排序数组中的最小值'),
              (4, '寻找两个正序数组的中位数')],
  'summary': ['① 搜索插入位置\u3000没找到时返回 left。\n'
   '② 搜索二维矩阵\u3000先找可能的行，再在行内查找。\n'
   '③ 查找首尾位置\u3000命中后继续向对应的边界收缩。\n'
   '④ 搜索旋转排序数组\u3000先识别有序半段，再按值域选方向。\n'
   '⑤ 找旋转数组的最小值\u3000和右端比较，向左收缩时保留 mid。\n'
   '⑥ 寻找两个正序数组的中位数\u3000二分左半边从第一个数组取多少个。',
   '以 LC 704 的闭区间为起点。写每一道变形前，先确定二分找的是什么，mid 是否仍可能是答案，以及循环结束后该返回什么。']},
 {'id': 'stack',
  'name': '栈',
  'problems': [{'title': '有效的括号',
  'source': 'LC 20',
  'note': '给定只含 ()、[]、{} 六种字符的字符串 s，判断括号是否全部按正确类型和嵌套顺序闭合。',
  'example': 's = "([])"  →  True；s = "([)]"  →  False；s = "("  →  False',
  'code': 'class Solution:\n'
          '    def isValid(self, s):\n'
          '        pairs = {"(": ")", "[": "]", "{": "}"}\n'
          '        stack = []\n'
          '        for ch in s:\n'
          '            if ch in pairs:\n'
          '                stack.append(ch)  # 左括号入栈，等待闭合\n'
          '            elif not stack or pairs[stack.pop()] != ch:\n'
          '                return False      # 无左括号可配对，或栈顶类型不匹配\n'
          '        return not stack          # 所有左括号都必须已闭合',
  'tips': ['右括号只能匹配最近一个尚未闭合的左括号。`not stack or ...` 先判断栈空，短路时不会调用 `pop()`。', '时间 O(n)，额外空间 O(n)。']},
 {'title': '最小栈',
  'source': 'LC 155',
  'note': '实现 MinStack，支持入栈、出栈、查看栈顶和取最小值，每个操作要求 O(1)。pop、top、getMin 只在栈非空时调用。',
  'example': '操作 = ["MinStack","push","push","push","getMin","pop","getMin","pop","top"]；参数 = '
             '[[],[3],[1],[1],[],[],[],[],[]]  →  [null,null,null,null,1,null,1,null,3]（null 对应构造或无返回值的操作）',
  'code': 'class MinStack:\n'
          '    def __init__(self):\n'
          '        self.stack = []\n'
          '        self.min_stack = []\n'
          '\n'
          '    def push(self, value):\n'
          '        if not self.min_stack or self.min_stack[-1] >= value:\n'
          '            self.min_stack.append(value)  # 相等的最小值也分别入栈\n'
          '        self.stack.append(value)\n'
          '\n'
          '    def pop(self):\n'
          '        value = self.stack.pop()\n'
          '        if value == self.min_stack[-1]:\n'
          '            self.min_stack.pop()          # 同步移除这一次最小值\n'
          '\n'
          '    def top(self):\n'
          '        return self.stack[-1]\n'
          '\n'
          '    def getMin(self):\n'
          '        return self.min_stack[-1]',
  'tips': ['辅助栈的栈顶始终是当前最小值。两个 1 都入栈时，弹出一个 1 后另一个 1 仍是最小值，所以条件要包含相等。',
           '各操作摊还 O(1)，其中 top、getMin 直接取末尾，为 O(1)。辅助栈额外空间最坏 O(n)。']},
 {'title': '字符串解码',
  'source': 'LC 394',
  'note': '给定合法编码字符串 s，k[片段] 表示将片段重复 k 次。k 为正整数，可以有多位，方括号可以嵌套。返回解码后的字符串。',
  'example': 's = "3[a2[c]]"  →  "accaccacc"；s = "10[a]b"  →  "aaaaaaaaaab"',
  'code': 'class Solution:\n'
          '    def decodeString(self, s):\n'
          '        stack = []\n'
          '        cur = ""\n'
          '        num = 0\n'
          '        for ch in s:\n'
          '            if ch.isdigit():\n'
          '                num = num * 10 + int(ch)  # 累积多位重复次数\n'
          '            elif ch == "[":\n'
          '                stack.append((cur, num))   # 保存外层已解码前缀和重复次数\n'
          '                cur = ""\n'
          '                num = 0\n'
          '            elif ch == "]":\n'
          '                prev, k = stack.pop()\n'
          '                cur = prev + cur * k      # 展开当前层，接回外层前缀\n'
          '            else:\n'
          '                cur += ch\n'
          '        return cur',
  'tips': ['`cur` 是当前层已解码的内容，`num` 是下一个左方括号前的重复次数。读到右方括号时，先完成最近打开的一层。',
           '题目中的数字是 0 到 9，可直接用 `isdigit()` 和 `int(ch)`。字符串重复和拼接会复制字符，嵌套时同一段内容可能复制多次，耗时要计入这些复制。']},
 {'title': '每日温度',
  'source': 'LC 739',
  'note': '给定每天的温度 temperatures，返回每一天要等几天才会遇到严格更高的温度。之后没有更高温度时填 0。',
  'example': 'temperatures = [73,74,75,71,69,72,76,73]  →  [1,1,4,2,1,1,0,0]；temperatures = [70,70,71]  →  [2,1,0]',
  'code': 'class Solution:\n'
          '    def dailyTemperatures(self, temperatures):\n'
          '        stack = []\n'
          '        ans = [0] * len(temperatures)\n'
          '        for i, temp in enumerate(temperatures):\n'
          '            while stack and temp > stack[-1][0]:\n'
          '                _, prev_i = stack.pop()    # 今天是 prev_i 右侧第一个更暖的日子\n'
          '                ans[prev_i] = i - prev_i\n'
          '            stack.append([temp, i])        # 记录还在等待升温的日期\n'
          '        return ans',
  'tips': ['这里在等更暖的一天，栈内温度从底到顶越来越低，允许相等。新温度高于栈顶就弹出，直到栈空或栈顶温度大于等于新温度，再把今天入栈。',
           '比如栈里从底到顶是 `[76, 73, 71]`，今天是 74。先弹 71，再弹 73，因为 74 比它们都高。遇到 76 停下，入栈后是 `[76, 74]`。今天就是被弹出那两天右边第一次升温的日子。',
           '相同温度不算升温。遍历完还在栈里的日期没有等到更高温度，答案保留为 0。每个下标至多入栈和出栈各一次，时间 O(n)，辅助空间 O(n)。']},
 {'title': '柱状图中最大的矩形',
  'source': 'LC 84',
  'note': '给定非负整数数组 heights，每根柱子宽度为 1。返回由连续柱子围成的最大矩形面积，矩形高度不能超过覆盖范围内的最低柱子。',
  'example': 'heights = [2,1,5,6,2,3]  →  10（高度 5、宽度 2）；heights = [2,2,2]  →  6',
  'code': 'class Solution:\n'
          '    def largestRectangleArea(self, heights):\n'
          '        n = len(heights)\n'
          '        left = [-1] * n\n'
          '        right = [n] * n\n'
          '        stack = []\n'
          '        for i, h in enumerate(heights):\n'
          '            while stack and h < stack[-1][1]:\n'
          '                j, _ = stack.pop()\n'
          '                right[j] = i                # j 右侧第一个严格更矮的位置\n'
          '            if stack:\n'
          '                left[i] = stack[-1][0]      # i 左侧最近一个不高于 h 的位置\n'
          '            stack.append([i, h])            # 栈内高度从底到顶非递减\n'
          '        ans = 0\n'
          '        for i in range(n):\n'
          '            width = right[i] - left[i] - 1  # 两侧边界都不计入宽度\n'
          '            ans = max(ans, heights[i] * width)\n'
          '        return ans',
  'tips': ['递增单调栈从栈底往栈顶看，数值从小到大。本题允许相等，准确说是非递减。新柱子比栈顶矮，就先把栈顶弹掉。一直弹到栈空，或剩下的栈顶不高于新柱子，才让新柱子入栈。弹出的都比新柱子高，留下的都不高于新柱子。',
           '比如栈里从底到顶是 `[2, 4, 6, 8]`，新柱子高度是 5。先弹 8，再弹 6，因为它们都比 5 高。遇到 4 停下，因为 `4 <= 5`。把 5 放进去，栈就变成 `[2, 4, 5]`。',
           '对弹出的 8 和 6，右边第一个严格更矮的柱子都是 5。对新入栈的 5，左边最近一个不高于它的柱子是留下来的栈顶 4。找不到左、右边界时，分别用 -1 和 n。',
           '本题只弹出比新柱子高的柱子，等高会一起留在栈里。后面的等高柱可能被左边的同高柱挡住。看任意一个矩形，取其中最靠左的最低柱子，它算出的宽度就能覆盖整个矩形。',
           '每根柱子至多入栈和出栈各一次。时间 O(n)，辅助空间 O(n)。']}],
  'pending': [(20, '有效的括号'),
              (155, '最小栈'),
              (394, '字符串解码'),
              (739, '每日温度'),
              (84, '柱状图中最大的矩形')],
  'summary': ['① 有效的括号\u3000左括号入栈，右括号匹配栈顶。\n'
   '② 最小栈\u3000辅助栈保存当前及历史最小值，相等的最小值也入栈。\n'
   '③ 字符串解码\u3000遇到左方括号保存外层状态，遇到右方括号展开并接回。\n'
   '④ 每日温度\u3000当前温度严格更高时弹栈，等待天数是两个下标之差。\n'
   '⑤ 最大矩形\u3000当前柱子严格更矮时弹栈，宽度是 `right[i] - left[i] - 1`。',
   '先确定栈里保存什么，再写出何时弹栈。单调栈题要分清比较是否包含相等，以及遍历结束时栈内元素的含义。']},
 {'id': 'heap',
  'name': '堆',
  'problems': [{'title': '数组中的第 k 个最大元素',
                'source': 'LC 215',
                'note': '返回 nums 排序后第 k 大的元素（按位置算，不是第 k 个不同值）。',
                'example': 'nums = [3,2,1,5,6,4], k = 2  →  5（降序 6,5,4,3,2,1，第 2 个是 5）',
                'code': 'import heapq\n'
                        '\n'
                        'class Solution:\n'
                        '    def findKthLargest(self, nums, k):\n'
                        '        h = []                               # 小根堆，只留当前最大的 k 个\n'
                        '        for i in nums:\n'
                        '            if len(h) < k:\n'
                        '                heapq.heappush(h, i)         # 前 k 个先填满\n'
                        '            else:\n'
                        '                if i > h[0]:                 # 堆顶是这 k '
                        '个里最小的，比它大才换\n'
                        '                    heapq.heappop(h)\n'
                        '                    heapq.heappush(h, i)\n'
                        '        return h[0]                          # 堆顶就是第 k 大'},
               {'title': '前 K 个高频元素',
                'source': 'LC 347',
                'note': '返回 nums 中出现频率最高的 k 个元素，顺序任意。',
                'example': 'nums = [1,1,1,2,2,3], k = 2  →  [1,2]（1 出现 3 次，2 出现 2 次）',
                'code': 'import heapq\n'
                        'from collections import defaultdict\n'
                        '\n'
                        'class Solution:\n'
                        '    def topKFrequent(self, nums, k):\n'
                        '        freq = defaultdict(int)\n'
                        '        for num in nums:\n'
                        '            freq[num] += 1                    # 缺键自动补 0，可以直接 +1\n'
                        '\n'
                        '        h = []                                # 小根堆存 (频率, 元素)，堆顶是 '
                        'k 个里最冷门的\n'
                        '        for num, count in freq.items():\n'
                        '            if len(h) < k:\n'
                        '                heapq.heappush(h, (count, num))\n'
                        '            else:\n'
                        '                if h[0][0] < count:           # 比堆顶频率高才够格替换\n'
                        '                    heapq.heapreplace(h, (count, num))\n'
                        '        return [num for count, num in h]      # 题目允许任意顺序，不用再排'},
               {'title': '数据流的中位数',
                'source': 'LC 295',
                'note': '数据流里不断加入整数，随时返回当前所有元素的中位数。',
                'example': 'addNum(1) → addNum(2) → findMedian() = 1.5；再 addNum(3) → '
                           'findMedian() = 2.0',
                'code': 'import heapq\n'
                        '\n'
                        'class MedianFinder:\n'
                        '    def __init__(self):\n'
                        '        self.l = []                # 大根堆（存负数），装较小的一半\n'
                        '        self.r = []                # 小根堆，装较大的一半\n'
                        '\n'
                        '    def addNum(self, num):\n'
                        '        heapq.heappush(self.l, -num)             # 先无脑进左堆\n'
                        '        if len(self.l) - len(self.r) > 1:        # 左边多出 2 '
                        '个，挪一个过去\n'
                        '            a = heapq.heappop(self.l)\n'
                        '            heapq.heappush(self.r, -a)\n'
                        '        if self.l and self.r and -self.l[0] > self.r[0]:   # 左堆最大 '
                        '> 右堆最小\n'
                        '            b = heapq.heappop(self.l)            # 交换两个堆顶，恢复有序\n'
                        '            c = heapq.heappop(self.r)\n'
                        '            heapq.heappush(self.r, -b)\n'
                        '            heapq.heappush(self.l, -c)\n'
                        '\n'
                        '    def findMedian(self):\n'
                        '        m = len(self.l)\n'
                        '        n = len(self.r)\n'
                        '        if (m + n) % 2 == 0:                     # 偶数个，两个堆顶取平均\n'
                        '            return (self.r[0] - self.l[0]) / 2   # l 存的是负数，所以是相减\n'
                        '        else:                                    # 奇数个，左堆多一个\n'
                        '            return -self.l[0]'}],
  'summary': ['① 第 k 大：完全不用把数排好，只要盯住「目前最大的那几个」，让这几个里最差的那个守在门口，新来的比它强就换掉它，最后站在门口的就是第 k 大。\n'
              '② 前 k 高频：先数一遍每个数出现几次，再用同一招只留「出现最多的 k 个」，只不过比较的是次数、不是数值本身。\n'
              '③ 中位数：把所有数从中间掰成两半，小的一半放左边、大的一半放右边，只要两边数量差不超过一个，中位数就永远卡在两半的交界上。',
              '堆只维护局部顺序，便于反复取最小或最大边界。第 k 大与前 k 高频用大小至多为 k 的小根堆淘汰候选，中位数用两个堆维护两半的边界和数量。小 k '
              '或持续插入时很合适；不保证任何规模下都比一次排序快。'],
  'pending': [(215, '数组中的第 K 个最大元素'), (347, '前 K 个高频元素'), (295, '数据流的中位数')]},
 {'id': 'greedy',
  'name': '贪心算法',
  'problems': [{'title': '买卖股票的最佳时机',
                'source': 'LC 121',
                'note': '给定每天股价 prices，只能买卖一次（先买后卖），返回能拿到的最大利润；赚不到就返回 0。',
                'example': 'prices = [7,1,5,3,6,4]  →  5（第 2 天 1 买入，第 5 天 6 卖出）',
                'code': 'class Solution:\n'
                        '    def maxProfit(self, prices):\n'
                        '        n = len(prices)\n'
                        '        a = prices[-1]                    # 循环开始时 a = i 之后的最高价\n'
                        '        ans = 0\n'
                        '        for i in range(n - 2, -1, -1):    # 从倒数第二天倒着往前扫\n'
                        '            b = a - prices[i]             # 第 i 天买、后面最高价卖，能赚多少\n'
                        '            ans = max(ans, b)             # ans 初值 0，亏损自然被挡掉\n'
                        '            a = max(a, prices[i])         # 把第 i 天也算进后缀最高价\n'
                        '        return ans'},
               {'title': '跳跃游戏',
                'source': 'LC 55',
                'note': '给定每个位置能跳的最大步数 nums，从下标 0 出发，判断能不能到达最后一个下标。',
                'example': 'nums = [2,3,1,1,4]  →  true；nums = [3,2,1,0,4]  →  false（下标 3 '
                           '只能跳 0 步，卡死）',
                'code': 'class Solution:\n'
                        '    def canJump(self, nums):\n'
                        '        maxpos = 0                            # 当前能到达的最远下标\n'
                        '        for i in range(len(nums)):\n'
                        '            if i > maxpos:                    # 连 i 都到不了，后面更到不了\n'
                        '                return False\n'
                        '            maxpos = max(maxpos, i + nums[i]) # 用 i 起跳，更新最远可达\n'
                        '            if maxpos >= len(nums) - 1:       # 已经够到最后一位，直接赢\n'
                        '                return True'},
               {'title': '跳跃游戏 II',
                'source': 'LC 45',
                'note': '同上一个数组 nums，返回跳到最后一个下标所需的最少跳跃次数；题目保证一定到得了。',
                'example': 'nums = [2,3,1,1,4]  →  2（0 → 1 → 4，两步到位）',
                'code': 'class Solution:\n'
                        '    def jump(self, nums):\n'
                        '        ans = 0                               # 已跳的步数\n'
                        '        end = 0                               # 当前这一跳能覆盖的右边界\n'
                        '        maxpos = 0                            # 下一跳能到达的最远处\n'
                        '        for i in range(len(nums) - 1):        # '
                        '不用看最后一位，站在它上面就结束了\n'
                        '            maxpos = max(maxpos, i + nums[i]) # 边扫边扩下一跳的范围\n'
                        '            if i == end:                      # 走到本层边界，必须再跳一次\n'
                        '                ans += 1\n'
                        '                end = maxpos\n'
                        '        return ans'},
               {'title': '划分字母区间',
                'source': 'LC 763',
                'note': '把字符串切成尽量多的段，同一个字母只能出现在一段里，返回每段的长度。',
                'example': 's = "ababcbacadefegdehijhklij"  →  [9,7,8]（切成 ababcbaca / '
                           'defegde / hijhklij）',
                'code': 'class Solution:\n'
                        '    def partitionLabels(self, s):\n'
                        '        start = -1                     # 上一段的结尾，第一段之前当作 -1\n'
                        '        maxpos = 0                     # 当前这一段至少要延伸到哪\n'
                        '        ans = []\n'
                        '        last = {c: i for i, c in enumerate(s)}   # 每个字母最后一次出现的下标\n'
                        '        for i in range(len(s)):\n'
                        '            if i > maxpos:             # 越过上一段结尾，上一段可以封闭了\n'
                        '                ans.append(maxpos - start)   # 段长 = 本段结尾 - 上段结尾\n'
                        '                start = maxpos\n'
                        '            if i == len(s) - 1:        # 最后一段没有下一段来触发，就地收尾\n'
                        '                ans.append(i - start)\n'
                        '            j = last[s[i]]\n'
                        '            maxpos = max(maxpos, j)    # 本段必须盖住 s[i] 最后的出现位置\n'
                        '        return ans',
                'tips': ['j 的两种找法，效果完全一样：',
                         '哈希版 `j = last[s[i]]` —— 先花 O(n) 建一次表，之后每个字符平均 O(1) 查，总 '
                         'O(n)；代价是多一个 dict。',
                         '库函数版 `j = s.rfind(s[i])` —— 不建表，每次在整串中倒着查找，单次 O(n)，整体最坏 '
                         'O(n²)；代码少一行，n 小的时候随便用。']}],
  'summary': ['① 买卖股票：与其对每一天都往后找最高价，不如倒着走，一边走一边记住「后面见过的最高价」，拿它减去当天的价钱，就是这天买入能赚多少。\n'
              '② 跳跃游戏：不用管具体跳哪几步，只跟住「目前最远能到哪儿」，路过一个位置就试着把这个距离往外推一推；一旦有个位置自己都够不着，后面全废。\n'
              '③ 最少步数：在上一题基础上多记一件事——这一跳管到哪儿为止，走到边界就必须再跳，跳一次就往外扩一层，扩了几层就是走了几步。\n'
              '④ 划分区间：既然一个字母不许跨两段，这一段就得盖住段内所有字母的最后出现位置，所以边扫边把结尾往后推，推不动了就切一刀。',
              '这四题都能用已扫描的信息更新状态，但状态不只一个数。股票维护后缀最高价与答案；跳跃游戏维护最远可达位置；最少跳数还维护当前层边界和步数；划分区间先记录每个字母的最后位置，再维护本段边界。贪心需要证明局部选择不会损害全局结果，不能只看题目是否问最值。例如硬币 '
              '1、3、4 凑 6，优先拿最大面额需 3 枚，最优却是两个 3。'],
  'pending': []},
 {'id': 'dp',
 'name': '动态规划',
 'problems': [{'title': '爬楼梯',
               'source': 'LC 70',
               'note': '共有 n 级台阶，每次可以爬 1 级或 2 级，返回爬到楼顶的不同走法数（n 为正整数）。',
               'example': 'n = 3  →  3（1+1+1、1+2、2+1 是三种不同走法）',
               'code': 'class Solution:\n'
                       '    def climbStairs(self, n):\n'
                       '        dp = [0] * (n + 1)             # dp[i] 表示爬到第 i 级台阶的走法数\n'
                       '        dp[0] = 1                      # 不走任何一步算一种空方案，作为递推起点\n'
                       '        dp[1] = 1                      # 爬到第 1 级只有一种走法\n'
                       '        for i in range(2, n + 1):       # 从小到大填表，自下而上计算\n'
                       '            dp[i] = dp[i - 1] + dp[i - 2]  # 转移 dp[i] = dp[i-1] + '
                       'dp[i-2]\n'
                       '        return dp[n]                   # 爬到第 n 级的走法总数',
               'tips': ['自下而上：先确定 `dp[0]`、`dp[1]`，再依次算到 `dp[n]`。时间 O(n)，额外空间 O(n)。']},
              {'title': '杨辉三角',
               'source': 'LC 118',
               'note': '给定行数 numRows，返回杨辉三角的前 numRows 行；每行两端都是 1，中间每个数等于上一行相邻两个数之和。',
               'example': 'numRows = 3  →  [[1],[1,1],[1,2,1]]',
               'code': 'class Solution:\n'
                       '    def generate(self, numRows):\n'
                       '        ans = []                           # 保存每一行，行号从 0 开始\n'
                       '        for i in range(numRows):\n'
                       '            ans.append([1] * (i + 1))       # 第 i 行有 i+1 个数，先全部填成 '
                       '1\n'
                       '        for i in range(2, numRows):         # 前两行已正确，从第三行开始补中间\n'
                       '            for j in range(1, i):          # 跳过每行两端，端点始终为 1\n'
                       '                # 转移 ans[i][j] = ans[i-1][j-1] + ans[i-1][j]\n'
                       '                ans[i][j] = ans[i-1][j-1] + ans[i-1][j]\n'
                       '        return ans                         # 返回包含所有行的二维列表',
               'tips': ['每行都用 `[1] * (i + 1)` 单独创建，避免多行共用同一个列表。时间和保存结果所需的空间均为 '
                        'O(numRows²)。']},
              {'title': '打家劫舍',
               'source': 'LC 198',
               'note': '非空数组 nums 记录一排房屋中的非负金额，不能同时偷相邻两间房，返回能偷到的最大总金额。',
               'example': 'nums = [2,7,9,3,1]  →  12（偷第 1、3、5 间，2+9+1 = 12）',
               'code': 'class Solution:\n'
                       '    def rob(self, nums):\n'
                       '        dp = [0] * (len(nums) + 1)      # dp[k] 是前 k 间房的最大金额，dp[0] '
                       '为 0\n'
                       '        dp[1] = nums[0]                # 前 1 间房的答案，对应 nums 的下标 0\n'
                       '        for i in range(1, len(nums)):   # i 是房屋下标，从第 2 间开始处理\n'
                       '            # 转移 dp[i+1] = max(dp[i], dp[i-1] + nums[i])\n'
                       '            dp[i+1] = max(dp[i], dp[i-1] + nums[i])\n'
                       '        return dp[-1]                  # 前 len(nums) 间，也就是全部房屋的答案',
               'tips': ['`dp` 比 `nums` 多一位：`nums[i]` 是第 i+1 间房，`dp[i]` 只考虑前 i 间，`dp[i+1]` '
                        '才包含当前房。不偷当前房取 `dp[i]`；偷当前房取 `dp[i-1] + nums[i]`，避免偷相邻房屋。',
                        '边界是 `dp[0] = 0`、`dp[1] = nums[0]`；题目保证 nums 非空，只有一间时循环不执行，直接返回 '
                        '`dp[1]`。时间 O(n)，额外空间 O(n)。']},
              {'title': '完全平方数',
               'source': 'LC 279',
               'note': '给定正整数 n，返回和为 n 的完全平方数的最少个数；同一个平方数可以重复使用。',
               'example': 'n = 12  →  3（4+4+4）；n = 13  →  2（4+9）',
               'code': 'import math\n'
                       '\n'
                       'class Solution:\n'
                       '    def numSquares(self, n):\n'
                       '        dp = [float("inf")] * (n + 1)  # dp[i] 是凑出 i 的最少个数，先设为无穷大\n'
                       '        dp[0] = 0                      # 凑出 0 不需要任何平方数\n'
                       '        for i in range(1, n + 1):       # 从小到大填表，自下而上计算\n'
                       '            for j in range(1, math.isqrt(i) + 1):  # 枚举不超过 i 的平方数 '
                       'j**2\n'
                       '                # 转移 dp[i] = 1 + min(dp[i-j**2])，遍历 1 <= j <= '
                       'isqrt(i)\n'
                       '                dp[i] = min(dp[i], dp[i - j**2] + 1)\n'
                       '        return dp[-1]                  # 最后一项就是凑出 n 的最少个数',
               'tips': ['`math.isqrt(i)` 是向下取整的整数平方根；range 右端加 1 才能枚举到它。`j ** 2` 是 j '
                        '的平方，`^` 是异或，不能替代乘方。',
                        '下面的 DP 类封装写法仍按 j = 1..n 计算，属于自下而上，不是记忆化递归。`get()` '
                        '是这里自定义的方法；负下标返回无穷大，用来排除超过当前金额的平方数。两种写法的时间均为 O(n√n)，额外空间均为 O(n)。'],
               'alt_title': '补充写法：DP 类封装（仍为自下而上）',
               'alt_code': 'import math\n'
                           '\n'
                           'class Solution:\n'
                           '    def numSquares(self, n):\n'
                           '        class DP:\n'
                           '            def __init__(self, n):\n'
                           '                self.dp = [0] * (n + 1)  # 保存各个状态，dp[0] 为 0\n'
                           '            def get(self, x):\n'
                           '                if x < 0:\n'
                           '                    return float("inf")  # 余数为负，这个平方数不能选\n'
                           '                else:\n'
                           '                    return self.dp[x]    # 返回此前已经算出的状态\n'
                           '        dp = DP(n)\n'
                           '        m = math.isqrt(n)                # 枚举的平方根上界\n'
                           '        for j in range(1, n + 1):        # 仍然从小状态算到大状态\n'
                           '            # 转移（取所有合法剩余金额的最小值，再加 1）\n'
                           '            dp.dp[j] = min(dp.get(j - i**2) for i in range(1, '
                           'm + 1)) + 1\n'
                           '        return dp.dp[n]                  # 每次转移相当于再选一个平方数'},
              {'title': '零钱兑换',
               'source': 'LC 322',
               'note': '给定正整数硬币面额数组 coins 和非负金额 amount，每种硬币可无限使用；返回凑出 amount '
                       '所需的最少硬币数，无法凑出则返回 -1。',
               'example': 'coins = [1,2,5], amount = 11  →  3（5+5+1）；coins = [2], amount = '
                          '3  →  -1；amount = 0  →  0',
               'code': 'class Solution:\n'
                       '    def coinChange(self, coins, amount):\n'
                       '        dp = [float("inf")] * (amount + 1)  # dp[i] 是凑出金额 i '
                       '的最少硬币数\n'
                       '        dp[0] = 0                          # 凑出 0 元不需要硬币\n'
                       '        for i in range(1, amount + 1):      # 从小金额开始，自下而上填表\n'
                       '            for j in coins:                # j 是硬币面额，不是数组下标\n'
                       '                if j <= i:                 # 面额不超过当前金额，才考虑选它\n'
                       '                    # 转移 dp[i] = 1 + min(dp[i-j])，遍历 coins 中 j <= '
                       'i\n'
                       '                    dp[i] = min(dp[i-j] + 1, dp[i])\n'
                       '        return dp[amount] if dp[amount] != float("inf") else -1  # '
                       '无解时返回 -1',
               'tips': ['`dp[i-j]` 中可能已经使用过面额 j，因此同一种硬币可以重复选。无穷大表示不可达状态，加 1 '
                        '后仍为无穷大，不会覆盖有限的最优解。',
                        'amount = 0 时循环不执行，直接返回 `dp[0] = 0`。时间 O(amount × len(coins))，额外空间 '
                        'O(amount)。']},
              {'title': '单词拆分',
               'source': 'LC 139',
               'note': '给定字符串 s 和词典 wordDict，判断能否按原顺序用词典中的单词拼成整个 s；单词可以重复使用，不能遗漏字符。',
               'example': 's = "leetcode", wordDict = ["leet","code"]  →  '
                          'True（leet+code）；同一词典下 s = "leetcodes"  →  False',
               'code': 'class Solution:\n'
                       '    def wordBreak(self, s, wordDict):\n'
                       '        n = len(s)\n'
                       '        dp = [False] * (n + 1)         # dp[i] 表示前 i 个字符 s[:i] '
                       '能否拼出\n'
                       '        dp[0] = True                  # 空前缀可以拼出，作为递推起点\n'
                       '        for i in range(1, n + 1):      # 从短前缀开始，自下而上判断\n'
                       '            for word in wordDict:     # 尝试把 word 放在当前前缀的末尾\n'
                       '                j = i - len(word)     # 若末尾放 word，它的起点就是 j\n'
                       '                # 转移 dp[i] = OR(dp[j] and s[j:i] == word)，仅取 j >= '
                       '0\n'
                       '                if j >= 0 and dp[j] and s[j:i] == word:\n'
                       '                    dp[i] = True      # 前 j 个字符能拼出，末尾单词也完全匹配\n'
                       '                    break             # 当前前缀已可拼出，不用再试其他单词\n'
                       '        return dp[n]                  # 判断整个字符串，而不只是其中一段',
               'tips': ['`dp` 长度为 n+1，索引表示字符个数。`s[j:i]` 左闭右开，长度为 i-j；先检查 j >= 0，再判断前缀 '
                        '`dp[j]` 和末尾单词是否匹配。',
                        '设 n 为字符串长度、m 为词典大小、L 为最长单词长度，最坏时间 O(n × m × L)，其中包含切片和字符串比较的耗时；空间 '
                        'O(n)。']},
              {'title': '最长递增子序列',
               'source': 'LC 300',
               'note': '给定整数数组 nums，返回最长严格递增子序列的长度；可以跳过元素，但必须保留原有顺序，相等的数不能接在一起。',
               'example': 'nums = [10,9,2,5,3,7,101,18]  →  4（例如 2,3,7,101）；nums = '
                          '[2,2,2]  →  1',
               'code': 'class Solution:\n'
                       '    def lengthOfLIS(self, nums):\n'
                       '        n = len(nums)\n'
                       '        dp = [1] * n                   # dp[i] 是以 nums[i] '
                       '结尾的最长长度，至少有自己\n'
                       '        for i in range(n):             # 依次确定每个结尾位置的答案\n'
                       '            for j in range(i):         # 尝试接在前面的 nums[j] 后面\n'
                       '                if nums[i] > nums[j]:  # 必须严格变大，相等不能接\n'
                       '                    # 转移 dp[i] = max({1} ∪ {dp[j]+1 | j < i 且 '
                       'nums[j] < nums[i]})\n'
                       '                    dp[i] = max(dp[i], dp[j] + 1)\n'
                       '        return max(dp) if nums else 0  # 最优序列可在任意位置结尾；空数组返回 0',
               'tips': ['`dp[i]` 必须以 `nums[i]` 结尾，不是整个前缀的最优长度。例如 nums = [1,2,3,0] 时，dp = '
                        '[1,2,3,1]，答案是 `max(dp) = 3`，不是最后一项。',
                        '时间 O(n²)，额外空间 O(n)。空数组时 dp 也为空，先判断 nums，避免对空列表调用 max。']},
              {'title': '乘积最大子数组',
               'source': 'LC 152',
               'note': '给定非空整数数组 nums，找出乘积最大的非空连续子数组，返回这个最大乘积；数组可含负数和 0。',
               'example': 'nums = [2,3,-2,4]  →  6（子数组 [2,3]）；nums = [-2,3,-4]  →  '
                          '24（整段相乘）',
               'code': 'class Solution:\n'
                       '    def maxProduct(self, nums):\n'
                       '        n = len(nums)\n'
                       '        min_n = [0] * n                # min_n[i] 是以 nums[i] '
                       '结尾的最小乘积\n'
                       '        max_n = [0] * n                # max_n[i] 是以 nums[i] '
                       '结尾的最大乘积\n'
                       '        min_n[0] = nums[0]             # 非空子数组，第一项只能取 nums[0]\n'
                       '        max_n[0] = nums[0]\n'
                       '        for i in range(1, n):\n'
                       '            # 令 x = nums[i]，C = {x, x*max_n[i-1], x*min_n[i-1]}\n'
                       '            # 转移 max_n[i] = max(C)，min_n[i] = min(C)\n'
                       '            max_n[i] = max(nums[i], nums[i] * max_n[i-1], nums[i] '
                       '* min_n[i-1])\n'
                       '            min_n[i] = min(nums[i], nums[i] * max_n[i-1], nums[i] '
                       '* min_n[i-1])\n'
                       '        return max(max_n)              # 最优子数组可在任意位置结尾',
               'tips': ['负数会让最大、最小乘积互换角色，所以两个状态都要保存。转移时还要考虑只取当前元素，重新开始一段。数组版时间 O(n)，额外空间 '
                        'O(n)。',
                        '优化版先用旧状态算出 a、b，再一起更新 max_n、min_n，不能让 b 用到已更新的 max_n。按下标遍历，避免 '
                        'nums[1:] 复制列表；时间 O(n)，额外空间 O(1)。'],
               'alt_title': '空间优化：只保留上一位置的最大、最小乘积',
               'alt_code': 'class Solution:\n'
                           '    def maxProduct(self, nums):\n'
                           '        max_n = min_n = ans = nums[0]  # 当前结尾的最大、最小乘积，以及全局答案\n'
                           '        for i in range(1, len(nums)):  # 用下标遍历，不创建 nums[1:] '
                           '的临时列表\n'
                           '            x = nums[i]\n'
                           '            a = max(x, x * max_n, x * min_n)  # '
                           '转移（用旧状态计算新的最大乘积）\n'
                           '            b = min(x, x * max_n, x * min_n)  # '
                           '转移（用旧状态计算新的最小乘积）\n'
                           '            max_n = a                 # 两个新值都算完后，再更新状态\n'
                           '            min_n = b\n'
                           '            ans = max(ans, max_n)      # 更新全局答案，不只看最后一个位置\n'
                           '        return ans'},
              {'title': '分割等和子集',
               'source': 'LC 416',
               'note': '给定非空正整数数组 nums，判断能否分成两个元素和相等的子集；每个位置的数只能分到一边。等价于寻找总和一半的子集。',
               'example': 'nums = [1,5,11,5]  →  True（[11] 与 [1,5,5]）；nums = [1,2,5]  →  '
                          'False',
               'code': 'class Solution:\n'
                       '    def canPartition(self, nums):\n'
                       '        total = sum(nums)\n'
                       '        if total % 2:                      # 总和为奇数，不可能平分\n'
                       '            return False\n'
                       '        target = total // 2                # 只需凑出总和的一半\n'
                       '        dp = [False] * (target + 1)         # dp[j] 表示已处理的数能否凑出和 '
                       'j\n'
                       '        dp[0] = True                       # 不选任何数，可以凑出 0\n'
                       '        for num in nums:                   # 每个位置对应一件只能选一次的物品\n'
                       '            for j in range(target, num - 1, -1):  # '
                       '金额倒序，防止重复使用当前物品\n'
                       '                # 转移 D(k,j) = D(k-1,j) or D(k-1,j-num)，此处 j >= '
                       'num\n'
                       '                dp[j] = dp[j] or dp[j - num]\n'
                       '        return dp[target]                  # 能凑出一半，剩下的数就构成另一半',
               'tips': ['0/1 背包：每个数组位置是一件物品，重量是该数，目标容量为 target；每件只能选 0 次或 1 '
                        '次。相同数值出现在不同位置，仍算不同物品。这里求「能否恰好装满」，所以用布尔状态和 or 转移。',
                        '为什么倒序：在外层枚举物品、一维压缩时，倒序保证 `dp[j-num]` '
                        '仍是加入当前物品之前的状态。同一轮中不会借用刚更新的较小金额，因此不会重复选 num。num > target 时，这个 '
                        'range 为空，自动跳过。',
                        '与完全背包的区别：完全背包每件物品可重复选。在同样「外层物品、一维状态」的写法下，内层金额正序，使 `dp[j-num]` '
                        '可包含本轮物品。若把本题改成正序，[1,2,5] 会误用多个 1 凑出 4，错误返回 True。',
                        '与零钱兑换的联系：都是凑目标金额；零钱兑换允许面额重复、求最少个数，用 min，本题每个位置只能用一次、求可行性，用 '
                        'or。循环顺序须结合状态定义；零钱兑换原解按金额再枚举面额，同样能求最少个数。',
                        '设 n 为数组长度，target 为总和的一半：时间 O(n × target)，额外空间 O(target)。下面两份 DFS '
                        '仅作思路备注，未记忆化，最坏是指数级搜索。'],
               'remarks': [{'title': '备注一：DFS 枚举子集，使用 nonlocal 传出结果',
                            'note': '`nonlocal Flag` 声明要重新绑定最近一层外部函数已有的 Flag；不写时，内层的 `Flag '
                                    '= True` 只会建立局部变量，外层仍为 False。它不是模块级 global。 '
                                    '`path.append()` / `path.pop()` 修改同一个列表，不重新绑定 '
                                    'path，因此不需要 nonlocal；若要在内层执行 `path = []`，才需声明 nonlocal '
                                    '才能替换外层绑定。 此版 DFS 不做搜索剪枝，每个叶子还要 sum(path)，最坏时间 O(n × '
                                    '2ⁿ)，辅助空间 O(n)，大输入可能超时。',
                            'code': 'class Solution:\n'
                                    '    def canPartition(self, nums):\n'
                                    '        a = sum(nums)\n'
                                    '        n = len(nums)\n'
                                    '        if a % 2 != 0:                 # 总和为奇数，不可能平分\n'
                                    '            return False\n'
                                    '        a = a // 2                     # '
                                    '子集的目标和，使用整数整除\n'
                                    '        path = []                      # 当前选入子集的数\n'
                                    '        Flag = False                   # 是否找到目标子集\n'
                                    '        def dfs(x):\n'
                                    '            nonlocal Flag              # 修改外层 '
                                    'canPartition 中的 Flag\n'
                                    '            if x == n:                 # '
                                    '每个位置都已决定选或不选\n'
                                    '                if sum(path) == a:\n'
                                    '                    Flag = True        # '
                                    '找到一个和为目标值的子集\n'
                                    '                return\n'
                                    '            dfs(x + 1)                 # 不选 nums[x]\n'
                                    '            path.append(nums[x])       # 选择 nums[x]\n'
                                    '            dfs(x + 1)\n'
                                    '            path.pop()                 # 撤销选择，还原当前路径\n'
                                    '        dfs(0)\n'
                                    '        return Flag'},
                           {'title': '备注二：DFS 累计和、剪枝和短路返回',
                            'note': '用参数 s 记录当前和，返回 bool，不需要 nonlocal。s > 目标和的剪枝依赖正整数条件；or '
                                    '左支为 True 时不再搜索右支。未记忆化，最坏时间 O(2ⁿ)，辅助空间 O(n)，大输入可能超时。',
                            'code': 'class Solution:\n'
                                    '    def canPartition(self, nums):\n'
                                    '        a = sum(nums)\n'
                                    '        n = len(nums)\n'
                                    '        if a % 2 != 0:                 # 奇数总和不能平分\n'
                                    '            return False\n'
                                    '        a = a // 2\n'
                                    '        def dfs(x, s):                 # x 是待处理下标，s '
                                    '是已选数字之和\n'
                                    '            if s == a:\n'
                                    '                return True            # '
                                    '已凑出目标，无需再选剩余数字\n'
                                    '            if x == n or s > a:        # '
                                    '数已用完，或正整数累加后超过目标\n'
                                    '                return False\n'
                                    '            return dfs(x + 1, s) or dfs(x + 1, s + '
                                    'nums[x])\n'
                                    '        return dfs(0, 0)               # '
                                    '先尝试不选，再尝试选，or 会短路'}]},
              {'title': '最长有效括号',
               'source': 'LC 32',
               'note': '给定只含左括号和右括号的字符串 s，返回最长连续有效括号子串的长度；要求括号正确配对，不能跳过中间字符。',
               'example': 's = ")()())"  →  4（子串 ()()）；s = "()(()"  →  2；s = ""  →  0',
               'code': 'class Solution:\n'
                       '    def longestValidParentheses(self, s):\n'
                       '        n = len(s)\n'
                       '        dp = [0] * (n + 1)        # dp[i] 是前 i 个字符的最长有效括号后缀长度\n'
                       '        for i in range(1, n + 1):\n'
                       '            if s[i - 1] == ")":   # 只有右括号可以结束有效括号段\n'
                       '                j = i - dp[i - 1] - 2  # 跳过已有后缀，找当前右括号对应的左括号\n'
                       '                if j >= 0 and s[j] == "(":\n'
                       '                    dp[i] = dp[j] + 2 + dp[i - 1]  # 转移 dp[i] = '
                       'dp[j] + 2 + dp[i-1]\n'
                       '        return max(dp)             # 最长有效段可以在任意位置结束',
               'tips': ['设当前右括号在下标 i-1。先跳过前一位置的有效后缀，再找候选左括号下标 `j = i - dp[i-1] - 2`。',
                        '配对成功时，`dp[i] = dp[j] + 2 + '
                        'dp[i-1]`。三项分别是左括号前相邻的有效段、新配成的一对、被包住的有效段。其余位置保持 0，答案取 `max(dp)`。',
                        '时间 O(n)，额外空间 O(n)。空串时 dp 只有初始的 0。'],
               'remarks': [{'title': '备注 · 栈与匹配标记',
                            'note': '栈存未匹配的左括号下标。配对后标记两端，再取最长连续 True 段。未匹配位置会切断子串。时间 '
                                    'O(n)，额外空间 O(n)。',
                            'code': 'class Solution:\n'
                                    '    def longestValidParentheses(self, s):\n'
                                    '        stack = []                     # '
                                    '保存尚未匹配的左括号下标\n'
                                    '        ans = [False] * len(s)          # True '
                                    '表示该位置已与另一个括号配对\n'
                                    '        path = 0                       # 当前连续匹配段的长度\n'
                                    '        res = 0                        # 已找到的最长长度\n'
                                    '        for i, x in enumerate(s):\n'
                                    '            if x == "(":\n'
                                    '                stack.append(i)        # '
                                    '左括号先入栈，等待右括号\n'
                                    '            elif x == ")" and stack:\n'
                                    '                a = stack.pop()        # '
                                    '与最近一个未匹配的左括号配对\n'
                                    '                ans[a] = True          # '
                                    '标记这一对括号的两个位置\n'
                                    '                ans[i] = True\n'
                                    '        for j in range(len(ans)):      # 再找标记中最长的连续 '
                                    'True 段\n'
                                    '            if ans[j]:\n'
                                    '                path += 1\n'
                                    '                res = max(res, path)   # 更新最长连续段\n'
                                    '            elif not ans[j]:\n'
                                    '                path = 0               # '
                                    '未匹配的位置会切断子串，必须重新计数\n'
                                    '        return res'}]}],
 'pending': [(70, '爬楼梯'),
             (118, '杨辉三角'),
             (198, '打家劫舍'),
             (279, '完全平方数'),
             (322, '零钱兑换'),
             (139, '单词拆分'),
             (300, '最长递增子序列'),
             (152, '乘积最大子数组'),
             (416, '分割等和子集'),
             (32, '最长有效括号')],
 'summary': ['① 爬楼梯\u3000`dp[i] = dp[i-1] + dp[i-2]`（i ≥ 2）。边界 dp[0] = dp[1] = 1。\n'
             '② 杨辉三角\u3000`ans[i][j] = ans[i-1][j-1] + ans[i-1][j]`（0 < j < i）。每行两端为 1。\n'
             '③ 打家劫舍\u3000`dp[i+1] = max(dp[i], dp[i-1] + nums[i])`（i ≥ 1）。dp[k] 对应前 k '
             '间房。\n'
             '④ 完全平方数\u3000`dp[i] = 1 + min(dp[i-j**2])`，在 1 ≤ j ≤ isqrt(i) 中取最小值。dp[0] = '
             '0。\n'
             '⑤ 零钱兑换\u3000`dp[i] = 1 + min(dp[i-j])`，在面额 j ≤ i 中取最小值。dp[0] = '
             '0，无可行选择时为无穷大。\n'
             '⑥ 单词拆分\u3000`dp[i] = OR(dp[j] and s[j:i] == word)`。对词典中满足 j = i - len(word) '
             '≥ 0 的词求或。dp[0] = True。\n'
             '⑦ 最长递增子序列\u3000`dp[i] = max({1} ∪ {dp[j]+1})`，内层只取 j < i 且 nums[j] < nums[i] '
             '的位置。没有候选时为 1，答案取 max(dp)。\n'
             '⑧ 乘积最大子数组\u3000令 x = nums[i]，`C = {x, x * max_n[i-1], x * min_n[i-1]}`。转移为 '
             '`max_n[i] = max(C)`、`min_n[i] = min(C)`。\n'
             '⑨ 分割等和子集\u3000令 D(k,j) 表示前 k 个数能否凑出 j，x = nums[k-1]。`D(k,j) = D(k-1,j) or (j '
             '>= x and D(k-1,j-x))`。压成一维后按 j 倒序更新。\n'
             '⑩ 最长有效括号\u3000`j = i - dp[i-1] - 2`。当 s[i-1] 为右括号、j ≥ 0 且 s[j] 为左括号时，`dp[i] '
             '= dp[j] + 2 + dp[i-1]`。其余情况为 0，答案取 max(dp)。',
             '先定义状态，再写出边界和转移条件。前缀状态通常取目标位置的值。要求以某处结尾的状态，最后要在所有结尾中取最值。压缩状态时要确认更新顺序仍满足原来的依赖。']},
 {'id': 'multi-dp',
  'name': '多维动态规划',
  'problems': [{'title': '不同路径',
  'source': 'LC 62',
  'note': '给定 m 行 n 列的网格，从左上角出发，每一步只能向右或向下。返回到达右下角的不同路径数。',
  'example': 'm = 3, n = 7  →  28；m = 1, n = 4  →  1',
  'code': 'class Solution:\n'
          '    def uniquePaths(self, m, n):\n'
          '        dp = [[0] * n for _ in range(m)]  # dp[i][j] 是到达第 i 行第 j 列的路径数\n'
          '        for i in range(n):\n'
          '            dp[0][i] = 1                  # 第一行只能一直向右\n'
          '        for j in range(m):\n'
          '            dp[j][0] = 1                  # 第一列只能一直向下\n'
          '        for i in range(1, m):\n'
          '            for j in range(1, n):\n'
          '                # 转移 dp[i][j] = dp[i-1][j] + dp[i][j-1]\n'
          '                dp[i][j] = dp[i-1][j] + dp[i][j-1]  # 上方与左方的路径数相加\n'
          '        return dp[m-1][n-1]              # 右下角的路径总数',
  'tips': ['状态 `dp[i][j]` 表示从左上角到达坐标 (i, j) 的路径数。起点和边界格都只有一条走法，因此第一行、第一列初始化为 1。',
           '内部格子的最后一步可以从上方或左方进入，转移为 `dp[i][j] = dp[i-1][j] + dp[i][j-1]`。按行从左到右填表时，两项都已算好。',
           '用 `[[0] * n for _ in range(m)]` 为每一行创建独立列表。时间 O(m × n)，额外空间 O(m × n)。']},
 {'title': '最小路径和',
  'source': 'LC 64',
  'note': '给定非空的非负整数网格 grid，从左上角出发，每步只能向右或向下。返回到达右下角的最小路径和，起点和终点都计入。',
  'example': 'grid = [[1,3,1],[1,5,1],[4,2,1]]  →  7（1+3+1+1+1）',
  'code': 'class Solution:\n'
          '    def minPathSum(self, grid):\n'
          '        m = len(grid)\n'
          '        n = len(grid[0])\n'
          '        dp = [[0] * n for _ in range(m)]  # dp[i][j] 是到达 (i, j) 的最小路径和\n'
          '        a = 0\n'
          '        for i in range(m):\n'
          '            dp[i][0] = a + grid[i][0]    # 第一列只能向下走，逐格累加\n'
          '            a = dp[i][0]\n'
          '        b = 0\n'
          '        for j in range(n):\n'
          '            dp[0][j] = b + grid[0][j]    # 第一行只能向右走，逐格累加\n'
          '            b = dp[0][j]\n'
          '        for i in range(1, m):\n'
          '            for j in range(1, n):\n'
          '                # 转移 dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]\n'
          '                dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]\n'
          '        return dp[m-1][n-1]             # 右下角的最小路径和',
  'tips': ['状态 `dp[i][j]` 表示到达 (i, j) 的最小路径和。第一行和第一列各自只有一条路径，因此分别沿行和列累加。两次初始化都会把起点设为 '
           'grid[0][0]。',
           '内部格子的转移是 `dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + '
           'grid[i][j]`。最后一步可以来自上方或左方，取代价更小的一边，再加上当前格子的值。',
           '按行从左到右填表，两项前驱状态都已算好。时间 O(m × n)，额外空间 O(m × n)。']},
 {'title': '最长回文子串',
 'source': 'LC 5',
 'note': '给定字符串 s，返回其中一个最长回文子串。子串必须连续，长度并列时可以返回任意一个。',
 'example': 's = "babad"  →  "aba"（"bab" 也可）。s = "cbbd"  →  "bb"。',
 'code': 'class Solution:\n'
         '    def longestPalindrome(self, s):\n'
         '        n = len(s)\n'
         '        dp = [[False] * n for _ in range(n)]  # dp[i][j] 判断 s[i:j+1] 是否回文\n'
         '        ans = ""\n'
         '        for i in range(n-1, -1, -1):         # 先填第 i+1 行，再填第 i 行\n'
         '            for j in range(i, n):\n'
         '                # 转移 dp[i][j] = (s[i] == s[j]) and (j-i <= 1 or dp[i+1][j-1])\n'
         '                dp[i][j] = s[i] == s[j] and (j-i <= 1 or dp[i+1][j-1])\n'
         '                if dp[i][j] and j-i+1 > len(ans):\n'
         '                    ans = s[i:j+1]          # 只用更长的回文更新答案\n'
         '        return ans',
 'tips': ['状态 `dp[i][j]` 表示闭区间 [i, j] 是否为回文。两端相等时，长度为 1 或 2 可以直接确认。更长的区间要看去掉两端后是否为回文。',
          '转移为 `dp[i][j] = (s[i] == s[j]) and (j-i <= 1 or dp[i+1][j-1])`。右侧依赖第 i+1 行，所以 i '
          '从 n-1 倒着遍历到 0。遍历到第 i 行时，更大的左端点已经处理完毕。',
          '每个区间先按公式给 dp[i][j] 赋布尔值，再用它判断是否更新答案。当 j-i <= 1 时，or 会短路，跳过内部状态的访问。时间 O(n²)，额外空间 '
          'O(n²)。'],
 'remarks': [{'title': '备注 · 双指针中心扩展法',
              'note': '本题使用双指针中心扩展。中心 `(i, i)` 对应奇数长度，`(i, i+1)` 对应偶数长度。每次比较两端字符，再向外移动一格。 '
                      '易错点 `1=<r<=2` 有语法错误，正确写法是 `1 <= r <= 2`。本题用 `0 <= l and r < n` '
                      '分别检查左、右指针的边界。 停止扩展时，l 和 r 已越过最后一对匹配的位置，可能越界，也可能指向不相等的字符。有效区间是 '
                      '`[l+1, r)`，用 `s[l+1:r]` 取出，长度为 `r-l-1`。 时间 O(n²)。双指针和下标只用 O(1) '
                      '空间，Python 切片会创建新字符串，保存答案最多需要 O(n) 空间。',
              'code': 'class Solution:\n'
                      '    def longestPalindrome(self, s):\n'
                      '        n = len(s)\n'
                      '        ans = ""\n'
                      '        for i in range(n):\n'
                      '            for l, r in [(i, i), (i, i+1)]:  # 奇数长度与偶数长度的中心\n'
                      '                while 0 <= l and r < n:      # 访问字符前先检查两端下标\n'
                      '                    if s[l] == s[r]:\n'
                      '                        l -= 1              # 当前两端匹配，继续向外扩展\n'
                      '                        r += 1\n'
                      '                    else:\n'
                      '                        break\n'
                      '                if r-l-1 > len(ans):        # 有效区间 [l+1, r) 的长度是 '
                      'r-l-1\n'
                      '                    ans = s[l+1:r]          # 左端回到 l+1，右端 r 由切片排除\n'
                      '        return ans'}]},
 {'title': '最长公共子序列',
 'source': 'LC 1143',
 'note': '给定字符串 text1 和 text2，返回最长公共子序列的长度，没有公共字符时返回 0。子序列保留原字符顺序，可以跳过字符。',
 'example': 'text1 = "abcde", text2 = "ace"  →  3（公共子序列 "ace"）；text1 = "abc", text2 = "def"  →  0',
 'code': 'class Solution:\n'
         '    def longestCommonSubsequence(self, text1, text2):\n'
         '        m = len(text1)\n'
         '        n = len(text2)\n'
         '        dp = [[0] * (n + 1) for _ in range(m + 1)]  # 空前缀的答案是 0\n'
         '        for i in range(1, m + 1):\n'
         '            for j in range(1, n + 1):\n'
         '                if text1[i-1] == text2[j-1]:\n'
         '                    dp[i][j] = dp[i-1][j-1] + 1  # 转移：接上相同的末尾字符\n'
         '                else:\n'
         '                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # 转移：分别跳过一个末尾字符\n'
         '        return dp[-1][-1]',
 'tips': ['状态 `dp[i][j]` 表示 text1[:i] 和 text2[:j] 的最长公共子序列长度。i、j 是前缀长度，末尾字符的下标分别是 i-1 和 j-1。任一前缀为空时，长度为 0。',
          '末尾字符相同，接在两个更短前缀的公共子序列后面：`dp[i][j] = dp[i-1][j-1] + 1`。末尾不同，至少要跳过其中一个：`dp[i][j] = max(dp[i-1][j], '
          'dp[i][j-1])`。',
          '从左到右逐行填表，上方、左方和左上方都已算好。时间 O(m × n)，额外空间 O(m × n)。']},
 {'title': '编辑距离',
 'source': 'LC 72',
 'note': '给定字符串 word1 和 word2，每次可以在 word1 中插入、删除或替换一个字符。返回把 word1 变为 word2 所需的最少操作次数。',
 'example': 'word1 = "horse", word2 = "ros"  →  3（horse → rorse → rose → ros）；word1 = "", word2 = "abc"  →  3',
 'code': 'class Solution:\n'
         '    def minDistance(self, word1, word2):\n'
         '        m = len(word1)\n'
         '        n = len(word2)\n'
         '        dp = [[0] * (n + 1) for _ in range(m + 1)]\n'
         '        for i in range(1, m + 1):\n'
         '            dp[i][0] = i                         # 删掉 word1 前缀的全部字符\n'
         '        for j in range(1, n + 1):\n'
         '            dp[0][j] = j                         # 从空串插入 word2 的前缀\n'
         '        for i in range(1, m + 1):\n'
         '            for j in range(1, n + 1):\n'
         '                if word1[i-1] == word2[j-1]:\n'
         '                    dp[i][j] = dp[i-1][j-1]      # 转移：保留相同字符，代价为 0\n'
         '                else:\n'
         '                    # 转移 dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])\n'
         '                    dp[i][j] = min(dp[i-1][j] + 1,      # 删除\n'
         '                                   dp[i][j-1] + 1,      # 插入\n'
         '                                   dp[i-1][j-1] + 1)    # 替换\n'
         '        return dp[-1][-1]',
 'tips': ['状态 `dp[i][j]` 表示把 word1[:i] 变为 word2[:j] 的最少操作数。第一列 `dp[i][0] = i`，第一行 `dp[0][j] = j`，分别对应全部删除和全部插入。',
          '末尾相同：`dp[i][j] = dp[i-1][j-1]`。末尾不同：`dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], '
          'dp[i-1][j-1])`，三项依次对应删除、插入和替换。',
          '按 i、j 从小到大填表，当前状态所需的三个相邻状态都已算好。时间 O(m × n)，额外空间 O(m × n)。']}],
  'pending': [(62, '不同路径'), (64, '最小路径和'), (5, '最长回文子串'), (1143, '最长公共子序列'), (72, '编辑距离')],
  'summary': ['① 不同路径\u3000`dp[i][j] = dp[i-1][j] + dp[i][j-1]`。第一行和第一列都为 1。\n'
   '② 最小路径和\u3000`dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]`。边界沿第一行、第一列累加。\n'
   '③ 最长回文子串\u3000`dp[i][j] = (s[i] == s[j]) and (j-i <= 1 or dp[i+1][j-1])`。i 倒序，先算内层依赖。\n'
   '④ 最长公共子序列\u3000末尾相同：`dp[i][j] = dp[i-1][j-1] + 1`；否则：`dp[i][j] = max(dp[i-1][j], dp[i][j-1])`。空前缀为 0。\n'
   '⑤ 编辑距离\u3000末尾相同：`dp[i][j] = dp[i-1][j-1]`；否则：`dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`。空前缀边界为 '
   '`dp[i][0] = i`、`dp[0][j] = j`。',
   '先分清下标表示网格坐标、区间端点还是前缀长度，再根据依赖决定填表顺序。两个前缀的题常用额外一行一列表示空前缀，取末尾字符时用 i-1 和 j-1。']},
 {'id': 'tricks',
  'name': '技巧',
  'problems': [{'title': '只出现一次的数字',
  'source': 'LC 136',
  'note': '非空整数数组 nums 中，只有一个数字出现一次，其余数字都出现两次；返回这个只出现一次的数字，要求线性时间、常数额外空间。',
  'example': 'nums = [4,1,2,1,2]  →  4（两个 1 和两个 2 抵消，只剩 4）',
  'code': 'class Solution:\n'
          '    def singleNumber(self, nums):\n'
          '        x = 0                          # 异或的初值，0 与任何数异或仍是那个数\n'
          '        for num in nums:\n'
          '            x = x ^ num                # 相同数字异或为 0，成对出现的数会抵消\n'
          '        return x                       # 最后留下的就是只出现一次的数字',
  'tips': ['异或规则：`a ^ a == 0`、`a ^ 0 == a`；异或满足交换律和结合律，所以重复的数即使不相邻也能抵消。',
           '`^` 是整数按位异或，乘方用 `**`。本题返回单个整数，不返回列表，也不修改 nums。']},
 {'title': '多数元素',
  'source': 'LC 169',
  'note': '非空数组 nums 中有一个元素出现次数严格大于 len(nums) / 2，返回它；题目保证这个多数元素一定存在。',
  'example': 'nums = [2,2,1,1,1,2,2]  →  2（2 出现 4 次，超过总数 7 的一半）',
  'code': 'class Solution:\n'
          '    def majorityElement(self, nums):\n'
          '        ans = nums[0]                  # 当前候选数，题目保证数组非空\n'
          '        hp = 1                         # 候选的抵消计数，不是实际出现次数\n'
          '        for i in range(1, len(nums)):\n'
          '            if nums[i] == ans:\n'
          '                hp += 1                # 遇到相同的数，计数加一\n'
          '            else:\n'
          '                hp -= 1                # 遇到不同的数，抵消一次\n'
          '            if hp == 0:\n'
          '                ans, hp = nums[i], 1   # 归零就换当前数为候选，重新计数\n'
          '        return ans                     # 有严格多数的保证，最后候选就是答案',
  'tips': ['`hp` 是抵消计数，不是候选的真实出现次数；若题目不保证多数元素存在，还需统计候选次数并验证。']},
 {'title': '颜色分类',
  'source': 'LC 75',
  'note': 'nums 只含 0、1、2，分别表示三种颜色；原地把相同颜色排在一起，并按 0、1、2 的顺序排列，不返回数组。',
  'example': 'nums = [2,0,2,1,1,0]  →  nums 变为 [0,0,1,1,2,2]（返回值是 None）',
  'code': 'class Solution:\n'
          '    def sortColors(self, nums):\n'
          '        p0 = p1 = 0                    # p0 是 0 区右边界，p1 是 0/1 区右边界\n'
          '        for i, x in enumerate(nums):    # x 保存当前位置写入前的原值\n'
          '            nums[i] = 2                # 先把新位置归到 2 区\n'
          '            if x <= 1:\n'
          '                nums[p1] = 1           # 原值为 0 或 1，先扩大 0/1 区\n'
          '                p1 += 1\n'
          '            if x == 0:\n'
          '                nums[p0] = 0           # 原值为 0，再把 0 区扩大一位\n'
          '                p0 += 1',
  'tips': ['循环开始时，`[0, p0)` 全是 0，`[p0, p1)` 全是 1，`[p1, i)` 全是 2。两个 `if` 不能改成 `if / '
           'elif`：遇到 0 时，两处都要执行。']},
 {'title': '下一个排列',
  'source': 'LC 31',
  'note': '将 nums 原地重排为字典序紧邻的下一个排列；若已经是最大排列，就变为升序的最小排列。允许重复元素，不返回数组。',
  'example': 'nums = [1,2,3]  →  nums 变为 [1,3,2]；nums = [3,2,1]  →  [1,2,3]（均返回 None）',
  'code': """class Solution:
    def nextPermutation(self, nums):
        n = len(nums)
        i = n - 2                          # 从倒数第二位找能增大的位置
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1                         # 右边这段不升序，继续向左找
        if i >= 0:                         # 找到后，先把这一位换大
            j = n - 1                      # 从右找后缀中最小的、更大的数
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]  # 换成刚好更大的数
        left, right = i + 1, n - 1          # i 为 -1 时，范围就是整个数组
        while left < right:                # 原地反转后缀，使它升序、增幅最小
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1"""},
 {'title': '寻找重复数',
  'source': 'LC 287',
  'note': 'nums 长度为 n + 1，所有数都在 1..n 内，只有一种数字出现至少两次，返回这个重复数；不能修改 nums，额外空间要求 O(1)。',
  'example': 'nums = [1,3,4,2,2]  →  2；nums = [3,3,3,3,3]  →  3（重复次数可以超过两次）',
  'code': """class Solution:
    def findDuplicate(self, nums):
        slow = fast = 0                    # 从下标 0 出发，nums[i] 是下一位置
        while True:
            slow = nums[slow]              # 慢指针每次走一步
            fast = nums[nums[fast]]         # 快指针每次走两步
            if fast == slow:
                break                      # 先找到环内相遇点，未必是环入口
        head = 0                           # 一个从起点走，一个从相遇点走
        while slow != head:
            slow = nums[slow]              # 两个指针同步，每次各走一步
            head = nums[head]
        return slow                        # 再次相遇的位置就是环入口和重复数"""}],
  'summary': ['① 只出现一次：利用相同数字异或为 0，让成对的数抵消。\n'
 '② 多数元素：维护一个候选和抵消计数；题目保证严格多数存在，最后的候选就是答案。\n'
 '③ 颜色分类：用两个边界维护 0 区、1 区和 2 区，边扫描边放回正确区域。\n'
 '④ 下一个排列：从右边找能增大的位置，换上右侧刚好更大的数，再反转后缀，让增幅尽量小。\n'
 '⑤ 寻找重复数：把下标到 nums[下标] 当成指针，先找环内相遇点，再从 0 和相遇点同步走，找出环入口。',
 '这些技巧依赖各自的题目条件：异或需要其余数成对；候选抵消依赖严格多数的存在；颜色分类只处理三种取值；下一个排列利用后缀的不升序；快慢指针利用长度和取值范围形成环。先确认条件，再使用对应方法，不能把它们当成同一种通用规则。'],
  'pending': [(136, '只出现一次的数字'),
              (169, '多数元素'),
              (75, '颜色分类'),
              (31, '下一个排列'),
              (287, '寻找重复数')]}]
