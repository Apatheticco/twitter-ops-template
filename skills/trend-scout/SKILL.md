---
name: trend-scout
description: "Crypto & macro market trend scanner — orchestrates MCP tools and data skills to collect breaking news, on-chain signals, macro data, trading signals, and CT buzz into a structured briefing. Use this skill whenever the user mentions finding trends, hot topics, market news, what's happening in crypto, morning briefing, news roundup, 热点, 新闻, 行情, 今日要闻, 早报, 市场动态, what happened overnight, daily scan, or any request to gather market intelligence before tweeting."
---

# 热点采集 Trend Scout

你的市场情报采集中枢。直接调用 MCP 工具拿一手数据，编排 Skill 做深度分析，输出结构化热点简报。

---

## 价格数据铁律

1. **单一信源**：简报中所有当前价格/涨跌幅，只能引用 `crypto_realtime_price_batch` 返回的数字。新闻标题、热门话题里的价格描述一律视为"历史叙述"，标注为叙事来源，不作为当前数据使用。
2. **简报强制分区**：输出简报必须分为「📊 实时数据区」（只放 API 返回的硬数据）和「📰 叙事摘要区」（新闻/KOL/事件，标注来源）。两个区的数字不混用。下游 topic-engine / tweet-composer 引用价格时，只能取实时数据区的数字。

---

## 数据采集层：工具 → Skill 双层架构

trend-scout 有两层数据来源：
- **MCP 工具层**（直接调用，速度快，数据粒度细）
- **Skill 层**（封装了多工具编排 + 分析逻辑，适合复杂场景）

优先用 MCP 工具直接拿数据，Skill 用于需要复杂分析逻辑的场景。

---

## ⚠️ 数据量控制规则（经实测验证）

以下工具返回数据量过大，**必须用 Agent 子进程调用**，在子进程内提取关键字段后再返回摘要：

| 工具 | 原始数据量 | 处理方式 |
|------|-----------|---------|
| open_trending_topic_ranks | ~86K/10条 | count≤5，或 Agent 处理 |
| twitter_advanced_search | ~99K/20条 | Agent 调用，只取 text/author/engagement |
| economic_calendar | ~1.5M/7000+条 | Agent 调用，只取 High impact + US/CN/EU |
| open_feed_list_trending | 含 full_content | 只取 title + content，丢弃 full_content |
| search_finance_news | 含 full_content | 只取 title + content，丢弃 full_content |

其余工具（kol_call_orders、top_traders_live、whale_trader_feeds、treasury_rates、market_analyst、open_feed_list_tag、open_feed_list_tag_opinions、open_search_feed、open_channel_feeds）数据量可控（<10K/10条），可直接在主进程调用。

---

## 工作流程

### 第一步：CT 热点 & 加密新闻（必跑）

**并行调用以下 MCP 工具：**

```
1. Followin 热门话题排行
   工具：open_trending_topic_ranks
   参数：count=5, lang="zh-cn"
   拿到：当前加密市场 Top 5 热点话题
   ⚠️ 注意：该工具返回数据量极大（每个话题含完整文章内容，10条≈86K字符）
   → count 控制在 5 以内，或用 Agent 子进程处理避免撑爆上下文

2. Followin 今日热榜 — 快讯
   工具：open_feed_list_trending
   参数：type="hot_news", count=15, lang="zh-cn"
   拿到：热门快讯 Top 15
   ⚠️ 数据处理：只提取 title + content（摘要），忽略 full_content 和 translated_full_content 字段（含完整文章正文，会严重膨胀数据量）

3. Followin 今日热榜 — 资讯
   工具：open_feed_list_trending
   参数：type="pop_info", count=15, lang="zh-cn"
   拿到：热门资讯 Top 15

4. Twitter/X 全球趋势
   工具：twitter_trends
   参数：woeid=1, count=30
   拿到：全球 Twitter 趋势话题
```

