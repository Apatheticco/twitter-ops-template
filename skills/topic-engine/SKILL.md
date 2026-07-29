---
name: topic-engine
description: "Transform trending topics into tweet angles — the bridge between trend-scout's raw intelligence and tweet-composer's content creation. Generates scored, data-backed angles with hooks for every topic. Use this skill whenever the user mentions topic selection, angle generation, what to tweet about, 选题, 角度, 切入点, content ideas, tweet ideas, 今天发什么, 写什么内容, 开角度, 找切入点."
---

# 话题引擎 Topic Engine

trend-scout（采集）→ **topic-engine（选题 + 开角度）** → tweet-composer（撰写）。
不采集数据，但可回调 MCP 补数据。

## 0. 使用前必填（占位配置）

| 变量 | 含义 |
|---|---|
| `BENCHMARK_KOLS` | 层 B 对标白名单·标杆组（3-5 个同语种同赛道优质账号） |
| `BASELINE_KOLS` | 层 B 对标白名单·基线组（2 个更挑、更策展的媒体/策展号） |
| `CATEGORY_CAP` | 单赛道周上限，如「Crypto ≤25%」 |
| `MAIN_ENGINE_TYPES` | 你的主引擎内容类型代号 + 周配额（在 `twitter-ops/references/operations-plan.md` 里定义，本文用 `#主引擎` / `#跟报` / `#叙事` 指代） |
| `WORK_DIR` | 落盘目录。**跨周文件（quota-$WEEK）必须落在持久目录，别放 `/tmp`**（重启即清） |
| `BRIEF_DIR` | trend-scout 简报目录（选题表追加到这里） |

> **别把高频全量搬运号放进 `BASELINE_KOLS`**：它们发的是新闻流不是策展，撞它们几乎对每条题都判 hit，零差异化信号。基线组要选"更挑、更策展"的。

---

## 1. 过程纪律（违规即重跑）

核心价值 = **3 角度备选 + Pattern 匹配 + 多样性校验**。
**禁止**：直接出推文（那是 tweet-composer 的活）/ 每选题只给 1 角度 / 角度缺 5 要素 / 无 Pattern 编号 / 无 3 角度对比表 / 无打分明细 / 无 Top 5 一览表 / 无多样性校验 / 跳过第零步 / Top 5 少于 5 条 / 只落盘不追加简报。

用户说"快速选一条" → 不接：本 skill 产出是"选题 + 3 角度 + 打分"，要快条直接调 tweet-composer。

**必跑 6 步**：⓪ 账号上下文 → ① 候选池 + 排序 → ② Pattern 匹配 → ③ 角度 5 要素 → ④ 双层打分 + 排序 → ⑤ 落盘 4 文件 + Top 5 markdown → ⑥ 追加简报。

**执行顺序硬规则**（砍 / 豁免类操作的先后）：
```
1. 纯交易排除 + 纯地缘跟报排除（最先）
2. 时效硬过滤（>48h 淘汰；24-48h 先跑层 B 单项检查，🔴 即砍省计算）
3. 第零步账号上下文 → Pattern 匹配 → 角度生成
4. 双层打分（含扩散斜率）→ 加分项
5. 层 B 差异化 4 标签
6. 抢先豁免判定（只作用于已过前两关的候选；纯交易 / 🔴 永不豁免）
7. 配比三态校验 → Top 5 输出 → 简报追加
```

## 2. 输入

- **强制**：读 `<候选目录>/trend-scout-candidates-YYYY-MM-DD-latest.txt` → candidates.json（首扫 ≥12 / 刷新 ≥7）。**禁止跳过 json 直接读简报挑话题**。
- 简报 Markdown 仅作上下文（分歧矩阵 / 宏观 / 社区风向）；用户突发点名可越过 json。
- json 缺失 / 数量不足 → 不允许自己挑话题，要求重跑 trend-scout。
- 处理范围：按 raw_score 降序取前 `max(8, 60%)` 条。
- 价格只用简报「实时数据区」数字；叙事区价格是历史叙述。

