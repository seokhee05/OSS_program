# pip install matplotlib 를 명령프롬프트에 입력하여 설치 => 그래프 보기

# pip install speechrecognition
# pip install pyaudio  # 설치 오류 시 → pip install pipwin && pipwin install pyaudio
# pip install matplotlib
# 위의 세개를 명령프롬프트에 입력하여 설치 => 음성 인식

## 지출 관리 프로그램
# 지출 추가
# 전체 기록 보기
# 총 지출 확인
# 지출 삭제
# 지출 수정
# 연간 지출 비교
# 지출 검색
# 지출 그래프 보기
# 음성으로 지출 추가

import csv  # CSV 파일 읽고 쓰기 위해
import os  # 파일 존재 여부 확인 위해
from datetime import datetime  # 날짜 형식 검사, 처리 위해
import matplotlib.pyplot as plt  # 그래프 그리기 위해
import matplotlib.font_manager as fm  # 한글 폰트 설정 위해
import speech_recognition as sr  # 음성 인식 기능 위해
import re  # 정규식으로 음성 텍스트 파싱 위해

# 한글 폰트 설정 (그래프에서 한글 깨짐 방지)
font_path = "C:/Windows/Fonts/malgun.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rc('font', family=fontprop.get_name())

# 데이터 파일 이름 지정
DATA_FILE = "spend_data.csv"

# 프로그램 시작 시 파일이 없으면 새로 생성
def init_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["날짜", "항목", "금액"])

# 1. 지출 추가 (직접 입력)
def add_expense():
    while True:
        date = input("날짜 (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("⚠️ 날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 입력해주세요.")
    item = input("항목명: ").strip()
    while True:
        amount = input("금액: ").strip()
        if amount.isdigit():
            break
        else:
            print("⚠️ 숫자만 입력해주세요.")
    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([date, item, amount])
    print("저장되었습니다.\n")

# 2. 전체 지출 보기
def show_all():
    if not os.path.exists(DATA_FILE):
        print("아직 기록이 없습니다.\n")
        return

    # 연도와 월 입력받기 (엔터 시 전체보기)
    ym_input = input("조회할 연도와 월 입력 (예: 2025-06, 전체보기는 엔터): ").strip()

    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    # 필터링: 입력한 연-월이 있으면 해당 데이터만 필터, 없으면 전체
    if ym_input:
        # 형식 체크 (YYYY-MM)
        if not re.match(r"^\d{4}-\d{2}$", ym_input):
            print("⚠️ 형식이 올바르지 않습니다. YYYY-MM 형식으로 입력해주세요.\n")
            return
        filtered_rows = [row for row in rows if row[0].startswith(ym_input)]
        if not filtered_rows:
            print(f"{ym_input}에 해당하는 기록이 없습니다.\n")
            return
    else:
        filtered_rows = rows

    # 날짜 내림차순 정렬 (YYYY-MM-DD 형식이므로 문자열 내림차순 가능)
    filtered_rows.sort(key=lambda x: x[0], reverse=True)

    print(f"{ym_input if ym_input else '전체'} 지출 내역 :")
    for row in filtered_rows:
        print(f"- {row[0]} | {row[1]} | {row[2]}원")
    print()

# 3. 총 지출 확인 및 항목별 합계
def total_spent():
    if not os.path.exists(DATA_FILE):
        print("아직 기록이 없습니다.\n")
        return
    total = 0
    category_totals = {}
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            try:
                amount = int(row[2])
            except:
                continue
            total += amount
            category = row[1]
            category_totals[category] = category_totals.get(category, 0) + amount
    print(f"총 지출: {total}원")
    print("항목별 지출:")
    for category, amt in category_totals.items():
        print(f"- {category}: {amt}원")
    print()

# 4. 지출 삭제
def delete_expense():
    if not os.path.exists(DATA_FILE):
        print("아직 기록이 없습니다.\n")
        return
    date = input("삭제할 지출 날짜 (YYYY-MM-DD): ").strip()
    item = input("삭제할 항목명: ").strip()
    rows, deleted = [], False
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] == date and row[1] == item:
                deleted = True
                continue
            rows.append(row)
    if deleted:
        confirm = input("정말 삭제하시겠습니까? (y/n): ").strip().lower()
        if confirm != 'y':
            print("삭제 취소.\n")
            return
        with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
        print("삭제 완료.\n")
    else:
        print("해당 지출을 찾을 수 없습니다.\n")

# 5. 지출 수정
def edit_expense():
    if not os.path.exists(DATA_FILE):
        print("아직 기록이 없습니다.\n")
        return
    date = input("수정할 지출 날짜 (YYYY-MM-DD): ").strip()
    item = input("수정할 항목명: ").strip()
    rows, edited = [], False
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] == date and row[1] == item:
                print(f"기존 기록: 날짜={row[0]}, 항목={row[1]}, 금액={row[2]}원")
                while True:
                    new_date = input("새 날짜 (엔터=변경 없음): ").strip()
                    if new_date == "":
                        new_date = row[0]
                        break
                    try:
                        datetime.strptime(new_date, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("날짜 형식 오류.")
                new_item = input("새 항목명 (엔터=변경 없음): ").strip()
                while True:
                    new_amount = input("새 금액 (엔터=변경 없음): ").strip()
                    if new_amount == "" or new_amount.isdigit():
                        break
                    else:
                        print("숫자만 입력해주세요.")
                rows.append([new_date, new_item if new_item else row[1], new_amount if new_amount else row[2]])
                edited = True
            else:
                rows.append(row)
    if edited:
        confirm = input("정말 수정하시겠습니까? (y/n): ").strip().lower()
        if confirm != 'y':
            print("수정 취소.\n")
            return
        with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
        print("수정 완료.\n")
    else:
        print("해당 지출을 찾을 수 없습니다.\n")


# 메뉴 출력
def menu():
    print("""
==지출 관리 프로그램==
1. 지출 추가
2. 전체 보기
3. 총 지출 및 항목별 합계
4. 지출 삭제
5. 지출 수정
6. 연간 지출 비교
7. 지출 검색
8. 지출 그래프 보기
9. 음성으로 지출 입력
10. 지출 패턴 분석
11. 종료
""")

def main():
    init_file()
    while True:
        menu()
        choice = input("메뉴 선택: ").strip()
        if choice == '1':
            add_expense()
        elif choice == '2':
            show_all()
        elif choice == '3':
            total_spent()
        elif choice == '4':
            delete_expense()
        elif choice == '5':
            edit_expense()
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.\n")

# 이 파일이 직접 실행될 경우 main() 실행
if __name__ == "__main__":
    main()
