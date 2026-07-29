# 数据源 & RSS 列表

## 加密新闻

### 英文
| 来源 | URL | 更新频率 | 特点 |
|------|-----|---------|------|
| CoinDesk | coindesk.com | 实时 | 综合性最强 |
| The Block | theblock.co | 实时 | 机构视角、数据好 |
| Cointelegraph | cointelegraph.com | 实时 | 覆盖面广 |
| Decrypt | decrypt.co | 每日 | 叙事性强 |
| DL News | dlnews.com | 每日 | 深度报道 |

### 中文
| 来源 | URL | 更新频率 | 特点 |
|------|-----|---------|------|
| 金色财经 | jinse.cn | 实时 | 中文最快 |
| Odaily | odaily.news | 实时 | 项目分析深 |
| PANews | panewslab.com | 实时 | 综合覆盖 |
| BlockBeats | theblockbeats.info | 实时 | 快讯速度快 |
| 吴说 | wublock.com | 每日 | 独家消息多 |

## 宏观经济数据源

### 官方来源
| 来源 | 关注内容 | 频率 |
|------|---------|------|
| 美联储 (federalreserve.gov) | FOMC决议、会议纪要、点阵图 | 每6周/按需 |
| 美国劳工部 (bls.gov) | CPI、PPI、非农就业 | 月度 |
| 美国财政部 (treasury.gov) | 国债拍卖、TGA余额 | 每日/周度 |
| ECB (ecb.europa.eu) | 利率决议、经济展望 | 每6周 |
| 日本央行 (boj.or.jp) | 利率、YCC政策 | 按需 |

### 经济日历
| 工具 | URL | 用途 |
|------|-----|------|
| Investing.com 日历 | investing.com/economic-calendar | 每日关键数据发布时间 |
| ForexFactory | forexfactory.com/calendar | 外汇+宏观数据 |
| TradingEconomics | tradingeconomics.com | 全球宏观数据汇总 |

## 链上数据平台

### 综合数据
| 平台 | API | 用途 |
|------|-----|------|
| CoinGecko | api.coingecko.com | 价格、市值、交易量（免费） |
| DeFiLlama | api.llama.fi | TVL、协议数据、DEX交易量（免费） |
| Dune | dune.com/api | 自定义链上查询（有免费额度） |

### 鲸鱼 & 资金流
| 平台 | 用途 |
|------|------|
| Whale Alert | 大额转账实时追踪 |
| Lookonchain | 聪明钱地址追踪 |
| Arkham Intelligence | 实体标签+资金流向 |
| Nansen | 钱包标签+热钱追踪 |

### DeFi 专项
| 平台 | 用途 |
|------|------|
| DeBank | DeFi投资组合追踪 |
| Token Terminal | 协议收入和估值数据 |
| L2Beat | L2 TVL和安全性对比 |

### 交易所资金流
| 平台 | 用途 |
|------|------|
| CryptoQuant | 交易所流入/流出、矿工数据 |
| Glassnode | 链上指标（MVRV、SOPR等） |
| Coinalyze | 期货持仓、资金费率 |

## CT KOL 监控列表

> ⚠️ **本节是结构模板，不是推荐名单。** 下表按「你需要哪几类视角」分组，账号自己填。
> 别直接抄别人的关注列表——名单要匹配你的账号定位，否则扫回来的东西你既没观点也接不上话。

| 视角类别 | 你需要几个 | 选号标准 | 你的账号 |
|---|---|---|---|
| 宏观 × 加密 | 2–3 | 能把美联储/流动性和币价挂钩，不只喊单 | `@___` |
| 链上数据 | 2–3 | 自己跑数据、给图表，不是转述别人的 | `@___` |
| 交易观点 | 2–3 | 明确给方向和理由，且事后认账 | `@___` |
| 研究机构 | 1–2 | 出研报、有方法论 | `@___` |
| 中文圈 | 2–3 | 你的目标读者实际在看谁 | `@___` |

**选号三条**：
1. **粉丝量在你的 1.3–10 倍之间**——太小学不到东西，太大玩法不可复制
2. **发文频率适中**——高频全量搬运号会把你的扫描结果淹没
3. **零借鉴即移出**——连续几周没从他那儿拿到任何可用角度，就换掉

**辅助工具**：Twitter Lists 建私密列表分组关注；链上类可配合 Nansen Smart Money 等地址追踪工具。

## RSS 订阅建议

```
# 加密新闻 RSS
https://www.coindesk.com/arc/outboundfeeds/rss/
https://www.theblock.co/rss.xml
https://cointelegraph.com/rss
https://decrypt.co/feed

# 宏观
https://www.federalreserve.gov/feeds/press_all.xml

# 中文
https://www.odaily.news/rss
https://www.panewslab.com/rss
```

## API 调用示例

### CoinGecko — 24h涨跌幅Top币种
```
GET https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=price_change_percentage_24h_desc&per_page=10
```

### DeFiLlama — TVL变化排行
```
GET https://api.llama.fi/protocols
```

### Dune — 自定义查询
```
GET https://api.dune.com/api/v1/query/{query_id}/results
```

## 每日检查清单

### 快速扫描（5-10分钟）
- [ ] CoinGecko 24h 涨跌幅 Top 10
- [ ] DeFiLlama TVL 变化 Top 10
- [ ] Whale Alert 过去12h大额转账
- [ ] 今日经济数据日历
- [ ] CT 热门话题/趋势

### 深度挖掘（按需）
- [ ] Glassnode/CryptoQuant 链上指标变化
- [ ] 交易所资金费率和持仓量
- [ ] KOL 观点汇总（多空分歧）
- [ ] 项目重大更新/升级/解锁

### 信息质量检查
- [ ] 一手源还是二手源？
- [ ] 数据可验证吗？
- [ ] 是否有对立观点？
