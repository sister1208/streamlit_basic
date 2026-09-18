import glob
from pathlib import Path
import pandas as pd

# csv_data.py 파일 위치 기준으로 상위 폴더(Streamlit_Basic) 경로 감지
base_dir = Path(__file__).resolve().parent.parent
file_paths = sorted(base_dir.glob("*_입찰공고 내역.csv"))

df_list = []

for file in file_paths:
    # 1. 파일 상단 메타데이터를 건너뛰기 위해 실제 헤더 위치 탐색
    with open(file, "r", encoding="utf-16") as f:
        lines = f.readlines()

    skip_idx = 0
    for i, line in enumerate(lines):
        if "조달방식" in line and "입찰공고번호" in line:
            skip_idx = i
            break

    # 2. 데이터 읽기 (utf-16, 탭 구분자)
    df = pd.read_csv(file, encoding="utf-16", sep="\t", skiprows=skip_idx)
    df_list.append(df)

if df_list:
    # 3. 데이터 병합 및 저장
    merged_df = pd.concat(df_list, ignore_index=True)
    output_path = base_dir / "입찰공고내역_통합.csv"
    merged_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(
        f"총 {len(merged_df):,}건 병합 완료!\n저장 파일: {output_path}"
    )
else:
    print(f"경로에서 CSV 파일을 찾지 못했습니다: {base_dir}")