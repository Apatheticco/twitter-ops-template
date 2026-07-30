#!/usr/bin/env python3
"""
推文数据分析脚本
用于批量处理推文数据，筛选高表现推文，计算互动率。

支持的输入格式：
1. Twitter API v2 JSON 导出
2. Twitter 官方数据归档 (tweets.js)
3. CSV 格式 (手动整理)

用法：
    python tweet_analyzer.py --input tweets.json --format api
    python tweet_analyzer.py --input tweets.js --format archive
    python tweet_analyzer.py --input tweets.csv --format csv
"""

import json
import csv
import sys
import argparse
from datetime import datetime
from pathlib import Path


def load_api_json(filepath):
    """加载 Twitter API v2 格式的 JSON"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    tweets = []
    items = data.get('data', data) if isinstance(data, dict) else data

    for item in items:
        metrics = item.get('public_metrics', {})
        tweets.append({
            'id': item.get('id', ''),
            'text': item.get('text', ''),
            'created_at': item.get('created_at', ''),
            'likes': metrics.get('like_count', 0),
            'retweets': metrics.get('retweet_count', 0),
            'replies': metrics.get('reply_count', 0),
            'quotes': metrics.get('quote_count', 0),
            'impressions': metrics.get('impression_count', 0),  # 默认 0 —— 默认 1 会算出 16200% 并标成互动率
        })
    return tweets


def load_archive_js(filepath):
    """加载 Twitter 官方数据归档格式 (tweets.js)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # tweets.js 格式: window.YTD.tweets.part0 = [...]
    json_start = content.index('[')
    data = json.loads(content[json_start:])

    tweets = []
    for item in data:
        tweet = item.get('tweet', item)
        tweets.append({
            'id': tweet.get('id', ''),
            'text': tweet.get('full_text', tweet.get('text', '')),
            'created_at': tweet.get('created_at', ''),
            'likes': int(tweet.get('favorite_count', 0)),
            'retweets': int(tweet.get('retweet_count', 0)),
            'replies': 0,  # 归档格式不含评论数
            'quotes': 0,
            'impressions': 0,  # 归档格式不含印象数
        })
    return tweets


def load_csv(filepath):
    """加载 CSV 格式"""
    tweets = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tweets.append({
                'id': row.get('id', ''),
                'text': row.get('text', row.get('content', '')),
                'created_at': row.get('created_at', row.get('date', '')),
                'likes': int(row.get('likes', row.get('like_count', 0))),
                'retweets': int(row.get('retweets', row.get('retweet_count', 0))),
                'replies': int(row.get('replies', row.get('reply_count', 0))),
                'quotes': int(row.get('quotes', row.get('quote_count', 0))),
                'impressions': int(row.get('impressions', row.get('impression_count', 0))),
            })
    return tweets


def drop_retweets(tweets):
    """剔除纯转推。

    转推的 text 以 'RT @' 开头（官方归档的 full_text 同样如此）。
    这一步必须在打分之前做，且必须对所有输入格式统一生效——
    转推的互动数是别人的，混进来会霸占 S 级榜首，进而被写进素材库当成
    "你自己的可复用爆款句式"，再喂给写作环节。
    """
    def is_rt(text):
        s = text.lstrip()
        # 'RT @user:' 是标准形态；'RT@user:' 少数客户端会产出，同样是转推
        return s.startswith('RT @') or s.startswith('RT@')

    kept = [t for t in tweets if not is_rt(t.get('text', ''))]
    return kept, len(tweets) - len(kept)


def calculate_engagement(tweet):
    """计算互动率（%）或——没有印象数时——绝对互动数。

    返回 (值, 是否为百分比)。调用方必须据此决定单位，
    否则会把绝对互动数打印成 "12.00%"。
    """
    total_engagement = tweet['likes'] + tweet['retweets'] + tweet['replies'] + tweet['quotes']

    if tweet['impressions'] > 0:
        return total_engagement / tweet['impressions'] * 100, True
    else:
        # 没有印象数（官方归档格式就是这样）时，退化为绝对互动数排序
        return total_engagement, False