**如需深入某个热点，追加：**
```
5. Followin 全站搜索（定向深挖）
   工具：open_search_feed
   参数：keyword="[热点关键词]", type="all", sort_by="time"
   拿到：该热点的全维度信息（文章+推文+快讯）
   ⚠️ 关键词策略：搜索使用 AND 匹配，多词组合（如"Bittensor TAO Covenant"）容易零结果
   → 用单一实体名（如"Covenant AI"）或自然语义短语（如"Bittensor 去中心化"）
   → 突发事件建议并行搜索 2-3 个不同关键词组合提高命中率

6. Twitter 高级搜索（CT 舆论）
   工具：twitter_advanced_search
   参数：query="[关键词] lang:zh OR lang:en", queryType="Top"
   拿到：该话题的高互动推文，KOL 观点
   ⚠️ 注意：返回数据极大（~20条推文≈99K字符，含完整嵌套结构）
   → 必须用 Agent 子进程调用，只提取 text/author/likeCount/retweetCount/viewCount
```

### 第二步：链上 & 交易所异动（必跑）

**并行调用 Followin 情报中心：**

```
1. 极端资金费率警报
   工具：open_channel_feeds
   参数：code="fund_movement", count=20, lang="zh-cn"
   拿到：极端资金费率警报（如"ONG资金费率-1.11%"）
   ⚠️ 注意：此频道实际返回的是资金费率异常警报，而非大额转账/鲸鱼异动
   → 真正的鲸鱼/大额资金异动请用第三步的 whale_trader_feeds（Premium MCP）

2. 量价异动
   工具：open_channel_feeds
   参数：code="quant_signal", count=20, lang="zh-cn"
   拿到：价格突破、交易量异常

3. Token 解锁
   工具：open_channel_feeds
   参数：code="token_unlock", count=10, lang="zh-cn"
   拿到：近期解锁事件

4. 上币/下架
   工具：open_channel_feeds
   参数：code="listing_delisting", count=10, lang="zh-cn"
   拿到：交易所上下架动态

5. 项目重大事件
   工具：open_channel_feeds
   参数：code="altcoin_update", count=10, lang="zh-cn"
   拿到：项目升级、合作、事故等
```

### 第三步：交易信号 & 大户动向 & TG 情报（建议跑）

**并行调用 Premium MCP：**

```
1. KOL 喊单
   工具：kol_call_orders_24h
   参数：limit=50
   拿到：过去 24h KOL 喊单汇总（token + 方向 + 作者）

2. 专业交易员实盘
   工具：top_traders_live_24h
   参数：limit=50
   拿到：Top 19 交易员实际持仓变化

3. 鲸鱼链上异动
   工具：whale_trader_feeds
   参数：hours=24, limit=50
   拿到：鲸鱼钱包大额操作
   ⚠️ 格式：返回纯文本拼接（非结构化JSON），每条含时间戳/交易员名/Token/方向/仓位/PNL/清算价

4. TG 频道情报（多维度并行）
   工具：tg_kol_feeds
   并行调用多个 category：
   - tg_kol_feeds(category="macro", hours=24, limit=30)         → 宏观讨论
   - tg_kol_feeds(category="trading_signal", hours=24, limit=30) → 交易信号
   - tg_kol_feeds(category="narrative", hours=24, limit=30)      → 叙事/热点话题
   - tg_kol_feeds(category="onchain_data", hours=24, limit=30)   → 链上数据分析
   拿到：TG 社区各维度实时讨论，覆盖中英文 KOL 频道
   → 重点提取：TG 共识方向、与 Twitter CT 的情绪差异、独家信号（TG先于Twitter传播的消息）

5. TG 精选日报
   工具：open_feed_list_tg_daily
   参数：count=10, lang="zh-cn"
   拿到：TG 频道精选日报摘要

→ 交叉比对：KOL 喊单 vs 大户实盘 vs TG 社区共识，找多空分歧
→ TG-Twitter 情绪差异 = 信息差 = 高价值推文素材
→ 分歧越大 = 推文价值越高
```

### 第四步：宏观数据（建议跑）

**选择性调用，取决于当天是否有重要宏观事件：**

