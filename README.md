# Twitter Ops Workflow — 使用说明

> 一套基于 Claude Code 的 Twitter 日运营 AI Agent 工作流
> 适用账号：@followin_io_zh（加密+宏观全市场资讯）
> 最后更新：2026-04-13

---

## 这是什么

一个 **1 个主调度器 + 11 个子 Skill** 的 Twitter 运营系统。覆盖从热点采集、选题、撰写、互动、竞对监控到数据复盘的完整运营闭环。

所有 Skill 以 Markdown 文件（`SKILL.md`）形式存在，Claude Code 会读取这些文件作为行为指导，按流水线逻辑串联执行。

---

## 快速开始

### 1. 跑一轮完整流水线

在 Claude Code 中直接说：

| 你说的话 | 效果 |
|---------|------|
| "跑一轮" / "自动跑" | 自动模式 — 全程自动决策，直接输出终稿 |
| "手动跑一轮" | 手动模式 — 每个检查点暂停，等你确认 |

### 2. 两种模式的区别

**自动模式**：热点采集 → 自动选 Top 3 → 自动匹配角度 → 出稿 → 终稿展示

**手动模式**：热点采集 → ⏸️ 你挑话题 → ⏸️ 你选角度 → ⏸️ 你审草稿 → 终稿

两种模式可随时切换——自动模式下你发送任何消息，就会暂停变成手动。

### 3. 单独使用某个功能

| 你说的话 | 调用的 Skill | 干什么 |
|---------|-------------|--------|
| "扫一下热点" | trend-scout | 只看当前市场有什么热点 |
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

### 三条流水线

| 流水线 | 功能 | 触发频率 |
|--------|------|---------|
| **内容生产** | 热点 → 选题 → 撰写 → 终稿 | 每日多次 |
| **互动管理** | KOL互动规划 → 主动评论 + 被动回复 | 每日 |
| **复盘优化** | 数据分析 → 素材归档 → 策略反馈 | 每周 |

---

## 12 个 Skill 详解

### 主调度器

#### twitter-ops — 主控中心
- **位置**：`skills/twitter-ops/SKILL.md`
- **作用**：串联所有子 Skill，管理自动/手动模式和三个检查点
- **参考文件**：
  - `references/voice-guide.md` — 人设 & 语气指南（基于647条推文数据校准）
  - `references/content-calendar.md` — 内容日历和排期
  - `references/operations-plan.md` — 完整运营方案

---

### 内容生产流水线

#### 1. trend-scout — 热点采集
- **位置**：`skills/trend-scout/SKILL.md`
- **作用**：调用 MCP 工具（Followin、Premium MCP 等）采集加密+宏观市场热点
- **四种模式**：Quick（快速扫描）、Full（三轮深度）、Breaking（突发定向）、Deep（专题研究）
- **输出**：结构化热点简报（CT热点 + 链上异动 + 价格快照 + 宏观信号）
- **触发词**："扫一下热点"、"热点"、"市场动态"

#### 2. topic-engine — 选题排序
- **位置**：`skills/topic-engine/SKILL.md`
- **作用**：将热点转化为可执行的选题方案，排序优先级（P0-P3），生成角度
- **输入**：trend-scout 的热点简报 或 用户直接指定话题
- **输出**：每个话题的角度方案 + 推荐格式（单推/Thread/引用推）
- **触发词**："今天发什么"、"选题"、"角度"

#### 3. tweet-composer — 推文撰写
- **位置**：`skills/tweet-composer/SKILL.md`
- **作用**：根据选题角度写出发布级推文
- **支持格式**：单推、Thread、引用推文
- **自带质检**：观点加载、开头吸引力、情绪温度、互动钩子、voice-guide合规
- **触发词**："帮我写推文"、"写个帖子"

---

### 独立调用

#### 4. deep-write — 深度长文
- **位置**：`skills/deep-write/SKILL.md`
- **作用**：写 1000-5000 字深度文章，内置 20+ 风格模板
- **支持格式**：Substack、Mirror、公众号、Twitter Articles
- **注意**：不在自动流水线中，需手动触发
- **触发词**："写篇深度文章：[主题]"

#### 5. thread-builder — Thread 拆解
- **位置**：`skills/thread-builder/SKILL.md`
- **作用**：将已有长文（研报、文章、白皮书）拆解为 Twitter Thread
- **与 tweet-composer 的区别**：thread-builder 转化已有内容，tweet-composer 从零创作
- **触发词**："把这篇拆成Thread"

---

### 互动管理流水线

#### 6. engagement-manager — 互动战略
- **位置**：`skills/engagement-manager/SKILL.md`
- **作用**：规划每日互动目标，协调 hot-comment 和 comment-ops
- **参考文件**：`references/kol-targets.md` — 三层 KOL 互动目标清单（28个账号）
- **触发词**："互动规划"、"今天互动什么"

#### 7. hot-comment — 主动评论
- **位置**：`skills/hot-comment/SKILL.md`
- **作用**：在 KOL 热推下发有质量的评论，引流到自己账号
- **核心原则**：速度+内容增量，不发"👍"式无效评论
- **触发词**："帮我评论这条"、"热评"

