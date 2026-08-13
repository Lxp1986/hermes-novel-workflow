#!/usr/bin/env python3
"""历史汇率查询 — 数据源 Frankfurter（ECB 官方参考汇率，1999 至今，免费无 key）。

用法:
    python exchange_rate.py 2013-01-15 [USD] [CNY]

参数:
    日期   YYYY-MM-DD（必填）
    base   基准货币（默认 USD）
    symbols 目标货币（默认 CNY）

示例:
    python exchange_rate.py 2013-01-15 USD CNY
    # → 2013-01-15  USD → CNY: 6.2157

说明: 返回 ECB 官方参考汇率（央行参考中间价），非黑市/换汇价。
"""
import sys
import json
import urllib.request

API = "https://api.frankfurter.app"


def fetch(date, base="USD", symbols="CNY"):
    url = f"{API}/{date}?from={base}&to={symbols}"
    req = urllib.request.Request(url, headers={"User-Agent": "novel-era-data/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    date = sys.argv[1]
    base = sys.argv[2] if len(sys.argv) > 2 else "USD"
    symbols = sys.argv[3] if len(sys.argv) > 3 else "CNY"
    try:
        d = fetch(date, base, symbols)
        rate = d["rates"][symbols]
        print(f"{d['date']}  {base} → {symbols}: {rate}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"错误: {date} 无数据（ECB 参考汇率覆盖 1999 至今，节假日无报价）")
        else:
            print(f"HTTP 错误 {e.code}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
