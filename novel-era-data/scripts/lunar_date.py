#!/usr/bin/env python3
"""农历日期查询 — 公历↔农历转换 + 节气 + 节日 + 星期。

依赖：同目录下的 zhdate 包（纯 Python，已随脚本附带，无需 pip 安装）。

用法:
    python lunar_date.py 2013-01-01              # 查某公历日的农历/节气/节日/星期
    python lunar_date.py 2013-01-01 --range 40   # 查该日前后 40 天内的节日/节气（找最近的春节/清明等）
    python lunar_date.py lunar 2013 1 1          # 农历正月初一 → 公历

用途：小说时间逻辑验证——公历农历对得上、节日习俗不搞错（如「元旦说过年」「清明拜山」这类）。
"""
import sys, os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zhdate import ZhDate

# 24 节气（公历大致日期，精确到日足够小说用）
JIEQI = {
    1: [("小寒", 5), ("大寒", 20)], 2: [("立春", 4), ("雨水", 19)],
    3: [("惊蛰", 5), ("春分", 20)], 4: [("清明", 4), ("谷雨", 20)],
    5: [("立夏", 5), ("小满", 21)], 6: [("芒种", 5), ("夏至", 21)],
    7: [("小暑", 7), ("大暑", 22)], 8: [("立秋", 7), ("处暑", 23)],
    9: [("白露", 7), ("秋分", 23)], 10: [("寒露", 8), ("霜降", 23)],
    11: [("立冬", 7), ("小雪", 22)], 12: [("大雪", 7), ("冬至", 21)],
}

# 农历节日（农历月, 日）
LUNAR_FESTIVAL = {
    (1, 1): "春节(正月初一)", (1, 15): "元宵节", (2, 2): "龙抬头",
    (5, 5): "端午节", (7, 7): "七夕", (7, 15): "中元节",
    (8, 15): "中秋节", (9, 9): "重阳节", (12, 8): "腊八节",
    (12, 23): "小年(北方)", (12, 24): "小年(南方)", (12, 30): "除夕",
}

# 公历节日（月, 日）
SOLAR_FESTIVAL = {
    (1, 1): "元旦", (2, 14): "情人节", (3, 8): "妇女节",
    (5, 1): "劳动节", (6, 1): "儿童节", (10, 1): "国庆节", (12, 25): "圣诞节",
}

def jieqi_of(d):
    month, day = d.month, d.day
    for name, jd in JIEQI.get(month, []):
        if abs(day - jd) <= 1:
            return name
    return None

def festivals_of(d, lunar):
    fests = []
    key = (d.month, d.day)
    if key in SOLAR_FESTIVAL:
        fests.append(SOLAR_FESTIVAL[key])
    lkey = (lunar.lunar_month, lunar.lunar_day)
    if lkey in LUNAR_FESTIVAL:
        fests.append(LUNAR_FESTIVAL[lkey])
    return fests

def describe(d):
    lunar = ZhDate.from_datetime(d)
    jq = jieqi_of(d)
    fests = festivals_of(d, lunar)
    weekday = "一二三四五六日"[d.weekday()]
    parts = [f"{d.strftime('%Y-%m-%d')} 星期{weekday}", f"农历 {lunar.chinese()}"]
    if jq:
        parts.append(f"节气: {jq}")
    if fests:
        parts.append("节日: " + "、".join(fests))
    return " | ".join(parts)

def main():
    args = sys.argv[1:]
    if not args:
        print("用法: python lunar_date.py 2013-01-01 [--range N]  或  python lunar_date.py lunar 2013 1 1")
        return
    if args[0] == "lunar":
        y, m, dd = int(args[1]), int(args[2]), int(args[3])
        d = ZhDate(y, m, dd).to_datetime()
        print(f"农历 {y}年{m}月{dd}日 → 公历 {d.strftime('%Y-%m-%d')} 星期{'一二三四五六日'[d.weekday()]}")
        return
    d = datetime.strptime(args[0], "%Y-%m-%d")
    rng = 0
    if "--range" in args:
        rng = int(args[args.index("--range") + 1])
    if rng:
        print(f"=== {d.strftime('%Y-%m-%d')} 前后 {rng} 天的节日/节气 ===")
        for i in range(-rng, rng + 1):
            dd = d + timedelta(days=i)
            lunar = ZhDate.from_datetime(dd)
            fests = festivals_of(dd, lunar)
            jq = jieqi_of(dd)
            if fests or jq:
                marker = "  ← 今天" if i == 0 else ""
                print(describe(dd) + marker)
    else:
        print(describe(d))

if __name__ == "__main__":
    main()
