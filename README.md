==지출 관리 프로그램==

목적 : 개인의 지출 데이터를 관리하고, 통계/분석/시각화를 통해 소비 패턴을 파악해준다. 또한, 음성 인식을 활용해 직접 입력하지 않고 자동으로 저장하게 한다.

상세 기능 :

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

그래프 보기 위해 다음을 입력하여 설치
pip install matplotlib

음성 인식을 위해 다음을 입력하여 설치
pip install speechrecognition
pip install pyaudio  # 설치 오류 시 → pip install pipwin && pipwin install pyaudio
pip install matplotlib
    
입출력 형태 : 
대부분은 input()을 사용하여 날짜(YYYY-MM-DD), 항목명(문자열), **금액(숫자)**을 받는다 
음성 입력은 "2025년 6월 5일 커피 3000원" 같은 문장을 말하면 자동으로 입력되어 저장되고, 날짜는 datetime.strptime()로 유효성 검사를 수행한다.
