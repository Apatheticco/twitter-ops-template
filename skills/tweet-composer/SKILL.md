---
name: tweet-composer
description: "Draft publish-ready tweets — single tweets, original threads, quote tweets, and threads split out of long-form content (reports, articles, whitepapers). Handles formatting, voice consistency, fact-checking and pre-publish checks. Use this skill whenever the user wants to write a tweet, draft tweet, compose tweet, 写推文, 发推, 帮我写, tweet draft, 推文, 内容撰写, 发个推, or to turn long content into a thread: 拆线程, 长文拆解, 拆成推文, 研报转推文, article to thread, make a thread from, 写个线程."
---

# 推文撰写 Tweet Composer

topic-engine（选题 + 角度）→ **tweet-composer（撰写）** → 人工发布 → engagement（互动运营）。
不做选题判断，专注把角度 / 原文写成可发布的推文。**支持三种产出：单推 / Thread（原创）/ Thread（长文拆解）。**

> 🔴 **全手动发推**：本 Skill 只出终稿，不 hook 任何发推 MCP。发布永远由人确认后手动执行。

## 0. 输入分支（先判模式）

| 模式 | 输入 | 入场检查 | 差异 |
|---|---|---|---|
| **A 单推** | topic-engine 的角度 | §1.1 上游 7 项 | 字符预算最紧 |
| **B Thread 原创** | topic-engine 的角度 | §1.1 上游 7 项 | 无原文，靠角度展开 |
| **C Thread 长文拆解** | 长内容（研报 / 文章 / 白皮书 / 推文串 / 笔记 / 大纲） | §1.2 原文消化 6 项 | 有原文要压缩，难在取舍不在分段 |

三种模式只有**入场检查**（§1）和**结构模板**（§3.2）不同，其余章节全部共用。

## 1. 入场硬检（不接活条件）

**1.1 模式 A / B — 上游 7 项**：①候选 ID + 标题 ②Pattern 编号 + Hook ③核心观点 ④数据支撑 ≥3 ⑤反向风险 ⑥结尾金句 ⑦形式建议。
缺任一 → 回 topic-engine，**不自行选题**。**快速通道**：用户自带 ≥6/7 要素可直接接（显式声明"自带模式"）。选题阶段已定性的沿用，不重新评估。

**1.2 模式 C — 原文消化 6 项**（缺项不动笔）：核心论点（≤3 个，一句话一个）· 关键数据（最有冲击力的 3-5 个）· 支撑论据 · 作者隐含假设（没明说但逻辑依赖的前提）· 最薄弱环节（最容易被反驳处）· **你的独立角度**。
⚠️ 最后一项是硬性的：**没有独立角度 = 纯转述 = 不该发**。

## 2. Draft 落盘 schema

终稿先落 `/tmp/tweet-composer-draft-YYYY-MM-DD.md`，§9 按这个 schema 核：

```markdown
---
date / candidate_id / mode: A_single | B_thread | C_thread_from_longform
content_type: <operations-plan §三 类型名>  pattern: <编号>  source_ref: <模式 C 必填：原文标题/链接>
# 爆款 5 件套（≥4 项 true）
first_person_rhetoric / data_anti_consensus / mechanism_breakdown / novel_hook / closing_hook: true|false
# 标的型必填（点名具体标的时）
single_ticker_focus / authority_position_anchor: true|false|n_a
# 跟报型必填 / BREAKING 型必填
is_followup: true|false   first_sentence_absolute_adjective: <词>|null
breaking_ip_hook / breaking_ticker / breaking_magnitude: true|false
---
[推文正文 / 线程逐条]

## 配图方案
[图的内容 / 形式 / 来源 —— 附图在发布端，写作端交方案]

## 首评草稿
[T+5 发的补充数据 / 延展 / 来源]
```

## 3. 写作约束

### 3.1 字符预算（第一道闸门）
中文 / 全角计 2、ASCII 计 1，**上限 280 加权**（≈140 汉字含标点）。单推目标 ≤270 留余量；引用推 ≤160（被引内容占空间）；Thread **每条单独核**。**先定预算再动笔**，超限砍修饰词、不砍数据钉子。

### 3.2 结构模板

- **单推**：Hook（<40 字）→ 核心论证含数据（1-2 句）→ 主流看法 vs 我的看法 → 决策式收尾 + Cashtag
- **引用推**：1-2 句锐评立场 + 1 句数据或风险
- **Thread 通用**：首推独立成立 + 🧵；每条标 [n/N]、单独转发也看得懂；每 3-4 条换节奏（数据 → 观点 → 反问 → 类比）；末条 = 总结 + 反向风险 + 钩子。🚫 **禁目录式开头**（"关键词：A、B、C"/"本文将讨论"），首推三选一：反问式冲突 / 硬数字锚 / 反常识断言

