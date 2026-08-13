---
name: novel-era-data
description: "Use when 查小说年代数据：历史汇率、历史天气、某年物价/事件/产品上市时间线。"
version: 1.0.0
author: anonymous
license: MIT
metadata:
  hermes:
    tags: [小说, 年代考据, 汇率, 天气, 历史数据]
    related_skills: [novel-foundation, historical-price-research]
---

# 小说年代数据查询（Novel Era Data）

为年代题材小说查证**真实的历史数据**：历史汇率、历史天气、某年事件/产品。数据源全部免费、无需 API key、零依赖（Python stdlib）。

## When to Use

- 小说写到「某年某月」需要真实的汇率、天气、物价、事件背景。
- 需要把「推演」升级为「verified」——用原始数据源，而不是凭印象。

## 数据源（全部免费、无 key、真实）

| 数据 | 源 | 覆盖 | 脚本 |
|---|---|---|---|
| 历史汇率 | Frankfurter（ECB 官方参考汇率） | 1999 至今，逐日 | scripts/exchange_rate.py |
| 历史天气 | Open-Meteo（ERA5 再分析） | 1940 至今，逐日/逐小时 | scripts/historical_weather.py |

## 用法

### 历史汇率（USD→CNY 等）

```bash
python scripts/exchange_rate.py 2013-01-15 USD CNY
# → 2013-01-15 USD → CNY: 6.2157
```

支持任意货币对（ECB 参考汇率覆盖约 30 种货币）。汇率是**央行参考中间价/官方汇率**，非黑市价。

### 历史天气（某地某时间段）

```bash
# 需要该地的经纬度（可用 maps skill 的 search 命令获取）
python scripts/historical_weather.py 22.25 111.69 2013-01-01 2013-01-07
# → 逐日最高温/最低温/降水
```

加 `--hourly` 出逐小时温度/降水（用于写「那天下午下雨」）。

## 注意事项

- 汇率是官方参考价，故事里黑市/换汇价需另外标注。
- 天气是 ERA5 再分析（网格插值），城市级真实度够用，极端局地天气可能有偏差。
- 这两个数据源解决「汇率」「天气」两个缺口；物价/车价/逐日价仍走 historical-price-research。
- 拿到的数据记进 06-时代细节库（带来源 + 查询日期），不要只留在对话里。