**纯交易排除（兜底，上游已预排除）**：单一交易事件（爆仓 / 抄底 / 清算 / 建仓 / 仓位变动 / 喊单 / 清算地图 / 技术面阈值 / 资金费率）且**本候选 title/one_liner 文本内**无叙事 layer（宏观锚 / 项目生态 / KOL 冲突 / 跨源共识；**不可继承同实体历史轮**）→ 砍，不进打分，砍掉的 ID 显式列出。

**纯地缘跟报排除**（实测这类跟报互动 median 全线沉底）：军事 / 地缘 **follow-up**（第 N 轮打击 / 又一次升级 / 持续交火 / 常规化播报）且**本候选无独家角度**（时间线拼图 / 量级换算 / 跨语言共识 / 跨界传导（地缘→油价→实际利率→风险资产）/ 反共识读法，≥1 命中才算有角度；**不可继承同实体首发轮的角度**）→ 砍。
**豁免**（真 BREAKING 不是跟报）：首发突发（`first_seen <6h`）/ 带 ≥2 `exclusive_details` / `🌉跨界传导` 或 `✅多源确认` 标签。
判定靠**角度有无**，不靠"是不是地缘题材"：首发轮带时间线拼图 + 跨语言共识的该留，次日"第二轮打击"纯播报的该砍。

**时效硬过滤**：≤24h 正常 / 24-48h 先层 B 检查（🔴 即砍）且需 ≥2 可验证数字才保留 / >48h 淘汰（特例：持续发展事件只写最新进展；周期数据仅发布当日 24h 有效）。过滤后可用 <2 → 警告 + 三选项（重跑首扫 / 突发 / 手动补）。

## 3. 第零步：账号上下文（强制必读）

按需 grep 源文档，**不得凭记忆复述**；文件不存在 → warn 继续，对应加分项跳过。

| 文档 | 用途 |
|---|---|
| `twitter-ops/references/voice-guide.md` | 调性 ±0.3 |
| `twitter-ops/references/operations-plan.md` | 周配额 / 红线 / 频次预算（**配比唯一权威**） |
| `twitter-ops/references/content-calendar.md` | 选题金字塔 / 差异化标签 |
| `performance-review/references/patterns.md` | Pattern 实证 + 反模式 |
| `performance-review/references/audience-profile.md` | 受众画像 + 时段矩阵 |
| `<WORK_DIR>/account-weekly-progress-*.json` | 配额缺口 +0.2 |
| `<WORK_DIR>/account-pending-topics.json` | 待发清单**无条件占 Top 5 名额** |
| `<WORK_DIR>/account-today-published-count.txt` | ≥4 → 硬叫停警告 |

## 4. Pattern 匹配（16 模板，详见 `references/angle-templates.md`）

| # | 模板 | 时效 | # | 模板 | 时效 |
|---|---|---|---|---|---|
| 1 🔥 直击对立 | 4-24h | 9 🎯 对比分析 | 24h+ |
| 2 📊 数据讲故事 | 4-48h | 10 💡 交易洞察 | 4-24h |
| 3 🔄 反向风险 | 4-48h | 11 🌍 宏观视角 / 跨界传导 | 24h+ |
| 4 📈 历史平行线 | 24h+ | 12 🌊 叙事追踪 | 24-72h |
| 5 😤 嘲讽吐槽 | 4-24h | 13 🪞 反差叙事 / 第三方 | 24-72h |
| 6 🚀 破局新视角 | 24h+ | 14 🎭 人物花絮反差 | 24-72h |
| 7 ⚡ 突发快评 | <4h | 15 🔢 一句话 + 量级对比 | 24h+ |
| 8 🎓 深度教育 Thread | 24h+ | 16 🎙️ 借大佬之口反共识 | 4-48h |

匹配组合：突发→7+2+3 / KOL-大户分歧→1+2+10 / 数据驱动→2+11+3 / 行业争议→5+1+6 / 周期信号→4+2+10 / 新叙事→6+9+8。**每话题 3 角度，Pattern 不重复。**

