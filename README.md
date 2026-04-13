# Twitter Ops Workflow

> 基于 Claude Code 的 Twitter 日运营 AI Agent 工作流框架
> 适用于任何 Twitter/X 账号的内容运营

---

## 这是什么

一个 **1 个主调度器 + 11 个子 Skill** 的 Twitter 运营系统。覆盖从热点采集、选题、撰写、互动、竞对监控到数据复盘的完整运营闭环。

所有 Skill 以 Markdown 文件（`SKILL.md`）形式存在，Claude Code 读取后按流水线逻辑串联执行。

---

## 前置要求

### MCP 工具（数据源）

| MCP Server | 用途 |
|------------|------|
| **Followin MCP** | 热门话题、热门快讯、频道内容 |
| **Premium MCP** | Twitter 数据、加密价格、美股、宏观、新闻 |

需要在 Claude Code 中配置这两个 MCP Server。

---

## 初始化指南

clone 后需要初始化以下文件，填入你的账号信息：

| 步骤 | 文件 | 说明 |
|------|------|------|
| 1 | `skills/twitter-ops/references/voice-guide.md` | 定义你的人设和语气风格 |
| 2 | `skills/twitter-ops/references/operations-plan.md` | 定义运营目标和发布节奏 |
| 3 | `skills/competitor-watch/references/competitor-list.md` | 添加竞对账号 |
| 4 | `skills/engagement-manager/references/kol-targets.md` | 添加 KOL 互动目标 |

以下文件可以通过 Claude 自动生成（推荐）：

| 文件 | 生成方式 |
|------|---------|
| `audience-profile.md` | 说 "帮我分析账号数据" 或提供 Twitter Analytics CSV |
| `vault.md` | 说 "帮我建立素材库"，Claude 会扫描历史推文 |
| `patterns.md` | 与 vault.md 同时生成 |
| `kol-targets.md` | 说 "帮我分析历史互动对象"，可自动从数据提取 |

---

## 快速开始

### 跑一轮完整流水线

| 你说的话 | 效果 |
|---------|------|
| "跑一轮" / "自动跑" | 自动模式 — 全程自动决策，直接输出终稿 |
| "手动跑一轮" | 手动模式 — 每个检查点暂停，等你确认 |

### 两种模式

**自动模式**：热点采集 → 自动选 Top 3 → 自动匹配角度 → 出稿 → 终稿展示

**手动模式**：热点采集 → ⏸️ 你挑话题 → ⏸️ 你选角度 → ⏸️ 你审草稿 → 终稿

两种模式可随时切换——自动模式下发送任何消息，就会暂停变成手动。

### 单独使用某个功能

| 你说的话 | 调用的 Skill | 干什么 |
|---------|-------------|--------|
| "扫一下热点" | trend-scout | 只看当前有什么热点 |
| "今天发什么" | trend-scout → topic-engine | 热点采集 + 选题排序 |
| "帮我写推文：[主题]" | tweet-composer | 直接写一条推文 |
| "突发：[事件]" | 突发快速通道 | 全速出稿，争分夺秒 |
| "写篇深度文章：[主题]" | deep-write | 长文写作（1000-5000字） |
| "把这篇拆成Thread" | thread-builder | 长文 → Twitter 线程 |
| "帮我评论这条：[链接]" | hot-comment | 生成高质量评论 |
| "看看我评论区" | comment-ops | 评论区分级管理+回复 |
| "互动规划" | engagement-manager | 今日互动策略 |
| "竞对在发什么" | competitor-watch | 竞对账号监控 |
| "这周数据怎么样" | performance-review | 数据复盘 |
| "找灵感" | content-vault | 从爆款素材库找灵感 |

---

## 系统架构