def analyze_tweets(tweets):
    """分析推文，按互动率排序，分级"""
    # 计算互动率
    for tweet in tweets:
        tweet['engagement_total'] = tweet['likes'] + tweet['retweets'] + tweet['replies'] + tweet['quotes']
        tweet['engagement_rate'], tweet['rate_is_pct'] = calculate_engagement(tweet)

    # 🔴 混合输入不许跨单位排序：只要有一条缺 impressions，整批降级为绝对互动数。
    # 否则 1620（绝对数）会和 6.60（百分比）在同一个列表里比大小，
    # S 级完全由"哪条缺 impressions"决定，与表现无关。
    if tweets and not all(t['rate_is_pct'] for t in tweets):
        for tweet in tweets:
            tweet['engagement_rate'] = tweet['engagement_total']
            tweet['rate_is_pct'] = False

    # 按互动率排序
    tweets.sort(key=lambda x: x['engagement_rate'], reverse=True)

    # 计算百分位
    total = len(tweets)
    if total == 0:
        return tweets

    avg_rate = sum(t['engagement_rate'] for t in tweets) / total
    top_10_threshold = tweets[max(0, int(total * 0.1) - 1)]['engagement_rate'] if total >= 10 else 0
    top_25_threshold = tweets[max(0, int(total * 0.25) - 1)]['engagement_rate'] if total >= 4 else 0

    for i, tweet in enumerate(tweets):
        percentile = (1 - i / total) * 100
        if percentile >= 90:
            tweet['grade'] = 'S'
        elif percentile >= 75:
            tweet['grade'] = 'A'
        elif tweet['engagement_rate'] >= avg_rate * 1.5:
            tweet['grade'] = 'B+'
        else:
            tweet['grade'] = '-'

    return tweets


def output_report(tweets, output_path=None, rt_dropped=0):
    """输出分析报告"""
    total = len(tweets)
    if total == 0:
        print("没有推文数据。")
        return

    # 单位不能猜：没有印象数的输入（官方归档）算出来的是绝对互动数，不是百分比
    is_pct = all(t.get('rate_is_pct') for t in tweets)
    unit = '%' if is_pct else ''
    metric_name = '互动率' if is_pct else '绝对互动数'

    avg_rate = sum(t['engagement_rate'] for t in tweets) / total
    s_tier = [t for t in tweets if t['grade'] == 'S']
    a_tier = [t for t in tweets if t['grade'] == 'A']

    report = []
    report.append(f"# 推文分析报告")
    report.append(f"")
    report.append(f"**分析时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"**总推文数**：{total}（已剔除转推 {rt_dropped} 条）")
    report.append(f"**平均{metric_name}**：{avg_rate:.2f}{unit}")
    report.append(f"**S级推文**：{len(s_tier)} 条（Top 10%）")
    report.append(f"**A级推文**：{len(a_tier)} 条（Top 25%）")
    if not is_pct:
        report.append(f"")
        report.append(f"> 🔴 **本次排序口径是绝对互动数，不是互动率。**"
                      f"输入数据没有印象数（impressions），无法算百分比。"
                      f"绝对值排序会系统性偏向粉丝量增长后的近期推文——"
                      f"跨期对比无效，只能用来在同一批数据内部挑相对好的。")
    report.append(f"")

    report.append(f"## 🏆 S级推文（必须入库）")
    report.append(f"")
    for t in s_tier[:20]:  # 最多展示20条
        text_preview = t['text'][:80].replace('\n', ' ')
        report.append(f"### [{t['grade']}] {metric_name} {t['engagement_rate']:.2f}{unit}")
        report.append(f"**内容**：{text_preview}...")
        report.append(f"**数据**：❤️ {t['likes']} | 🔄 {t['retweets']} | 💬 {t['replies']} | 📊 总互动 {t['engagement_total']}")
        report.append(f"**发布时间**：{t['created_at']}")
        report.append(f"")

    report.append(f"## ⭐ A级推文")
    report.append(f"")
    for t in a_tier[:20]:
        text_preview = t['text'][:80].replace('\n', ' ')
        report.append(f"- **[{t['grade']}] {t['engagement_rate']:.2f}{unit}** — {text_preview}...")

    report_text = '\n'.join(report)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"报告已保存到：{output_path}")
    else:
        print(report_text)

    # 同时输出 JSON 格式（供素材库使用）
    vault_entries = [t for t in tweets if t['grade'] in ('S', 'A')]
    json_path = output_path.replace('.md', '.json') if output_path else None
    if json_path:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(vault_entries, f, ensure_ascii=False, indent=2)
        print(f"JSON 数据已保存到：{json_path}")


def main():
    parser = argparse.ArgumentParser(description='推文数据分析工具')
    parser.add_argument('--input', '-i', required=True, help='输入文件路径')
    parser.add_argument('--format', '-f', choices=['api', 'archive', 'csv'], default='api', help='输入文件格式')
    parser.add_argument('--output', '-o', help='输出报告路径（.md）')

    args = parser.parse_args()

    loaders = {
        'api': load_api_json,
        'archive': load_archive_js,
        'csv': load_csv,
    }

    print(f"加载数据：{args.input}（格式：{args.format}）")
    tweets = loaders[args.format](args.input)
    print(f"加载了 {len(tweets)} 条推文")

    # 统一在这里剔转推——放在 loader 里就要写三遍，漏一个格式就前功尽弃
    tweets, rt_dropped = drop_retweets(tweets)
    print(f"剔除转推 {rt_dropped} 条，进入打分 {len(tweets)} 条")

    tweets = analyze_tweets(tweets)
    output_report(tweets, args.output, rt_dropped=rt_dropped)


if __name__ == '__main__':
    main()