**#12 要点**：由 trend-scout 叙事榜 ≥3.0 的板块触发；4 模式（深度成因 / 跨界映射 / 对照差异化 / 反向风险）；hook 必含数字；Thread 优先；禁"X 板块全解析 / 新风口 / 我觉得"。

## 5. 角度 5 要素（每角度必填）

核心观点（一句话强立场）/ 反共识维度（时间·反向·结构·意图·延伸 选一，**3 角度不重叠**）/ Hook（<140 字符，数字开头 / 反直觉 / 提问 / 嘲讽）/ 反向风险（1-2 句）/ 结尾金句（陈述式判断，不开放提问）。
数据不足回调 Followin MCP（**tradfi 必传 `asset_type`，单 ticker 单调用**）。

## 6. 双层打分

```
最终分 = raw_score × 0.30 + reweight × 0.70   （clamp ≤5.0，溢出记脚注）
reweight = 时效×0.4 + 数据×0.3 + 争议×0.2 + 热度×0.1
时效 = base_timeliness × diffusion_factor   ← 必须显式列来源判定
```
**base**：<4h=5 / 4-12h=4 / 12-24h=3 / 24-48h=2。
**diffusion_factor**：财报会 / 监管机构 / 央行 0.5 → 头部通讯社 0.6 → 一线加密媒体 0.7 → 项目官号 0.75 → 国际 KOL 0.85 → 私域 / TG 0.9 → 中文小 KOL / 链上事件 0.95 → 多源独家 1.0。
⚠️ **"14h 全网热点给时效 5/5"是自查必抓错误。**

### 加分项（单候选总加分 cap +1.0）
| 项 | 分 | 判定要点（均须显式回答，禁裸加分） |
|---|---|---|
| 📌 bookmark | +0.3 | 30 天复用三问：对照表/矩阵/阈值清单？方法论手册？历史档案？情绪戏剧 / 单点快讯 / 当日点评 / 价格快照**全不算** |
| 👤 人物钩子 | +0.3 | 首句含顶级 IP 人物 |
| 🎭 调性 | ±0.3 | 4 题：合 voice-guide？合高表现模式？懂行朋友调性？避开低表现坑？命中红线 → -0.3。**情绪化 / BREAKING / 嘲讽是加分项不是扣分项** |
| 🎯 配额缺口 | +0.2 | 匹配当周最大 1-2 缺口类型 |
| 🅰️ 主引擎缺口 | +0.5 | **统计源以"实际已发"为准**：读本周已发帖落盘逐条判型统计——手动模式下"选过"≠"发过"；缺文件时 fallback 已选数（偏乐观）。本周已发 `#主引擎` < 周锚且当前候选属该类型 → +0.5。与 🎯 **不叠加，取高**；两源都缺→跳过 |
| 🌉 跨界传导 | +0.5 | Q1 ≥2 市场域 + 传导逻辑？Q2 ≥2 数据钉子？Q3 280 字讲清？三问显式 |
| 📐 框架公式 | +0.3 | 框架先行 / 时间尺度对比 / 三催化剂 + 大佬原话 任一。**强制激活**：产业链 / 框架型候选（产业链 / 光通信 / 存储 / AI capex / 算力 / 定价权 / 渗透率）3 角度里必须 ≥1 个套此公式，漏套 warn |
| 💡 thesis | +0.5 | hook 是论点句（转折对立结构 / 可证伪 / 指向二阶含义，≥2 命中）非描述句。每候选显式判定；描述句候选 ≥1 角度必须改写成论点句 |

**跟报型 thesis 硬门槛**：`content_type ∈ {#跟报, #叙事}` 且层 B ∈ {🟠,🔴} → 主推 hook 必须论点句，否则 B/C 须有论点句改写；都没有 → 不进 Top 5（独家 / 🟡 不受约束）。

## 7. 层 B 差异化严判（默认必跑 + 2h 缓存）

`BENCHMARK_KOLS + BASELINE_KOLS` × `twitter(action="user_tweets")` 近 24h → 落盘 `<WORK_DIR>/topic-engine-layer-b-$DATE.json`（含 `scan_timestamp`，<2h 复用缓存）。EXPECTED_KOL 数从配置派生，**勿写死**。

