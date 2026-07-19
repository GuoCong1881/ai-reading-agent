#!/usr/bin/env python3
"""创建一个全天 Google Calendar 事件,用于同步每日阅读材料 Issue。

用法:
    python3 scripts/create_calendar_event.py "<标题>" "<YYYY-MM-DD>" "<描述,建议包含Issue链接>"

需要环境变量:
    GOOGLE_SERVICE_ACCOUNT_KEY  服务账号 JSON key 的完整内容
    GOOGLE_CALENDAR_ID          目标日历 ID(通常是你的 Gmail 地址,或日历设置里的 Calendar ID)

如果两个环境变量缺失,视为没有配置日历同步,直接跳过(退出码 1,但不抛异常),
调用方(workflow prompt)应当把这种失败当作非致命错误处理。
"""
import json
import os
import sys

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def main() -> int:
    if len(sys.argv) != 4:
        print("用法: create_calendar_event.py <标题> <YYYY-MM-DD> <描述>", file=sys.stderr)
        return 1

    title, date_str, description = sys.argv[1:4]

    key_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY")
    calendar_id = os.environ.get("GOOGLE_CALENDAR_ID")
    if not key_json or not calendar_id:
        print("缺少 GOOGLE_SERVICE_ACCOUNT_KEY 或 GOOGLE_CALENDAR_ID,跳过日历同步", file=sys.stderr)
        return 1

    creds = service_account.Credentials.from_service_account_info(
        json.loads(key_json), scopes=SCOPES
    )
    creds.refresh(Request())

    event = {
        "summary": title,
        "description": description,
        "start": {"date": date_str},
        "end": {"date": date_str},
    }
    resp = requests.post(
        f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events",
        headers={"Authorization": f"Bearer {creds.token}"},
        json=event,
        timeout=30,
    )
    if not resp.ok:
        print(f"日历事件创建失败: {resp.status_code} {resp.text}", file=sys.stderr)
        return 1

    print(resp.json().get("htmlLink", "日历事件已创建"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