| 档位 | 适用 | 结构 |
|---|---|---|
| 短 3-5 | 新闻评论、单一观点 | 核心观点 + hook → 最强论据 → 反向风险 →（历史对比）→ 结论 + 钩子 |
| 中 5-8 | 研报摘要、项目分析、复盘 | 反直觉结论 → 背景（30 秒能懂）→ 核心论证 ×2 → 转折 / 反面 → 实操启示 → 总结 + 独立判断 + 钩子 |
| 长 8-15 | 白皮书解读、行业 / 宏观研究 | 颠覆性开头 → 为什么重要 → 论点一 → 论点二 → 论点三 / 反面 → 综合判断 → 风险 → 收尾 + CTA |

**模式 C 额外**：不照搬原文措辞，用自己的语气重写；在原文基础上形成**你的判断**，不做中立转述；数据具体化（原文"大幅增长" → "增长 47%"）；原文核心数据不许丢；末条给的是你的判断，不是原作者的。

### 3.3 独立观点强制
（新闻/数据/链上/标的类必跑；BREAKING ≤30min 与实测类豁免）
① 找主流叙事（80% 人的第一反应）→ ② 挖小众视角（时间 / 意图 / 结构 / 反向 / 延伸，五选一）→ ③ **显式句式**"主流读法 X，我的看法 Y"→ ④ **单边判断收尾**。找不到小众视角 = 这选题不该发。

### 3.4 互动钩子（与单边判断兼容的三式）
**决策矩阵**"如果 X，就 Y"（首选，可证伪）/ **立场挑衅**"我不同意 X，理由 Z" / **具体反问**"接下来 12 个月哪家先死？"。🚫 禁空泛"你怎么看""拭目以待""值得关注"式收尾。

### 3.5 风格适配
锐评类犀利戳痛点 / 数据类数字优先 / 快评类短平快 / 叙事类递进 / 分析类必含对立面 / 对比类表格化。模板见 `references/tweet-styles.md`。

### 3.6 高触达公式
- 实测类**带实际产出**（截图 / 作品）；链上用**人物昵称 + 表情定性**不用 0x 地址；宏观**挖背后的人 / 公司**，不复读数据本身
- **五要素命中 ≥2**：三件套开头（身份 + 数字 / 时间 + 动作，禁"据悉 / 近日"）· 反差钩子（以为 X → 其实 Y）· 金句收尾（截图能独立成立）· 借嘴开炮（监管 / 法律 / 人身评价必引权威原话）· 跨界视角
- **跟报型首句必含绝对级形容词**：迄今为止 / 史上最大 / 破纪录 / 首次 / 唯一 / N 年来最 X
- **BREAKING 三件套**：具名主体 + $ticker + 量级数字（缺件回炉；时效优先可先发后补）
- **Bookmark 型（长图整理）**：过 30 天复用测试 + 数字打头 + 借嘴整理（禁自传体"我学到的 X 条"）+ 5-10 张图
- **跨界 / 框架型**：≥2 个数字钉子；框架先行 / 拉长时间尺度 / 三催化剂 + 权威原话，三选一

## 4. 模式 C 专属：数据补充

原文数据不足或过期时回调 MCP，**回调拿到的价格覆盖原文旧价格**（§5.4）：

```
价格 / 宏观 / 基本面 → mcp__followin__metrics（美股大宗宏观必传 asset_type="tradfi"）
链上 / KOL 持仓      → mcp__followin__signal      报道 / 研报 → mcp__followin__news(query="…")
账号级数据          → mcp__followin__twitter(action=…)    原文是 URL → WebFetch
```

可接受输入：研报 / 文章链接 · 粘贴的长文本 · 白皮书或 PDF · 别人的推文串（整合再创作）· 语音转文字笔记 · 要点大纲。

## 5. 事实核查 6 维

逐条列证据，**禁裸写"已过"**：

1. **数字验算**：百分比 / 倍数本机算一遍（"近一倍" = 2x 不是 1.82x）；非官方一手标"据 X"/"估"
2. **主体逐字比**：范围词（巨鲸持仓 ≠ 平台持仓）/ 定性词（自研 ≠ 套壳）/ 上市地 / 公司角色
3. **引用保留限定词**：删掉原话里的"在相当程度上"/"可能"就是改语气，会被原推打脸
4. **相对时间对齐**当前日期；价格必与最新 `metrics` 一致（涉价格的开写前重拉，不用简报旧数）
5. **因果软化**：无时序 / 数据支撑，改"A 之后 B"/"A 可能推动 B"
6. **信源密度**：≥2 独立源可直引；单一权威源标"据 X"；单一非权威源标 ⚠️ 或改"传 X"；0 源禁当事实

