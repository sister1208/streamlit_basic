# -*- coding: utf-8 -*-
"""
공공데이터포털 국내 계약정보 API -> CSV 대량 수집기

대상 API:
getDmstcCntrctInfoList

기본 조회기간:
2025-01-01 ~ 2026-09-15

실행:
    pip install requests pandas
    python 국내_계약정보_API_5만건_수집.py

주의:
- 현재 대화에 입력한 서비스키는 노출된 상태이므로 가능하면 공공데이터포털에서
  서비스키를 재발급/교체한 뒤 아래 SERVICE_KEY에 새 키를 넣으세요.
- API가 허용하는 최대 numOfRows에 맞춰 자동으로 페이지를 반복 호출합니다.
- 응답 XML의 실제 필드명을 임의로 바꾸지 않고 가능한 한 원래 태그명을 그대로 CSV 컬럼으로 보존합니다.
- 5만 건 이상이면 totalCount까지 자동으로 수집합니다.
"""

import csv
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

SERVICE_KEY = "EraD/qvK8JCpvEsPoN4CoDtN5Mj5ZLIjKZYahdaFFJccEgZ1EhVrLFZe3d2iutI102EGU+V0FQgozon6lEh/Iw=="

BASE_URL = (
    "https://apis.data.go.kr/1690000/"
    "CntrctInfoService/getDmstcCntrctInfoList"
)

PAGE_SIZE = 1000
DATE_BEGIN = "20250101"
DATE_END = "20260915"

OUTPUT = Path("국내_계약정보_2025-01-01_2026-09-15_전체.csv")

# API 서버/계정 정책에 따라 1000건이 거부되면 100으로 낮춰 재시도
FALLBACK_PAGE_SIZE = 100

def strip_ns(tag):
    return tag.split("}", 1)[-1]

def flatten_xml(element, prefix=""):
    """중첩 XML을 1행짜리 dict로 평탄화."""
    children = list(element)
    if not children:
        return {prefix or strip_ns(element.tag): (element.text or "").strip()}

    result = {}
    for child in children:
        key = strip_ns(child.tag)
        full_key = f"{prefix}.{key}" if prefix else key
        child_children = list(child)
        if child_children:
            nested = flatten_xml(child, full_key)
            for k, v in nested.items():
                # 같은 필드가 반복될 경우 suffix 부여
                if k in result:
                    i = 2
                    nk = f"{k}_{i}"
                    while nk in result:
                        i += 1
                        nk = f"{k}_{i}"
                    result[nk] = v
                else:
                    result[k] = v
        else:
            result[full_key] = (child.text or "").strip()
    return result

def get_xml(page, rows):
    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": page,
        "numOfRows": rows,
        "cntrctDateBegin": DATE_BEGIN,
        "cntrctDateEnd": DATE_END,
    }
    r = requests.get(BASE_URL, params=params, timeout=60)
    r.raise_for_status()
    return r.content

def parse_response(content):
    root = ET.fromstring(content)

    # API 표준 응답에서 totalCount/resultCode를 찾되,
    # 실제 응답 구조가 달라도 local-name 기준으로 탐색
    values = {}
    for el in root.iter():
        name = strip_ns(el.tag)
        if len(list(el)) == 0:
            values[name] = (el.text or "").strip()

    result_code = values.get("resultCode", "")
    result_msg = values.get("resultMsg", "")
    total_count = values.get("totalCount", "")

    # 일반적인 item/items 구조 탐색
    item_elements = []
    for el in root.iter():
        if strip_ns(el.tag).lower() == "item":
            item_elements.append(el)

    rows = [flatten_xml(item) for item in item_elements]

    return result_code, result_msg, int(total_count or 0), rows

def collect():
    if SERVICE_KEY == "여기에_새로운_서비스키_입력":
        raise SystemExit("SERVICE_KEY에 공공데이터포털 서비스키를 입력하세요.")

    all_rows = []
    page = 1
    page_size = PAGE_SIZE
    total_count = None

    while True:
        print(f"[조회] page={page}, numOfRows={page_size}")

        try:
            content = get_xml(page, page_size)
            result_code, result_msg, total, rows = parse_response(content)
        except Exception as e:
            if page_size != FALLBACK_PAGE_SIZE:
                print(f"1000건 조회 실패 → {FALLBACK_PAGE_SIZE}건으로 재시도: {e}")
                page_size = FALLBACK_PAGE_SIZE
                continue
            raise

        if result_code not in ("", "00", "NORMAL SERVICE"):
            raise RuntimeError(
                f"API 오류: resultCode={result_code}, resultMsg={result_msg}"
            )

        if total_count is None:
            total_count = total
            print(f"[전체 건수] {total_count:,}건")

        if not rows:
            print("[종료] 이번 페이지에 데이터가 없어 종료합니다.")
            break

        all_rows.extend(rows)
        print(f"[누적] {len(all_rows):,}건 / {total_count:,}건")

        if len(all_rows) >= total_count:
            break

        page += 1
        time.sleep(0.15)

    if not all_rows:
        raise RuntimeError("수집된 계약 데이터가 없습니다.")

    # 행마다 컬럼이 다를 수 있으므로 전체 컬럼 union
    columns = []
    seen = set()
    for row in all_rows:
        for col in row:
            if col not in seen:
                seen.add(col)
                columns.append(col)

    # CSV UTF-8 BOM: Excel에서 한글이 깨지지 않도록 utf-8-sig
    with OUTPUT.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in all_rows:
            writer.writerow({c: row.get(c, "") for c in columns})

    print()
    print("=== 수집 완료 ===")
    print(f"파일: {OUTPUT.resolve()}")
    print(f"행 수: {len(all_rows):,}")
    print(f"컬럼 수: {len(columns):,}")

if __name__ == "__main__":
    collect()
