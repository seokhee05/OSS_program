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

from datetime import datetime  # 날짜 형식 검사, 처리 위해

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

def main():
    init_file()
    while True:
        menu()
        choice = input("메뉴 선택: ").strip()
        if choice == '1':
            add_expense()