- **必抽数**：单账号原始返回 65-172K 字符 → **Agent 子进程内立刻 jq** 抽 `text`(280字) / `userName` / `createdAt` / `viewCount`；per-account cap：媒体号 20、个人 KOL 30。子进程返回 >10K 字符 → 拒收重跑。**禁止跳过基线组省 token。**
- **🧾 子进程回执（必做）**：只数自己写进 json 的 `scanned_kols` 长度 = 手写几个名字就能过、零真扫凭据。修复：主进程先生成 `SCAN_TS`（ms epoch，与 `scan_timestamp` 同值）显式传给每个层 B Agent；**每个 Agent 扫完 + jq 后用 Bash 落回执** `<WORK_DIR>/topic-engine-lb-receipt-<userName>-$DATE.json` = `{"userName":"…","raw_count":<原始推文数>,"scan_ts":<SCAN_TS>}`。自查按 `scan_ts == layer-b.scan_timestamp 且 (raw_count>0 或 scanned_empty)` 计 distinct KOL 数，须 ≥ EXPECTED_KOL，否则 FAIL。
  - **`scanned_empty`**：某 KOL 近 24h 真没发推（API 滞后 / 账号安静）→ 回执加 `"scanned_empty": true`，用来区分"扫了·窗口内 0 条"（合法）与"压根没扫"（缺回执）；只看 `raw_count>0` 会把两者混为一谈（空返回 ≠ 源挂）。`layer-b.json` **必须含 ms epoch 的 `scan_timestamp`**（回执绑定依赖它）。
- **4 标签**：🟢 独家（0 命中）/ 🟡 标杆已发（可借鉴角度）/ 🟠 基线已发（需差异化）/ 🔴 双 hit（**直接砍，永不豁免**）。
- **层 A 免费信号**：trend-scout 主 list 内自然出现的对标推文先查一遍（无额外调用）。
- **架构原则**：对标差异化只在本 skill 做；**禁止**以"对标在讲什么"为选题灵感；禁用自家产品的机械信号作灵感（自吹嫌疑）。
- **同主题查重切 Pattern**：跟报型候选（🟠/🔴/同梯队已发）对照 `<WORK_DIR>/twitter-published-patterns-$WEEK.json`，entity 重复时主 Pattern 必须切换（如 #5→#2/#3/#16）。文件不存在 → 跳过。

## 8. Top 5 输出与配比

- **Top 5 硬下限**；候选 3-4 → 降级 Top 3 + 警告；<3 → 拒绝出选题给三选项。极端可 Top 6（分差 <0.1 或豁免触发）。
- **差异化硬约束**：🔴 不进 Top 5；🟢 + 🟡 至少各 1。
- **配比三态**：周 `CATEGORY_CAP`（🔴 硬）/ 单批同类 ≥80%（🔴 硬砍）/ 单批单赛道 ≤40% + ≥3 categories（🟡 软，警告不砍）/ **抢先豁免**（🟢 凌驾软规则）。
- **抢先豁免**：`first_seen <2h` + `reweight ≥4.5` + 🟢 独家 三条件全中 → 强占名额不计配比（仍受 80% 上限），脚注显式标注。纯交易 / 🔴 永不豁免。
- **大事件强制位**：候选池含**行业级大事件**（头部公司旗舰产品 / 模型发布、旗舰级发布会、龙头重大落地）→ **强制占 Top 5 一位**（不需抢先豁免三条件，但仍须过纯交易排除 + 层 B 非 🔴 + thesis 论点句）。**漏采兜底**：池内无此类候选、但简报 / 用户提示当日确有大事件 → 输出顶部红色警告「大事件未进池，疑似上游漏采，建议补扫」。
- **周单主题上限预警**（防单引擎依赖：赢在主题恰好对、抗风险极差，同主题堆量边际递减）：出选题前读本周已发帖落盘，统计**单一主题 / 实体占比**。>60% → 本批优先非该主题 + 软提醒；>80% → 红色提醒 + 本批强制至少 1 条非该主题（除非该主题当日有 `raw ≥4.5` 抢先级 BREAKING）。文件缺 → 跳过（宁缺勿误）。
- 连续 ≥2 轮单赛道 ≥40% → 末尾红色提醒「上游信号偏单赛道，建议 trend-scout 专项扫」——**不在本端硬砍**。
- **每条标注**：金字塔档位（★×5 顶层 = 新品首测 / 真 BREAKING；★×4 = 异动 / KOL 冲突 / 宏观×交易；★×2 底层不上）+ 内容类型代号 + 预期 views 档位 + 对标借鉴提示。
- **周配额锚**（operations-plan 权威）：`MAIN_ENGINE_TYPES` 合计 ≥70% / 主引擎 ≥3 条 / 叙事型 2-3 / Bookmark 型 ≥3-4 / 日报 ≤10% / Thread 单批 ≤1。
- 末尾附：频次预算检查（当日已发 vs 普通日 ≤3 / 重大日 ≤5 / 突发日 ≤7）+ **一次到位决策块**（选哪条 / 什么形式 / 什么时间，三变量一次答）。

