# Twitter运营AI Agent工作流 — Skill体系架构

## 定位
加密货币交易 + 宏观交易视角，日更中文为主，面向Crypto Twitter（CT）社区。

## 可用资源
- Twitter/X API（发推、读时间线、互动）
- Followin MCP（9个工具：热门话题、热榜、情报中心、搜索、项目数据、KOL观点等）
- Premium MCP（200+工具：Twitter API、金融数据、FRED宏观、加密实时价格、技术分析等）

## 模式控制

工作流支持两种运行模式：

| 模式 | 触发 | 行为 |
|------|------|------|
| 🤖 自动 | "跑一轮" / 默认 | 全流程自动执行，按预设规则决策 |
| 🔧 手动 | "手动跑一轮" | 每个检查点暂停，等待用户确认 |

**默认自动，随时可拦** — 用户在自动模式中发消息即触发当前检查点暂停。

## Skill体系总览（1个调度器 + 11个子Skill）

```
skills/
├── twitter-ops/                        ← 主调度器（模式控制 + 流程串联）
│   ├── SKILL.md
│   └── references/
│       ├── voice-guide.md              ← 人设 & 语气指南
│       └── content-calendar.md         ← 内容日历模板
│
├── trend-scout/                        ← Skill 1: 热点采集（4种模式：Quick/Full/Breaking/Deep）
│   ├── SKILL.md
│   └── references/
│       └── source-list.md              ← 数据源 & KOL列表
│
├── topic-engine/                       ← Skill 2: 选题排序 & 角度生成（P0-P3优先级）
│   ├── SKILL.md
│   └── references/
│       └── angle-templates.md          ← 11个角度模板
│
├── tweet-composer/                     ← Skill 3: 推文撰写（单推/Thread/引用推）
│   ├── SKILL.md
│   └── references/
│       └── tweet-styles.md             ← 推文风格 & 案例库
│
├── deep-write/                         ← Skill 4: 长文写作（1000-5000字，20+作家风格库）
│   └── SKILL.md
│
├── thread-builder/                     ← Skill 5: 长文→Thread拆解
│   └── SKILL.md
│
├── engagement-manager/                 ← Skill 6: 互动战略层（规划+追踪+KOL关系管理）
│   ├── SKILL.md
│   └── references/
│       └── reply-strategies.md         ← 回复策略模板
│
├── hot-comment/                        ← Skill 7: 主动出击（Outbound评论）
│   └── SKILL.md
│
├── comment-ops/                        ← Skill 8: 评论区运营（Inbound回复，5级分类）
│   └── SKILL.md
│
├── competitor-watch/                   ← Skill 9: 竞对监控 & 差异化分析
│   ├── SKILL.md
│   └── references/
│       └── competitor-list.md          ← 监控账号列表
│
├── performance-review/                 ← Skill 10: 数据复盘 & 策略优化
│   ├── SKILL.md
│   └── references/
│       └── metrics-guide.md            ← 关键指标定义
│
└── content-vault/                      ← Skill 11: 内容素材库（历史高表现推文入库+复用）
    ├── SKILL.md
    ├── references/
    │   ├── vault.md                    ← 素材库主文件（运行后生成）
    │   └── patterns.md                 ← 成功模式详解
    └── scripts/
        └── tweet_analyzer.py           ← 推文数据批量分析脚本
```

## 三条流水线 + 独立调用

### 主流水线：推文生产（自动/手动）

```
trend-scout → 检查点① → topic-engine → 检查点② → tweet-composer → 检查点③ → 终稿
  (热点采集)    (话题筛选)    (选题排序)    (选题确认)    (推文撰写)     (草稿审核)
```

检查点在手动模式下暂停等待用户，自动模式下按规则跳过。
主流水线仅产出推文级内容（单推/Thread/引用推）。

**突发快速通道：**
```
"突发：[事件]" → trend-scout(Breaking) → topic-engine(P0) → tweet-composer(单推) → 终稿
目标：15分钟内完成
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

| Skill | 格式 | 触发方式 | 说明 |
|-------|------|---------|------|
| deep-write | 长文（1000-5000字） | "写篇深度文章" / "写一篇关于XXX的分析" | 重型任务，不进自动流水线 |
| thread-builder | Thread（3-15条） | "把这篇拆成Thread" | 将已有长文转化为Thread |

可串联：deep-write → thread-builder → tweet-composer（预告推文），但每步需用户触发。

## 内容格式分工

| Skill | 格式 | 长度 | 场景 | 归属 |
|-------|------|------|------|------|
| tweet-composer | 单推 | ≤140中文字 | 快评、数据帖、即时反应 | 主流水线 |
| tweet-composer | Thread | 3-10条 | 多维度分析、事件梳理 | 主流水线 |
| tweet-composer | 引用推 | ≤80中文字 | 借势评论 | 主流水线 |
| deep-write | 长文 | 1000-5000字 | 深度分析、研报、专题 | 独立调用 |
| thread-builder | Thread（转化） | 3-15条 | 已有长文→Thread拆解 | 独立调用 |

## 数据流向

```
MCP数据采集
  │
  ├── Followin MCP（热榜、情报、搜索、项目数据）
  └── Premium MCP（Twitter API、价格、宏观、链上、KOL喊单）
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

## 人设基调

- 强观点、简洁表达
- 允许爆粗和幽默，但不强行
- 速度 > 完美，先推重要的
- 每个分析必须有反向风险
- 数据驱动，用数字说话
- 不做涨跌预测，不给投资建议
- 一手源 > 二手源
- 中文为主，行业术语用英文

详见 `skills/twitter-ops/references/voice-guide.md`
