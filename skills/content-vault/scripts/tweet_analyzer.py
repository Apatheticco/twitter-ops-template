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
            'impressions': metrics.get('impression_count', 1),
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


def calculate_engagement(tweet):
    """计算互动率"""
    total_engagement = tweet['likes'] + tweet['retweets'] + tweet['replies'] + tweet['quotes']

    if tweet['impressions'] > 0:
        return total_engagement / tweet['impressions'] * 100
    else:
        # 没有印象数时，用绝对互动数作为替代指标
        return total_engagement


def analyze_tweets(tweets):
    """分析推文，按互动率排序，分级"""
    # 计算互动率
    for tweet in tweets:
        tweet['engagement_total'] = tweet['likes'] + tweet['retweets'] + tweet['replies'] + tweet['quotes']
        tweet['engagement_rate'] = calculate_engagement(tweet)

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


def output_report(tweets, output_path=None):
    """输出分析报告"""
    total = len(tweets)
    if total == 0:
        print("没有推文数据。")
        return

    avg_rate = sum(t['engagement_rate'] for t in tweets) / total
    s_tier = [t for t in tweets if t['grade'] == 'S']
    a_tier = [t for t in tweets if t['grade'] == 'A']

    report = []
    report.append(f"# 推文分析报告")
    report.append(f"")
    report.append(f"**分析时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"**总推文数**：{total}")
    report.append(f"**平均互动率**：{avg_rate:.2f}%")
    report.append(f"**S级推文**：{len(s_tier)} 条（Top 10%）")
    report.append(f"**A级推文**：{len(a_tier)} 条（Top 25%）")
    report.append(f"")

    report.append(f"## 🏆 S级推文（必须入库）")
    report.append(f"")
    for t in s_tier[:20]:  # 最多展示20条
        text_preview = t['text'][:80].replace('\n', ' ')
        report.append(f"### [{t['grade']}] 互动率 {t['engagement_rate']:.2f}%")
        report.append(f"**内容**：{text_preview}...")
        report.append(f"**数据**：❤️ {t['likes']} | 🔄 {t['retweets']} | 💬 {t['replies']} | 📊 总互动 {t['engagement_total']}")
        report.append(f"**发布时间**：{t['created_at']}")
        report.append(f"")

    report.append(f"## ⭐ A级推文")
    report.append(f"")
    for t in a_tier[:20]:
        text_preview = t['text'][:80].replace('\n', ' ')
        report.append(f"- **[{t['grade']}] {t['engagement_rate']:.2f}%** — {text_preview}...")

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

    tweets = analyze_tweets(tweets)
    output_report(tweets, args.output)


if __name__ == '__main__':
    main()