```
1. 经济日历
   工具：finance_tool_economic_calendar
   拿到：今日/本周经济数据发布时间表
   判断：是否有 CPI/非农/FOMC 等重磅数据
   ⚠️ 注意：该工具无过滤参数，返回全球全部事件（7000+条/1.5M字符）
   → 必须用 Agent 子进程调用，只提取 impact="High" 且 country="US"/"CN"/"EU" 的事件

2. 美债利率
   工具：finance_tool_treasury_rates
   拿到：各期限国债收益率，判断利率环境

3. 宏观新闻（跨 30+ 财经媒体搜索）
   工具：search_finance_news
   参数：keyword="[宏观关键词]", users=[全部媒体列表]
   拿到：Bloomberg/Reuters/CNBC/WSJ 等主流媒体报道
   ⚠️ 数据处理：只提取 title + content（摘要），忽略 full_content 字段（5条≈24.7K字符）

4. 美股涨跌榜
   工具：finance_tool_biggest_gainers + finance_tool_biggest_losers
   拿到：美股异动，寻找与加密市场的关联

5. FRED 宏观指标（按需）
   工具：fred_get_series
   参数：series_id="DGS10"(10Y收益率) / "CPIAUCSL"(CPI) 等
   拿到：最新宏观数据点
```

**或调用 Skill 获取结构化分析：**
```
- /10_macro-morning-brief  → 一站式宏观晨报
- /08_btc-macro-dashboard  → BTC 宏观环境 0-100 评分
```

### 第五步：实时价格快照（必跑）

```
加密货币价格
工具：crypto_realtime_price_batch
参数：symbols="BTC,ETH,SOL,BNB,XRP,DOGE,ADA,AVAX,DOT,MATIC"
拿到：Top 10 加密货币实时价格+涨跌幅

传统资产价格（如需宏观交叉分析）
工具：realtime_price
分别查询：symbol="gold" / "spx" / "DXY" / "usdjpy"
拿到：黄金、标普500、美元指数、日元汇率
```

### 第六步：社区舆论深挖（按需）

```
1. 特定 Token 深挖（当某 Token 频繁出现在热点中）
   工具：open_feed_list_tag
   参数：symbol="[TOKEN]", type="key_events"
   +
   工具：open_feed_list_tag_opinions
   参数：symbol="[TOKEN]"
   拿到：该 Token 的重要事件 + KOL 观点汇总
```

**或调用 Skill：**
```
- /07_tg-channel-intel    → TG 频道深度聚合（10 类频道交叉分析）
- /05_token-buzz-views    → 单 Token 全维度舆论
```

### 第七步：CT KOL 动态监控（按需）

**直接用 Twitter MCP 拉 KOL 最新推文：**

```
工具：twitter_user_last_tweets
参数：userName="[KOL用户名]", includeReplies=false

批量监控（参考 source-list.md 中的 KOL 列表）：
- CryptoHayes（Arthur Hayes）
- DegenSpartan
- WClementeIII
- Phyrex_Ni
- 0xCryptowizard
...

→ 重点寻找：KOL 之间的观点分歧（多空分歧最有推文价值）
```

---

## 整合分析 & 输出

### 交叉比对：识别高价值信号

将所有采集到的数据做交叉分析，寻找以下模式：

| 信号类型 | 识别方法 | 推文价值 |
|---------|---------|---------|
| **多源共振** | 同一事件在 ≥2 个数据源出现 | ★★★★★ |
| **数据-叙事背离** | 链上数据和市场情绪方向相反 | ★★★★★ |
| **KOL-大户分歧** | KOL 喊多但大户在减仓（或反之） | ★★★★★ |
| **TG-Twitter情绪差异** | TG 社区共识与 Twitter CT 情绪方向不同 | ★★★★★ |
| **TG抢先信号** | 消息在 TG 传播但 Twitter 尚未讨论 | ★★★★★ |
| **抢先窗口** | 事件 <6h 且 Twitter 讨论量低 | ★★★★ |
| **资金异动+价格联动** | 大额转账后价格开始异动 | ★★★★ |
| **宏观-加密联动** | 宏观数据影响加密市场情绪 | ★★★ |

### 结构化输出：每条热点

