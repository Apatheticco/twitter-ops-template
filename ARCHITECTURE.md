# Twitter Ops Workflow — System Architecture

> An AI-native daily operations system for crypto/macro Twitter accounts.
> Orchestrates 11 specialized Skills across 3 pipelines, powered by real-time MCP data tools.

---

## Overview

This system automates the full daily workflow of a crypto/macro Twitter account — from market intelligence gathering to published tweets. It is built as a network of composable Skills, each owning a single responsibility, coordinated by a master orchestrator.

**Two operating modes:**

| Mode | Trigger | Behavior |
|------|---------|----------|
| 🤖 Auto | "run workflow" | Full pipeline executes autonomously, decisions made by preset rules |
| 🔧 Manual | "run manual" | Pauses at every checkpoint, waits for human review before proceeding |

**Core principle: default to auto, intercept at any time.** Any user message during execution triggers a manual checkpoint at the current stage.

---

## System Map

```
                    ┌──────────────────────────────────────┐
                    │         twitter-ops  (Orchestrator)  │
                    │   Mode control · Checkpoints · Routing│
                    └──────────────┬───────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
  ┌─────▼──────┐           ┌───────▼──────┐          ┌───────▼───────┐
  │  CONTENT   │           │  ENGAGEMENT  │          │    REVIEW     │
  │  Pipeline  │           │  Pipeline    │          │   Pipeline    │
  └─────┬──────┘           └───────┬──────┘          └───────┬───────┘
        │                          │                         │
   trend-scout              engagement-manager         performance-review
        ↓                     ├── hot-comment           competitor-watch
   topic-engine               └── comment-ops           content-vault
        ↓
   tweet-composer

                    ┌──────────────────────────────────────┐
                    │       Standalone (user-triggered)    │
                    │  deep-write · thread-builder         │
                    └──────────────────────────────────────┘
```

---

## The 11 Skills

### Content Pipeline

| Skill | Role |
|-------|------|
| **trend-scout** | Real-time market intelligence — pulls CT trends, on-chain signals, whale moves, TG channel feeds, and macro data across 7 parallel data streams |
| **topic-engine** | Converts raw intelligence into scored, actionable tweet angles using 11 angle templates; enforces a hard 48h time filter before any topic enters selection |
| **tweet-composer** | Writes publication-ready tweets in 3 formats (single / thread / quote); enforces price data integrity rules at every stage |

### Engagement Pipeline

| Skill | Role |
|-------|------|
| **engagement-manager** | Plans daily outbound targets and inbound review strategy |
| **hot-comment** | Executes outbound commenting on high-value posts |
| **comment-ops** | Triages and drafts replies for inbound comment threads |

### Review Pipeline

| Skill | Role |
|-------|------|
| **performance-review** | Analyzes weekly metrics and generates optimization recommendations |
| **competitor-watch** | Monitors competitor accounts and surfaces differentiation opportunities |
| **content-vault** | Stores top-performing tweets as reusable templates and inspiration |

### Standalone

| Skill | Role |
|-------|------|
| **deep-write** | Long-form content (1,000–5,000 words) for articles and newsletters |
| **thread-builder** | Breaks long-form content into optimized Twitter threads |

---

## Content Pipeline — Detail

The main content pipeline runs in 4 stages with 3 human checkpoints:

```
[trend-scout] → ①  →  [topic-engine] → ②  →  [price refresh] → [tweet-composer] → ③  →  [final output]
```

### Stage 1 — Intelligence Gathering (trend-scout)

Runs 7 data streams in parallel via MCP tools:

| Stream | Tool | What it captures |
|--------|------|-----------------|
| CT trending topics | `open_trending_topic_ranks` | Top crypto discussions |
| Breaking news feed | `open_feed_list_trending` | Hot news + hot content |
| On-chain signals | `open_channel_feeds` | Fund rates, volume spikes, token unlocks, listings |
| Real-time prices | `crypto_realtime_price_batch` | Live prices for 10+ assets |
| Whale activity | `whale_trader_feeds` | Large wallet movements |
| Top trader positions | `top_traders_live_24h` | Live positions of pro traders |
| TG channel feeds | `tg_kol_feeds` × 4 categories | Macro / trading signals / narrative / on-chain |

Output is a structured briefing with **mandatory two-zone separation**:
- 📊 **Realtime Data Zone** — only hard API numbers (prices, rates, volumes)
- 📰 **Narrative Zone** — news, KOL opinions, event descriptions (marked as historical)

**Supplementary scan** (triggered when topics are scarce):
When the pre-filter leaves fewer than 2 usable topics, trend-scout auto-triggers a broader scan using `twitter_advanced_search` and `search_finance_news` to find additional angles from mainstream financial media and macro events.

**Checkpoint ①** — topic filtering (auto: top 3 by signal strength / manual: user selects)

### Stage 2 — Topic Selection (topic-engine)

**Pre-filter (runs before anything else):**

| Age | Action |
|-----|--------|
| ≤ 24h | ✅ Enters selection normally |
| 24h – 48h | ⚠️ Downgraded — kept only with ≥2 verifiable data points |
| > 48h | ❌ Hard excluded — no angle generation, no scoring |

