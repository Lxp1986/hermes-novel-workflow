#!/usr/bin/env python3
"""历史天气查询 — 数据源 Open-Meteo（ERA5 再分析，1940 至今，免费无 key）。

用法:
    python historical_weather.py <lat> <lon> <start> <end> [--hourly]

参数:
    lat/lon   纬度/经度（可用 maps skill 的 search 命令获取）
    start/end 日期 YYYY-MM-DD
    --hourly  额外输出逐小时温度/降水

示例:
    python historical_weather.py 22.25 111.69 2013-01-01 2013-01-07
    python historical_weather.py 22.25 111.69 2013-01-01 2013-01-01 --hourly

说明: ERA5 再分析为网格插值，城市级真实度够用，极端局地天气（短时强对流）可能有偏差。
"""
import sys
import json
import urllib.parse
import urllib.request

API = "https://archive-api.open-meteo.com/v1/archive"


def fetch(lat, lon, start, end, hourly=False):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "Asia/Shanghai",
    }
    if hourly:
        params["hourly"] = "temperature_2m,precipitation"
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "novel-era-data/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    if len(sys.argv) < 5:
        print(__doc__)
        sys.exit(1)
    lat, lon = float(sys.argv[1]), float(sys.argv[2])
    start, end = sys.argv[3], sys.argv[4]
    hourly = "--hourly" in sys.argv
    try:
        d = fetch(lat, lon, start, end, hourly)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

    print(f"地点: ({d.get('latitude', lat):.3f}, {d.get('longitude', lon):.3f})  "
          f"时区 {d.get('timezone', 'Asia/Shanghai')}  海拔 {d.get('elevation', '?')}m")

    daily = d.get("daily", {})
    times = daily.get("time", [])
    if times:
        print("\n日期        | 最高温 | 最低温 | 降水(mm)")
        print("-" * 44)
        for i, t in enumerate(times):
            tmax = daily["temperature_2m_max"][i]
            tmin = daily["temperature_2m_min"][i]
            prec = daily["precipitation_sum"][i]
            print(f"{t} | {tmax:5.1f}° | {tmin:5.1f}° | {prec:6.1f}")

    if hourly:
        h = d.get("hourly", {})
        htimes = h.get("time", [])
        if htimes:
            print("\n逐小时:")
            print("时间                  | 温度   | 降水mm")
            for i, t in enumerate(htimes):
                tmp = h["temperature_2m"][i]
                prec = h["precipitation"][i]
                print(f"{t} | {tmp:5.1f}° | {prec:5.1f}")


if __name__ == "__main__":
    main()
