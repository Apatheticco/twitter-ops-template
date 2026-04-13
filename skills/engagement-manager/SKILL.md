---
name: engagement-manager
description: "Strategic engagement planner and tracker — coordinates hot-comment (outbound) and comment-ops (inbound), manages KOL relationships, tracks engagement metrics, and plans daily interaction priorities. Use this skill whenever the user mentions 互动管理, engagement strategy, 互动规划, 今天互动什么, 互动数据, 粉丝增长, relationship management, engagement report, 互动复盘, who to engage with, or any request to plan, track, or review Twitter engagement strategy."
---

# 互动管理 Engagement Manager

互动战略层。不做具体的评论和回复（那是 hot-comment 和 comment-ops 的活），而是做规划、协调和追踪。

---

## 核心定位

```
engagement-manager（战略规划+数据追踪）
  ├── hot-comment（执行：去别人推文下评论 — outbound）
  └── comment-ops（执行：管理自己评论区 — inbound）
```

**三者分工：**

| Skill | 职责 | 比喻 |
|-------|------|------|
| engagement-manager | 每日规划+关系管理+数据追踪 | 指挥官 |
| hot-comment | 主动出击，去别人推文下抢热评 | 前锋 |
| comment-ops | 防守阵地，运营自己评论区 | 后卫 |

---

## 工作流程

### 第一步：每日互动规划

每天开始运营前，生成今日互动计划：

**1.1 Outbound 目标（交给 hot-comment 执行）**

```
扫描工具：
  - twitter_user_last_tweets（监控KOL列表的最新推文）
  - twitter_advanced_search（当日热点话题下的高互动推文）
  → 用 Agent 子进程批量扫描，筛选出值得评论的目标

筛选标准：
  - 发布 <2h + 已有 50+ 互动
  - 评论区未饱和（<100条）
  - 话题与账号定位相关
  - 优先选择：有互动历史的KOL > 同量级账号 > 大V
```

**输出：今日 Outbound 目标清单**
```
| 优先级 | 目标推文 | 作者 | 互动量 | 评论策略 |
|--------|---------|------|--------|---------|
| 🔴 必评 | [推文摘要] | @KOL_A | ❤️500 💬30 | 数据补充型 |
| 🟡 建议 | [推文摘要] | @KOL_B | ❤️200 💬15 | 反向观点型 |
| ... | ... | ... | ... | ... |
```

**1.2 Inbound 检查（交给 comment-ops 执行）**

```
扫描工具：
  - twitter_tweet_replies（拉取自己近期推文的评论）
  - twitter_user_mentions（查看被@/引用的情况）

检查项：
  - 有无 S级质疑需要紧急回复？
  - 有无 KOL 回复了你？（高价值互动）
  - 有无可借势的评论？
```

**1.3 今日互动预算**

根据当天的内容发布计划，分配互动精力：

| 日类型 | Outbound 评论 | Inbound 回复 | 主动发推 |
|--------|-------------|-------------|---------|
| 热点日（CPI/大事件） | 3-5条 | 全部S/A级 | 2-3条 |
| 普通日 | 5-8条 | S/A/B级 | 1-2条 |
| 低谷日（无热点） | 8-10条 | 全级别 | 0-1条 |

热点日减少 outbound（自己的推文就是流量入口），低谷日加大 outbound（主动找曝光）。

### 第二步：KOL 关系网络管理

维护一个动态的 KOL 互动关系表：

**2.1 关系层级**

| 层级 | 定义 | 互动策略 |
|------|------|---------|
| 🟢 已建立 | 对方回复/互动过你 ≥3次 | 维护关系，定期互动，可以@对方讨论 |
| 🟡 认识中 | 对方回复/互动过你 1-2次 | 继续高质量评论，争取加深印象 |
| ⚪ 未接触 | 从未互动 | 通过 hot-comment 在其推文下出现 |

**2.2 关系追踪（MCP工具）**

```
查看互动历史：
  工具：twitter_user_last_tweets + twitter_tweet_replies
  用途：回顾与某KOL的历史互动记录

查看对方近态：
  工具：twitter_user_last_tweets
  参数：userName="[KOL用户名]"
  用途：了解对方最近在聊什么，找到自然的互动切入点

查看粉丝重叠：
  工具：twitter_user_followers / twitter_user_followings
  用途：发现共同关注者，识别圈子
```

**2.3 每周关系维护清单**