## 9. 落盘 + 简报追加

> ⚠️ **字段名以下表为准，禁止凭记忆另起命名**（字段名漂移曾致每次返工、简报满屏 null）。

| 文件 | 精确字段 |
|---|---|
| `topic-engine-layer-b-$DATE.json` | `scanned_kols[]`(≥EXPECTED_KOL) · `candidates_labels[]{id,label}` · `scan_timestamp`(ms epoch，回执绑定锚) |
| `topic-engine-lb-receipt-<userName>-$DATE.json` | `{userName, raw_count, scan_ts, scanned_empty?}` 子进程真扫凭据 |
| `topic-engine-quota-$WEEK.json` | `week_published_count` · 各类型 count · `category_pct`(0-1) · `main_engine_pct`(0-1)。**跨周文件 → 持久目录** |
| `topic-engine-top5-$DATE.json` | `top5[]{rank,id,title,content_type,pyramid_tier,layer_b_label,viral_potential,raw_score,reweight,final_score,layer_b_evidence,bonus,time_window?,angles[]}` · `angles[]{letter,pattern(整串如 "#4 历史平行线"),hook,reverse_consensus,counter_risk,closing_line,when_to_pick}` · 可选顶层 `diversity{}` `execution_order[]` `cut_candidates{}` |
| `topic-engine-readlog-$DATE.txt` | 第零步 Read 凭证 |
| 简报追加 `## 🏆 选题表 · HH:MM` | 7 段：元信息 / 一览表(12 列) / 多样性 / 配额警示 / 5 个选题块(共 15 角度) / 执行序 / 接驳；frontmatter `modes` 加"选题" |

> **latest 索引兜底**：若上游只写了无日期戳的 `-latest.txt`，本 skill 落盘时补写 `echo <候选json路径> > <候选目录>/trend-scout-candidates-$DATE-latest.txt`。

## 10. 输出前自查（任一不过禁止输出，补做重跑）

⓪ 第零步文档已读（有 readlog）① 候选池接力（模式自适应 floor）② 层 B 落盘 + ②.r 子进程回执真扫凭据 ③ 配比（`CATEGORY_CAP` / 主引擎 ≥70%）④ Top5 结构完整 ④.5 每个 angle 6 字段齐 ④.6 叙事型周配额 ⑤ 至少 1 条高传播潜力 ⑥ 简报追加（5 块 / 15 角度 / 7 段 / frontmatter）。

## 11. 接驳

→ tweet-composer：每角度含核心观点 / 数据支撑 / Hook / 形式建议 / 反向风险，拿到即写、无需再选题。
关键原则：**时效 > 一切**（6h 话题价值 10 倍于 24h）/ 绝不预测价格 / 数据为王 / 分歧 = 价值 / 开头金句决定成败。

## 参考文件
- `references/angle-templates.md` — 16 Pattern 详解与 Hook 模板
- `twitter-ops/references/operations-plan.md` — 配比与周配额权威
- `performance-review/references/patterns.md` — 高表现模式实证