```
                    ┌─────────────────────────────────────────┐
                    │         twitter-ops（主调度器）            │
                    │     模式控制 + 检查点 + 流程串联            │
                    └──────────────┬──────────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
  ┌─────▼─────┐            ┌──────▼──────┐           ┌───────▼───────┐
  │ 内容生产    │            │ 互动管理     │           │ 复盘优化      │
  │ Pipeline   │            │ Pipeline    │           │ Pipeline     │
  └─────┬─────┘            └──────┬──────┘           └───────┬───────┘
        │                         │                          │
   trend-scout              engagement-manager          performance-review
        ↓                    ├── hot-comment             competitor-watch
   topic-engine              └── comment-ops             content-vault
        ↓
   tweet-composer

                    ┌─────────────────────────────────────────┐
                    │         独立调用（手动触发）                │
                    │   deep-write  ·  thread-builder         │
                    └─────────────────────────────────────────┘
```

---

## 12 个 Skill 详解

### 主调度器

| Skill | 位置 | 作用 |
|-------|------|------|
| **twitter-ops** | `skills/twitter-ops/` | 串联所有子 Skill，管理模式和检查点 |

### 内容生产流水线

| Skill | 位置 | 作用 | 触发词 |
|-------|------|------|--------|
| **trend-scout** | `skills/trend-scout/` | 调用 MCP 采集市场热点 | "扫一下热点" |
| **topic-engine** | `skills/topic-engine/` | 热点→选题方案，P0-P3排序 | "今天发什么" |
| **tweet-composer** | `skills/tweet-composer/` | 写出发布级推文 | "帮我写推文" |

### 独立调用

| Skill | 位置 | 作用 | 触发词 |
|-------|------|------|--------|
| **deep-write** | `skills/deep-write/` | 1000-5000字深度文章 | "写篇深度文章" |
| **thread-builder** | `skills/thread-builder/` | 长文→Thread拆解 | "拆成Thread" |

### 互动管理流水线

| Skill | 位置 | 作用 | 触发词 |
|-------|------|------|--------|
| **engagement-manager** | `skills/engagement-manager/` | 互动战略规划 | "互动规划" |
| **hot-comment** | `skills/hot-comment/` | 主动去KOL帖子下评论 | "帮我评论这条" |
| **comment-ops** | `skills/comment-ops/` | 管理自己推文评论区 | "看看我评论区" |

### 复盘优化流水线

| Skill | 位置 | 作用 | 触发词 |
|-------|------|------|--------|
| **competitor-watch** | `skills/competitor-watch/` | 竞对账号监控 | "竞对在发什么" |
| **performance-review** | `skills/performance-review/` | 数据复盘+优化建议 | "这周数据怎么样" |
| **content-vault** | `skills/content-vault/` | 爆款素材库管理 | "找灵感" |

---

## 文件结构

```
twitter-ops-workflow/
├── ARCHITECTURE.md          ← 系统架构
├── README.md                ← 本文件
└── skills/
    ├── twitter-ops/         ← 主调度器
    │   ├── SKILL.md
    │   └── references/
    │       ├── voice-guide.md         ← 人设语气（⚠️ 需初始化）
    │       ├── content-calendar.md    ← 内容日历
    │       └── operations-plan.md     ← 运营方案（⚠️ 需初始化）
    ├── trend-scout/
    ├── topic-engine/
    ├── tweet-composer/
    ├── deep-write/
    ├── thread-builder/
    ├── engagement-manager/
    │   └── references/
    │       └── kol-targets.md         ← KOL列表（⚠️ 需初始化）
    ├── hot-comment/
    ├── comment-ops/
    ├── competitor-watch/
    │   └── references/
    │       └── competitor-list.md     ← 竞对列表（⚠️ 需初始化）
    ├── performance-review/
    │   └── references/
    │       └── audience-profile.md    ← 受众画像（可自动生成）
    └── content-vault/
        └── references/
            ├── vault.md               ← 素材库（可自动生成）
            └── patterns.md            ← 成功模式（可自动生成）
```

---

## 注意事项

1. **发布需人工确认** — 所有模式最终都输出终稿等待人工发布
2. **deep-write 和 thread-builder 不在自动流水线中** — 需手动触发
3. **突发事件优先** — "突发：[事件]" 会跳过常规流程全速出稿
4. **数据量大的 MCP 工具走 Agent 子进程** — trend-scout 内已有规则
5. **voice-guide 是核心** — 所有推文产出都基于人设语气指南