```
- [ ] 与 ≥3个「已建立」关系的KOL互动（维护）
- [ ] 在 ≥5个「认识中」KOL的推文下评论（加深）
- [ ] 尝试接触 ≥2个「未接触」的目标KOL（拓展）
- [ ] 检查是否有KOL关注了你（及时互动回应）
```

### 第三步：互动数据追踪

**3.1 单推互动分析**

对每条已发布的推文追踪表现：

```
扫描工具：
  - twitter_tweets_by_ids（获取推文的最新互动数据）
  - twitter_tweet_replies（获取评论数和内容）

追踪指标：
  - 浏览量 (Views)
  - 互动率 (Engagement Rate = (点赞+评论+转发) / 浏览量)
  - 评论质量（S/A级评论占比）
  - 二次传播（被引用推/转推的情况）
```

**3.2 Outbound 评论效果追踪**

```
追踪维度：
  - 哪条评论获得了原作者回复？（最高价值）
  - 哪条评论获得了最多点赞？（曝光最高）
  - 哪些KOL的推文下评论效果最好？（后续优先评论）
  - 哪种评论类型转化率最高？（深度/犀利/幽默/数据）
```

**3.3 周度互动报告**

```
━━━━━━━━━━━━━━━━━━━━━━━
📊 周度互动报告 — [日期范围]
━━━━━━━━━━━━━━━━━━━━━━━

## 📈 核心指标
- 本周发推：X 条
- 总浏览量：XXX,XXX
- 平均互动率：X.X%
- 新增粉丝：+XXX（推测归因见下）
- Outbound 评论：XX 条
- 获得原作者回复：X 条

## 🏆 本周最佳
- 最高互动推文：[推文摘要] — ❤️XX 💬XX 🔄XX 👁XXXX
- 最佳 Outbound 评论：[评论摘要] — 在 @XXX 推文下获 XX 赞
- 最有价值互动：@XXX 回复了你的评论（粉丝XXK）

## 📊 内容类型表现对比
| 类型 | 发布数 | 平均浏览 | 平均互动率 | 最佳表现 |
|------|--------|---------|-----------|---------|
| 单推-锐评 | X | XXX | X.X% | [摘要] |
| 单推-数据 | X | XXX | X.X% | [摘要] |
| Thread | X | XXX | X.X% | [摘要] |
| 引用推 | X | XXX | X.X% | [摘要] |

## 🐋 KOL 关系进展
- 新建立关系：@XXX（首次回复你）
- 关系升级：@XXX（第3次互动）
- 需要维护：@XXX（2周未互动）

## 💡 下周策略建议
- 内容方向：[基于数据的建议]
- Outbound 重点：[哪些KOL/话题]
- 优化建议：[哪种类型表现差，需要调整]
━━━━━━━━━━━━━━━━━━━━━━━
```

### 第四步：粉丝增长归因

**分析粉丝增长来自哪里：**

```
渠道归因（推测性）：
  - 自己发推带来的（推文互动→主页访问→关注）
  - Outbound评论带来的（评论曝光→主页访问→关注）
  - 被大V转发/回复带来的（单次事件驱动）
  - 自然增长（搜索/推荐算法）

追踪方法：
  - 对比发推日 vs 非发推日的粉丝增量
  - 对比有 Outbound 评论 vs 无评论日的增量
  - 记录被大V互动后的粉丝跳变
```

---

## 与上下游的衔接

### ← 接收
- **trend-scout**：当日热点（用于确定 Outbound 评论方向）
- **hot-comment**：已发布的评论列表（追踪效果）
- **comment-ops**：评论区健康度报告（监控自己的阵地）
- **tweet-composer**：已发布的推文（追踪表现）

### → 输出
- **hot-comment**：今日 Outbound 目标清单（评论谁）
- **comment-ops**：需要紧急处理的 Inbound 评论
- **topic-engine**：基于互动数据的选题建议（什么类型的内容表现好）
- **performance-review**：周度互动数据（纳入整体复盘）

---

## 关键原则

- **规划先行**：每天先花5分钟做互动规划，不要盲目刷
- **质量 > 数量**：3条有深度的评论 > 10条水评
- **关系是资产**：KOL互动关系是长期积累的，不是一次性的
- **数据驱动**：用互动数据指导策略，不凭感觉
- **热点日守、低谷日攻**：有热点时专注自己的内容，没热点时主动出击
- **不打口水仗**：超过两轮的争论立即撤出