```
### [分类emoji] 标题（一句话概括）

**数据来源**：[哪个 MCP 工具/Skill + 原始链接（如有）]
**重要性**：⭐⭐⭐⭐ (4/5)
**时效性**：约 X 小时（>24h 标注"时效递减"，>48h 标注"可能过时"）
**多源验证**：[✅ 已交叉验证 / ⚠️ 单源未验证]
**核心内容**：2-3 句话说明事件本身
**关键数据**：[具体数字——价格、TVL、持仓量、资金费率等]
**反向风险**：1 句话指出对立面或潜在风险
**推文潜力**：适合哪种角度（锐评/数据/故事/Thread）
```

### 完整简报模板

```
# 📋 每日热点简报 — [日期]

## 📊 实时数据区（仅限 API 返回的硬数据）

### ⚡ 数据采集概览
- 采集时间：[时间戳]
- 已调用工具：[列出本次实际调用了哪些 MCP 工具和 Skill]

### 价格快照（来源：crypto_realtime_price_batch）
- BTC：$XX,XXX (24h ±X.X%)
- ETH：$X,XXX (24h ±X.X%)
- [其他代币...]

### 大户持仓快照（来源：top_traders_live_24h / whale_trader_feeds）
[交易员实盘持仓变化，含具体仓位/PnL数字]

### 数据信号（来源：open_channel_feeds）
[链上异常、资金费率异动、量价异常]

---

## 📰 叙事摘要区（新闻/KOL/事件，标注来源）
⚠️ 此区域价格数字为新闻发布时的历史数据，非实时。下游引用价格只取实时数据区。

### 🔥 必关注（Top 3-5）
[最重要的事件，按 重要性×时效性 排序]
[每条包含完整的结构化分析]

### 🐋 资金流向 & 交易信号
[KOL 喊单 vs 大户实盘对比]
[多空分歧分析]
- 来源：kol_call_orders_24h + top_traders_live_24h + whale_trader_feeds

### 🏛️ 宏观动态
[央行、政策、经济数据]
- 来源：finance_tool_economic_calendar + treasury_rates + search_finance_news

### 💬 社区风向
[Twitter 热议 + TG 共识/分歧]
- 来源：twitter_advanced_search + tg_kol_feeds + open_feed_list_tg_daily

### 📝 选题建议
基于以上热点，推荐今日发推方向：
1. [热点A] — 角度建议 — 理由 — 时效窗口 — 数据支撑度
2. [热点B] — 角度建议 — 理由 — 时效窗口 — 数据支撑度
3. [热点C] — 角度建议 — 理由 — 时效窗口 — 数据支撑度

### ⚠️ 未验证信息
[单源信息、传闻、需进一步确认的消息]
```

---

## 补充扫描（热点匮乏时触发）

当常规采集（Step 1-5）结果不理想时，启动补充扫描拉取更广泛的新闻资讯。

**触发条件：**
- **自动触发**：下游 topic-engine 时效过滤后可用话题 < 2 个，自动回调补充扫描
- **手动触发**：用户指令 "热点不够" / "再扫一轮" / "补充扫描"

**补充扫描工具（并行调用）：**

```
1. 跨媒体财经新闻搜索
   工具：search_finance_news
   参数：keyword="crypto OR bitcoin OR ethereum", users=[全部媒体]
   拿到：Bloomberg/Reuters/CNBC/WSJ 等 30+ 主流财经媒体最新报道
   ⚠️ 数据处理：只提取 title + content（摘要），忽略 full_content 字段
   → 重点寻找：主流媒体关注但 CT 尚未热议的话题（信息差 = 抢先窗口）

2. 最新加密新闻聚合
   工具：finance_tool_news_crypto_latest
   拿到：最新加密货币新闻聚合
   → 重点寻找：刚发生的事件、未被 Followin 热榜收录的新消息

3. 今日宏观经济日历
   工具：finance_tool_economic_calendar
   拿到：今日/本周经济数据发布时间表
   ⚠️ 注意：返回数据极大（7000+条），必须用 Agent 子进程调用
   → 只提取 impact="High" 且 country="US"/"CN"/"EU" 的事件
   → 重点寻找：即将发布的重磅数据（CPI/非农/FOMC/PMI）作为预热选题
```

