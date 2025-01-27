#!/root/path/to/venv/bin/python3
# -*- coding: utf-8 -*-

import requests
import urllib.parse
import time
from datetime import datetime

BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# ชื่อไฟล์ .txt ที่เก็บลิงก์
file_path = 'urls.txt'
SLEEP_DURATION = 0.5 * 60 * 60  # หน่วยเป็นs

def extract_session(url):
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    return query_params.get("session", ["ไม่พบ session"])[0]

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def refresh_links():
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            urls = file.readlines()
    except FileNotFoundError:
        print(f"{RED}[{current_time()}] ไม่พบไฟล์ ตรวจสอบชื่อไฟล์อีกครั้ง{RESET}")
        exit()

    for i, url in enumerate(urls, start=1):
        url = url.strip()
        if not url:
            continue
        try:
            response = requests.get(url)
            if response.status_code == 200:
                session_id = extract_session(url)
                print(f"[{current_time()}] [{i}] {BLUE}Refresh new IP สำเร็จ{RESET} '{GREEN}session={session_id}{RESET}'")
            else:
                # ถ้าไม่ใช่ 200
                print(f"[{current_time()}] [{i}] {RED}ไม่สามารถเปิด {url} ได้ (Status Code: {response.status_code}){RESET}")
        except requests.exceptions.RequestException as e:
            # เกิดข้อผิดพลาด
            print(f"[{current_time()}] [{i}] {RED}เกิดข้อผิดพลาดกับ {url}: {e}{RESET}")

while True:
    print(f"{YELLOW}[{current_time()}] Starting script ...{RESET}")
    refresh_links()
    print(f"{YELLOW}[{current_time()}] พัก 1/2 ชั่วโมง ...{RESET}")
    time.sleep(SLEEP_DURATION)
    print(f"{YELLOW}[{current_time()}] กำลังเริ่มสคริป ...{RESET}")

