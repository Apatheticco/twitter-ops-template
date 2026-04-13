---
name: competitor-watch
description: "Monitor competitor crypto/macro Twitter accounts — track their content strategy, engagement patterns, topic choices, and growth. Use this skill whenever the user mentions competitor monitoring, competitive analysis, 竞对监控, 竞品分析, what are others tweeting, 同行在发什么, account comparison, benchmark against peers, 对标账号, or any request to analyze or track other crypto/macro Twitter accounts."
---

# 竞对监控 Competitor Watch

你的竞对情报助手。追踪同赛道KOL和竞对账号的内容策略、互动数据和增长趋势，为你的运营提供参考。

---

## 核心定位

```
competitor-watch（竞对情报）→ topic-engine（借鉴选题方向）
                            → engagement-manager（发现互动目标）
                            → performance-review（对标复盘）
```

周频为主的分析 skill，不需要每天跑。

---

## MCP 工具集

```
账号基本信息：
  工具：twitter_user_info / twitter_user_about
  拿到：粉丝数、发推数、简介、创建时间

最新推文：
  工具：twitter_user_last_tweets
  参数：userName="[竞对用户名]", includeReplies=false
  拿到：近期推文列表（含互动数据）

搜索竞对提到你的推文：
  工具：twitter_advanced_search
  参数：query="from:[竞对] [你的用户名或关键词]", queryType="Latest"
  ⚠️ Agent 子进程处理（数据量大）

批量获取账号信息：
  工具：twitter_batch_user_info
  参数：userNames="[逗号分隔的用户名列表]"
  拿到：批量粉丝数对比
```

---

## 工作流

### 1. 竞对账号管理

维护一份监控列表（存储在 `references/competitor-list.md`）：

**账号分类：**
| 类型 | 说明 | 数量建议 |
|------|------|---------|
| 🎯 直接竞对 | 同定位（加密交易+宏观）的中文账号 | 3-5个 |
| 📊 学习对象 | 做得好的英文加密KOL | 3-5个 |
| 🏛️ 宏观类 | 宏观交易/经济分析类账号 | 2-3个 |
| 🆕 新兴账号 | 增长快的新账号，值得观察 | 2-3个 |

### 2. 内容策略分析

对每个监控账号，定期分析：

**发布模式：**
- 发推频率（日/周）
- 发布时间分布
- 内容类型比例（快讯、分析、线程、meme）
- 话题覆盖范围

**互动表现：**
- 平均点赞/转发/评论数
- 高互动推文的共同特征
- 互动率（互动数/粉丝数）
- 粉丝增长趋势

**内容质量：**
- 信息来源质量（一手源还是转述）
- 观点独特性
- 数据使用频率和质量
- 风格辨识度

### 3. 爆款分析

当竞对账号出现高互动推文时，分析：

```
### 🔥 爆款推文分析

**账号**：@username
**推文**："[内容摘要]"
**数据**：❤️ X | 🔄 X | 💬 X

**爆款原因分析**：
1. 话题：[为什么这个话题火]
2. 角度：[独特切入点是什么]
3. 时机：[发布时间是否关键]
4. 格式：[排版/线程/图文]

**你可以怎么借鉴**：
- 角度A：[你的版本会怎么写]
- 角度B：[反向/补充角度]
- 注意：不要抄袭，要有自己的独特观点
```

### 4. 差异化洞察

定期（每周）输出差异化报告：

```
## 📊 竞对周报 — [日期范围]

### 话题覆盖对比
| 话题 | 你 | 竞对A | 竞对B | 竞对C |
|------|---|-------|-------|-------|
| BTC行情 | ✓ | ✓ | ✓ | ✗ |
| 链上数据 | ✓ | ✗ | ✓ | ✗ |
| 宏观分析 | ✓ | ✗ | ✗ | ✓ |
| [空白区] | ✗ | ✗ | ✗ | ✗ |

### 你的差异化优势
1. [你做得比竞对好的地方]
2. [你的独特定位]

### 改进机会
1. [竞对做得好但你没做的]
2. [空白区域的机会]

### 本周值得借鉴的爆款
[2-3条竞对爆款 + 你的借鉴思路]
```

### 5. 实时追踪

设置关键词追踪，发现竞对动态：
- 竞对提到你账号的推文
- 竞对讨论你覆盖过的话题（看观点异同）
- 竞对的粉丝增长异常（可能有爆款或推广）

---

## 与上下游的衔接

### → 输出给
- **topic-engine**：竞对爆款话题 → 借鉴选题方向（用不同角度写）
- **engagement-manager**：竞对账号列表 → Outbound 互动目标
- **performance-review**：竞对数据 → 对标复盘基准

### ← 接收
- **engagement-manager**：互动中发现的新兴竞对账号 → 加入监控列表
- **trend-scout**：热点话题 → 检查竞对是否已覆盖

---

## 关键原则

- **学习不抄袭**：借鉴策略和角度，但内容必须原创
- **关注差异化**：找到竞对没覆盖的空白区域
- **数据说话**：用互动数据判断什么有效，而非主观感觉
- **不要过度焦虑**：竞对分析是参考，不是枷锁
- **定期而非实时**：每周一次深度分析就够，不需要时刻盯着

## 参考资源

查看 `references/competitor-list.md` 管理你的监控账号列表。
