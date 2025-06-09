## 지출 관리 프로그램
# 지출 추가
# 전체 지출출 보기
# 총 지출 확인
# 지출 삭제
# 지출 수정
# 연간 지출 비교
# 지출 검색
# 지출 그래프 보기
# 음성으로 지출 추가

from datetime import datetime  # 날짜 형식 검사, 처리 위해

# 1. 지출 추가 (직접 입력)
def add_expense():
    while True:
        date = input("날짜 (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 입력해주세요.")
    item = input("항목명: ").strip()
    while True:
        amount = input("금액: ").strip()
        if amount.isdigit():
            break
        else:
            print("숫자만 입력해주세요.")
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
            print("형식이 올바르지 않습니다. YYYY-MM 형식으로 입력해주세요.\n")
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

def main():
    init_file()
    while True:
        menu()
        choice = input("메뉴 선택: ").strip()
        if choice == '1':
            add_expense()
        elif choice == '2':
            show_all()