**补充扫描输出规则：**
- 补充结果追加到原简报的「📰 叙事摘要区」，标注 `[补充扫描]` 来源
- 如发现新的价格相关事件，同步刷新「📊 实时数据区」的价格快照
- 补充扫描后仍无可用话题 → 输出警告，建议用户手动补充关注话题

---

## 执行模式

### 🟢 完整模式（"跑一遍热点" / "开始今日运营"）

调用步骤 1-6 全部，约 3-5 分钟：
```
并行 Wave 1（CT 热点 + 链上异动 + 价格快照）：
  - open_trending_topic_ranks
  - open_feed_list_trending × 2
  - twitter_trends
  - open_channel_feeds × 5
  - crypto_realtime_price_batch

并行 Wave 2（交易信号 + TG情报 + 宏观）：
  - kol_call_orders_24h
  - top_traders_live_24h
  - whale_trader_feeds
  - tg_kol_feeds × 4（macro/trading_signal/narrative/onchain_data）
  - open_feed_list_tg_daily
  - finance_tool_economic_calendar
  - finance_tool_treasury_rates

按需 Wave 3（深挖）：
  - twitter_advanced_search / open_search_feed
  - /08_btc-macro-dashboard
```

### 🟡 快速模式（"快速扫一下"）

只跑 Wave 1（~1 分钟）：
```
  - open_trending_topic_ranks
  - open_feed_list_trending (hot_news)
  - open_channel_feeds (fund_movement + quant_signal)
  - crypto_realtime_price_batch
→ 输出：Top 3 热点 + 价格快照 + 选题建议
```

### 🔴 突发模式（"刚出了个大事" / "[事件名]"）

定向深挖单个事件（~1 分钟）：
```
  - open_search_feed × 2-3（用不同关键词并行搜索，提高命中率）
    关键词策略：实体名 + 自然语义短语 + Token符号(flash模式)
    例："Covenant AI" / "Bittensor 去中心化" / "TAO"(type=flash)
  - twitter_advanced_search(query=关键词, queryType="Latest")
    → 突发事件中最有价值的工具（实时性最强，无索引延迟）
  - crypto_realtime_price_batch(相关 Token)
  - 如涉及宏观：search_finance_news(keyword=关键词)
    → 零结果时本身是有价值信号：主流媒体未报道 = 抢先窗口仍在
→ 输出：事件速报 + 多源验证 + 初步角度建议
→ 目标：5 分钟内从发现到给出可发推的内容方向
```

### 🟠 补充模式（"热点不够" / topic-engine 自动回调）

补充扫描单独跑（~1 分钟）：
```
并行：
  - search_finance_news(keyword="crypto OR bitcoin OR ethereum")
  - finance_tool_news_crypto_latest
  - finance_tool_economic_calendar（Agent 子进程，只取 High impact）
→ 输出：追加到现有简报，标注 [补充扫描] 来源
→ 回传给 topic-engine 重新进入时效过滤和选题流程
```

### 🔵 深度模式（"深挖 [Token/话题]"）

完整模式 + 单点深挖（~5-8 分钟）：
```
  - 完整模式所有工具
  +
  - open_feed_list_tag(symbol=TOKEN, type="key_events")
  - open_feed_list_tag_opinions(symbol=TOKEN)
  - twitter_advanced_search(query="$TOKEN", queryType="Top")
  - market_analyst(symbol=TOKEN, indicators="all")
→ 输出：完整简报 + Token 深度分析（基本面+技术面+舆论）
```

---

## 关键原则

- **MCP 工具优先**：能直接用工具拿数据就不绕 Skill，更快更精确
- **并行采集**：Wave 1 的工具全部并行调用，不串行等待
- **交叉验证**：≥2 个源确认的事件才标为"已验证"，单源标注"未验证"
- **数据 > 叙事**：有具体数字的热点排在纯叙事热点前面
- **时效递减**：>24h 降级，>48h 一般不作为首选推文素材
- **必须有反向风险**：每条热点都要指出对立观点
- **不预测价格**：只描述趋势、数据和逻辑
- **KOL-大户交叉**：喊单和实盘的分歧是最有价值的推文素材

## 参考资源

- `references/source-list.md` — KOL 监控列表、数据源 URL、API 示例（WebSearch 补充验证时参考）
