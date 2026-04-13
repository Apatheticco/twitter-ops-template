# Twitter运营AI Agent工作流 — Skill体系架构

## 定位

本框架适用于任何 Twitter/X 账号的日常运营。通过 AI Agent 实现从热点采集、选题、撰写、互动到复盘的完整闭环。

**使用前请先完成初始化**（见 README.md）：设定你的账号定位、人设语气、竞对列表、KOL目标等。

## 可用资源
- Followin MCP（热门话题、热榜、情报中心、搜索等）
- Premium MCP（Twitter API、金融数据、宏观数据、加密实时价格等）

## 模式控制

| 模式 | 触发 | 行为 |
|------|------|------|
| 🤖 自动 | "跑一轮" / 默认 | 全流程自动执行，按预设规则决策 |
| 🔧 手动 | "手动跑一轮" | 每个检查点暂停，等待用户确认 |

**默认自动，随时可拦** — 用户在自动模式中发消息即触发当前检查点暂停。

## 三条流水线 + 独立调用

### 主流水线：推文生产

```
trend-scout → 检查点① → topic-engine → 检查点② → tweet-composer → 检查点③ → 终稿
  (热点采集)    (话题筛选)    (选题排序)    (选题确认)    (推文撰写)     (草稿审核)
```

### 互动流水线：日常维护

```
engagement-manager（战略规划）
  ├── hot-comment（Outbound：去KOL帖子下评论引流）
  └── comment-ops（Inbound：运营自己评论区）
```

### 复盘流水线：定期优化

```
performance-review（数据分析） → content-vault（高表现入库） → topic-engine（反馈优化选题）
competitor-watch（竞对情报）  ↗
```

### 独立调用（用户手动触发）

| Skill | 格式 | 触发方式 |
|-------|------|---------|
| deep-write | 长文（1000-5000字） | "写篇深度文章" |
| thread-builder | Thread（3-15条） | "把这篇拆成Thread" |

## 数据流向

```
MCP数据采集
  │
  ├── Followin MCP（热榜、情报、搜索）
  └── Premium MCP（Twitter API、价格、宏观、链上）
  │
  ↓
trend-scout（汇总+清洗）
  ↓
topic-engine（筛选+排序+角度）← content-vault（历史模式参考）
  ↓                            ← competitor-watch（竞对空白区）
tweet-composer / deep-write（撰写）
  ↓
[发布]
  ↓
engagement-manager → hot-comment + comment-ops（互动执行）
  ↓
performance-review（数据复盘）→ content-vault（入库）
  ↓
反馈到 topic-engine + tweet-composer（策略优化）
```
