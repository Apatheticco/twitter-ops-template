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

### 英文 KOL（必关注）
- @CryptoHayes — Arthur Hayes，宏观+加密视角
- @100trillionUSD — PlanB，BTC模型
- @DegenSpartan — 交易观点，犀利
- @coaboroern — Cobie，行业深度
- @nic__carter — Nic Carter，BTC基础设施
- @WClementeIII — Will Clemente，链上分析
- @MessariCrypto — Messari官方，研报

### 中文 KOL
- @Phyrex_Ni — 数据分析
- @0xCryptowizard — 链上数据
- @Anbessa100 — 宏观+加密

### KOL追踪工具
- Nansen Smart Money：追踪聪明钱地址
- Twitter Lists：创建私密列表分组关注

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