#### 8. comment-ops — 评论区运营
- **位置**：`skills/comment-ops/SKILL.md`
- **作用**：管理自己推文下的评论区，五级分类+策略回复
- **分类**：高价值提问 → 认真回复 | 争议 → 数据回应 | 垃圾 → 忽略
- **触发词**："看看我评论区"、"回复评论"

---

### 复盘优化流水线

#### 9. competitor-watch — 竞对监控
- **位置**：`skills/competitor-watch/SKILL.md`
- **作用**：监控竞对账号的内容策略、互动数据、话题方向
- **参考文件**：`references/competitor-list.md` — 5个直接竞对 + 学习对象
- **触发词**："竞对在发什么"、"同行分析"

#### 10. performance-review — 数据复盘
- **位置**：`skills/performance-review/SKILL.md`
- **作用**：分析账号互动率、涨粉效率、内容效果，输出优化建议
- **参考文件**：`references/audience-profile.md` — 完整受众画像+账号诊断
- **触发词**："这周数据怎么样"、"数据复盘"

#### 11. content-vault — 素材库
- **位置**：`skills/content-vault/SKILL.md`
- **作用**：管理历史爆款推文素材库，提供灵感和可复用模板
- **参考文件**：
  - `references/vault.md` — 59条 S/A 级爆款推文
  - `references/patterns.md` — 6个数据验证的成功模式
- **触发词**："找灵感"、"素材库"、"更新素材库"

---

## 参考数据文件

所有 Skill 共享的数据基础：

| 文件 | 位置 | 内容 |
|------|------|------|
| voice-guide.md | twitter-ops/references/ | 人设语气指南，基于647条推文数据校准 |
| operations-plan.md | twitter-ops/references/ | 运营方案：定位、节奏、配比、增长策略 |
| content-calendar.md | twitter-ops/references/ | 每日/每周内容排期 |
| audience-profile.md | performance-review/references/ | 受众画像：人口统计+增长趋势+活跃时间 |
| vault.md | content-vault/references/ | 59条爆款推文（23条S级 + 36条A级） |
| patterns.md | content-vault/references/ | 6个成功模式（附ER数据和模板） |
| kol-targets.md | engagement-manager/references/ | 28个KOL互动目标（3层） |
| competitor-list.md | competitor-watch/references/ | 5个直接竞对分析 |

---

## 运营节奏速查

### 每天

| 时间 (UTC+8) | 动作 | 说明 |
|-------------|------|------|
| 09:00 | 跑一轮（自动） | 生成早报 + 第一条热点帖 |
| 10:00-14:00 | 有热点就发 | BREAKING / 锐评 |
| 19:00-21:00 | 发当日最强帖 | 黄金时段 |
| 随时 | 突发快速通道 | "突发：[事件]" |

### 每周

| 时间 | 动作 |
|------|------|
| 周二/周四 | 重点发布日（ER 最高），安排最强内容 |
| 周五 | performance-review 周度复盘 |
| 周末 | 至少各 1 条保持存在感 |

### 每月

| 动作 | 说明 |
|------|------|
| 内容配比检查 | 锐评是否达到 25%？日报是否控制在 20%？ |
| KOL 升级评估 | Tier 2 → Tier 1 |
| 竞对分析 | competitor-watch 月度报告 |
| 素材入库 | 高表现推文归档到 content-vault |

---

## 技术依赖

### MCP 工具（数据源）

| MCP Server | 用途 | 主要调用 Skill |
|------------|------|---------------|
| Followin MCP | 热门话题、热门快讯、频道内容 | trend-scout |
| Premium MCP | Twitter 数据、加密价格、美股、宏观、新闻 | trend-scout, performance-review |

### 文件结构

```
twitter-ops-workflow/
├── ARCHITECTURE.md          ← 系统架构文档
├── README.md                ← 本文件（使用说明）
└── skills/
    ├── twitter-ops/         ← 主调度器
    │   ├── SKILL.md
    │   └── references/
    │       ├── voice-guide.md
    │       ├── content-calendar.md
    │       └── operations-plan.md
    ├── trend-scout/         ← 热点采集
    ├── topic-engine/        ← 选题排序
    ├── tweet-composer/      ← 推文撰写
    ├── deep-write/          ← 深度长文
    ├── thread-builder/      ← Thread拆解
    ├── engagement-manager/  ← 互动战略
    │   └── references/
    │       └── kol-targets.md
    ├── hot-comment/         ← 主动评论
    ├── comment-ops/         ← 评论区运营
    ├── competitor-watch/    ← 竞对监控
    │   └── references/
    │       └── competitor-list.md
    ├── performance-review/  ← 数据复盘
    │   └── references/
    │       └── audience-profile.md
    └── content-vault/       ← 素材库
        └── references/
            ├── vault.md
            └── patterns.md
```

---

## 注意事项

1. **发布需人工确认** — 所有模式最终都会输出终稿等待人工发布，Claude 不会自动发推
2. **deep-write 和 thread-builder 不在自动流水线中** — 需要手动触发
3. **突发事件优先** — 说"突发：[事件]"会跳过常规流程，全速出稿
4. **数据量大的 MCP 工具需走 Agent 子进程** — trend-scout 内已有规则，避免上下文溢出
5. **voice-guide 是核心** — 所有推文产出都必须符合人设语气指南，这是内容一致性的基础