Topics are ranked by a weighted formula:

```
Topic value = Timeliness(40%) × Data support(30%) × Controversy(20%) × Buzz(10%)
```

Each surviving topic gets **3 angles** matched from 11 templates:

| # | Template | Best for |
|---|----------|---------|
| 1 | Contrarian | When everyone agrees on a direction |
| 2 | Data Narrative | New data releases, on-chain anomalies |
| 3 | Hidden Risk | Risks buried inside bullish headlines |
| 4 | Historical Parallel | Market cycle echoes |
| 5 | Sarcasm & Roast | Contradictory behavior, industry jokes |
| 6 | Novel Framework | Turning points, emerging phenomena |
| 7 | Breaking React | Major event just happened (<4h) |
| 8 | Educational Thread | Complex concepts, common misconceptions |
| 9 | Comparative | Competing chains, tool comparisons |
| 10 | Trading Insight | On-chain structure changes |
| 11 | Macro Big Picture | Central bank policy, rates, FX |

**Checkpoint ②** — angle and format confirmation (auto: P0+P1 / manual: user picks)

### Stage 3 — Content Writing (tweet-composer)

Three output formats:

| Format | Constraint | Best for |
|--------|-----------|---------|
| Single tweet | ≤140 CJK characters | Breaking news, sharp takes |
| Thread (3/5/7) | ≤140 chars/tweet, [1/N] labeled | Data-heavy analysis |
| Quote tweet | ≤80 CJK characters | Reacting to a specific post |

**Checkpoint ③** — draft review with quality checklist

### Stage 4 — Final Output

All modes pause here. Publishing always requires human confirmation.

---

## Design Principles

### 1. Price Data Integrity
All prices in published content must come from a single authoritative source: `crypto_realtime_price_batch`. No exceptions.

- News headlines contain **historical prices** — never used as current data
- A mandatory **price refresh** runs immediately before writing begins (prices move between collection and writing)
- A **price verification check** is part of the pre-publish quality checklist

### 2. Signal Cross-Verification
The system identifies high-value content angles by cross-referencing multiple data streams:

| Signal Type | How identified | Value |
|------------|---------------|-------|
| Multi-source resonance | Same event in ≥2 independent streams | ★★★★★ |
| Data-narrative divergence | On-chain data contradicts market sentiment | ★★★★★ |
| KOL-whale disagreement | KOLs bullish while whales are selling (or vice versa) | ★★★★★ |
| TG-Twitter gap | TG community discussed it before Twitter picked it up | ★★★★★ |
| Early window | Event <6h old with low Twitter discussion volume | ★★★★ |

### 3. Time-Based Hard Filter
Stale content is excluded before any processing begins — not just deprioritized. The 48-hour cutoff prevents the system from generating angles around outdated events. If fewer than 2 topics survive the filter, the system auto-triggers trend-scout's supplementary scan rather than falling back to stale content.

### 4. Persona Consistency
Every piece of content is checked against a data-calibrated voice guide (derived from analysis of 647 published tweets):
- Strong opinions, no hedging
- Data-first: numbers before narrative
- Contrarian risk always included
- No price predictions, no investment advice
- Crypto-native formatting: `$BTC` not `#BTC`, CT slang where appropriate

---

## Data Sources (MCP Tools)

| Category | Tools |
|----------|-------|
| **Followin MCP** | `open_trending_topic_ranks` · `open_feed_list_trending` · `open_channel_feeds` · `open_search_feed` · `open_feed_list_tg_daily` · `open_feed_list_tag_opinions` |
| **Premium MCP — Crypto** | `crypto_realtime_price_batch` · `whale_trader_feeds` · `top_traders_live_24h` · `kol_call_orders_24h` · `tg_kol_feeds` · `twitter_advanced_search` · `twitter_trends` |
| **Premium MCP — Macro** | `finance_tool_treasury_rates` · `finance_tool_economic_calendar` · `search_finance_news` · `fred_get_series` |

---

## Quick Command Reference

| Command | Skills invoked |
|---------|----------------|
| `"run workflow"` | Full content pipeline |
| `"scan trends"` | trend-scout only |
| `"what to post today"` | trend-scout → topic-engine |
| `"write tweet: [topic]"` | tweet-composer directly |
| `"breaking: [event]"` | trend-scout → topic-engine → tweet-composer (speed mode) |
| `"write deep dive: [topic]"` | deep-write |
| `"turn this into a thread"` | thread-builder |
| `"engagement plan"` | engagement-manager |
| `"what are competitors posting"` | competitor-watch |
| `"weekly review"` | performance-review |

---

## Portability

The system is designed to run on any agent platform that supports MCP tool connections. Each Skill exports as a standalone **Agent System Prompt** (core logic self-contained) paired with optional **Knowledge Base documents** for long-form references:

| Agent Prompt | Knowledge Base |
|--------------|---------------|
| `twitter-ops` master | voice-guide · operations-plan |
| `trend-scout` | *(tool-only, no KB needed)* |
| `topic-engine` | angle-templates |
| `tweet-composer` | voice-guide · tweet-styles |