## 6. 红线（绝对禁区）

不预测价格（"会涨到 X"）/ 不给投资建议 / 不把未验证消息当事实 / 不人身攻击（嘲讽观点 ≠ 攻击个人）/ 不碰政治敏感（除非直接影响市场）/ 不晒单、不泄露个人资产 / 不删已发推文（除非事实错误）。
第一人称占比与标志词（口头禅 / 粗口）频率上限见 `twitter-ops/references/voice-guide.md` —— 越线 = 账号定位滑向个人 IP，砍掉重写。

## 7. X 算法适配

- **外链禁放主推**（严重掉触达），移到 Thread 末条或评论区首楼
- **首评草稿随终稿交付**，主推发出后 T+5min 内发（触发早期互动速度阈值）
- **T+30min 作者亲自回复 2-3 条**（作者参与对话是权重最高的互动信号）
- **Cashtag 化**：股票 + 加密代码统一 `$`（$NVDA / $BTC），金额 / 商品 / 公司名 / 指标不加；单条 ≤1
- **hashtag ≤1 个 niche**（生态 / 工具类有正收益，泛品类 #crypto / #AI 禁用）
- **视频 / 书签向内容每周 ≥1 条**，本周累计为 0 则本条优先尝试

## 8. 发布前终检

- **反重叠**：vs 当日已发清单，角度 / 数据 / 钩子三维查重
- **频次预算**：日上限见 `twitter-ops/references/operations-plan.md` §二（默认 普通日 ≤3 / 重大日 ≤5 / 突发日 ≤7），到上限硬叫停；达不到预期曝光门槛的素材不发
- **ER 预判**：按内容类型历史基线（`performance-review/references/audience-profile.md`），到不了"良好"档砍掉重写
- **时段**：Thread 与主力推文各放黄金窗口（`twitter-ops/references/content-calendar.md`）；放大器 = 话题劫持 2-3h 窗口 / Thread 末条 @ 1-2 个相关 KOL

## 9. 终检清单（任一 FAIL 不准出稿）

```
[ ] ① frontmatter 必填齐（mode / content_type / pattern / 跟报标记）
[ ] ② 字符预算：单推 ≤280 加权 · Thread 逐条 ≤280 · 引用推 ≤160
[ ] ③ 爆款 5 件套 ≥4/5 为 true
[ ] ④ 标的型：single_ticker_focus + authority_position_anchor 已判（n_a 需写理由）
[ ] ⑤ 跟报型首句含绝对级形容词
[ ] ⑥ BREAKING 三件套齐（缺 → warn）
[ ] ⑦ 互动钩子命中 §3.4 三式之一，无空泛收尾
[ ] ⑧ 独立观点显式句式在正文里（豁免类型除外）
[ ] ⑨ 红线全过（§6）        [ ] ⑩ 外链不在主推
[ ] ⑪ 配图方案段非空        [ ] ⑫ 首评草稿段非空
[ ] ⑬ 事实核查 6 维逐条有证据 [ ] ⑭ cashtag / hashtag 数量合规
[ ] ⑮ 模式 C：原文核心数据无丢失 + 末条是你的判断而非原作者的
```
> 可按 §2 schema 写成脚本自动跑；手动过也要逐项过完。

## 10. 输出格式

正文（引用块，Thread 逐条编号）· 字符数（逐条）· 配图方案 · 事实核查 6 维摘要 · 终检清单结果 · 反重叠与频次结论 · 首评草稿 · 发布后 SOP（T+0/5/30/60）+ 建议时段 · **一次到位决策块**（形式 / 时间 / 决策三变量一次答，如"A 版 + 19:00 + 直接发"）。

**模式 C 追加**：原文来源 · 线程长度 · 核心论点一句话 · 发布节奏（一次发完 / 间隔 X 分钟）· 备选（第 1 条可单发；可从第 X 条截断成短线程）。

**首版即终稿**：一次给齐，不留半成品等挑刺。

## 11. 写作前路由（grep，不凭记忆）

`twitter-ops/references/`：`voice-guide.md`（调性 / 语言元素）· `operations-plan.md`（红线 / 频次 / 配比）· `content-calendar.md`（时段）
本 Skill：`references/tweet-styles.md`（风格模板 / hashtag / 线程结构）
其他：`topic-engine/references/angle-templates.md`（Pattern 与反模式）· `performance-review/references/`：`patterns.md` + `vault.md`（自家爆款句式 / 失败库）· `audience-profile.md`（受众 / ER 基线）· `engagement/references/kol-targets.md`（借嘴人物 / @ 谁）
