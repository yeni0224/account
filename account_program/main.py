from account_program.functions import *

#카테고리 이름을 변수화

def main():
    menu = {
        '1' : register_data,
        '2' : search_data,
        '3' : change_data,
        '4' : delete_data,
        '5' : sum_monthly,
        '6' : sum_category,
        '0' : quit_program
    }

    while True:
        print('====< account system >====')
        print('1. 수입/지출 등록')
        print('2. 전체 내역 조회')
        print('3. 금액 /메모 수정')
        print('4. 내역 삭제')
        print('5. 월별 지출 합계')
        print('6. 카테고리별 지출 통계')
        print('0. 프로그램 종료')

        choice = input('작업할 항목의 번호를 입력하시오 : ')
        action = menu.get(choice)

        if choice == False : continue

        if action : action()
        else : print('작업을 진행할 수 없습니다.')

if __name__ == '__main__':
    main()