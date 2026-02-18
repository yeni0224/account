import datetime
import sys
from init_db import household


#날짜, 유형, 카테고리, 금액, 메모를 입력받아 MongoDB에 저장
def register_data():
    str_date = input('날짜 (yyyy-MM-dd) : ').strip()
    try:
        date = datetime.datetime.strptime(str_date, '%Y-%m-%d')
    except:
        print("잘못된 날짜 형식으로 입력했습니다. (yyyy-MM-dd)로 입력하세요")
        return False
    
    consumption_type = input('소비 유형(income/expense) : ').strip()
    # income 혹은 expense만 입력받을 수 있도록 조건 걸기
    if consumption_type == 'income' or consumption_type == 'expense':    
        categories = input('카테고리 :').strip()
        price = int(input('금액 :'))
        memo = input('메모 :')
        household.insert_one({'date': date, 'consumption_type':consumption_type,'category':categories,'price':price,'memo':memo})
        print('거래 내역을 등록했습니다.')
    else : 
        print('income 혹은 expense 둘 중 하나를 반드시 입력하세요')


#모든 거래 내역을 날짜 기준으로 출력
def search_data():
    datas = household.find({},{'_id':0})
    for data in datas:
        print(data)

#_id 기준으로 특정 내역의 금액 또는 메모 수정
def change_data():
    #id를 기준으로 검색한다.
    input_id = input('ID를 검색하세요 :').strip()
    search_id = household.find_one({'_id':{'$exists':input_id}})

    if search_id :
        #수정할 내역은 총 2개이며 어떤 항목을 수정할지 선택한다.
        selection_str = input('어떤 항목을 수정하시겠습니까? (금액 / 메모) :').strip()
        #금액을 수정할 때
        if selection_str == '금액':
            input_amount = int(input('수정할 금액을 입력하세요:'))
            household.update_one({'_id':search_id['_id']},{'$set':{'amount':input_amount}})
        #메모를 수정할 때
        elif selection_str == '메모':
            input_memo = input('수정할 메모를 입력하세요 :')
            household.update_one({'_id':search_id['_id']},{'$set':{'memo':input_memo}})
        else : 
            print('잘못된 입력')
    else : 
        print('해당 ID는 존재하지 않습니다.')
        return False

#_id 기준으로 특정 내역 삭제
def delete_data():
    input_id = input('삭제할 데이터의 ID를 검색하세요 :').strip()
    try:
        if input_id:
            household.delete_one({'_id':input_id})
        else : 
            print('해당 ID는 존재하지 않습니다.')
            return False
    except:
        print('해당 입력 양식은 잘못되었습니다.')
        return False


#특정 월(YYYY-MM)을 입력받아 총 지출 금액 계산
def sum_monthly():
    input_date = input('지출 금액을 계산할 달을 입력하세요(YYYY-MM):').strip()
    update_input_date = datetime.datetime.strptime(input_date, '%Y-%m')

    #인풋값에 해당하는 월 범위 설정
    start_date = datetime.datetime(update_input_date.year, update_input_date.month, 1)
    if update_input_date.month == 12: 
        end_date = datetime.datetime(update_input_date.year + 1, 1, 1) 
    else: 
        end_date = datetime.datetime(update_input_date.year, update_input_date.month + 1, 1)

    pipeline = [{"$match":{"date":{"$gte":start_date, "$lt":end_date}}},
                {"$group":{"_id":None,"total":{"$sum":"$price"}}}]
    result = list(household.aggregate(pipeline))
    
    # 해당하는 월의 ($group) 총 지출의 합($sum)
    if result:
        result_sum = result[0]["total"]
        print('해당 월의 지출 합계는', result_sum,'입니다.')
    else : 
        print('해당 월의 지출은 존재하지 않습니다.')
        return False

#지출 내역을 카테고리별로 그룹화하여 합계 출력
def sum_category():
    input_category = input('확인할 지출 카테고리 :').strip()

    # $cond 연산자로 income/expense 연산시 음양연산자 설정
    pipeline = [{"$match":{"category":input_category}},{"$group":{"_id":None,"price_sum": {"$sum": {
        "$cond":[{"$eq":["$consumption_type","expense"]},{"$multiply":["$price",-1]}, "$price"]}}}}]
    result = list(household.aggregate(pipeline))
    if result:
        print("해당 카테고리의 지출 :",result[0]['price_sum'])
    else:
        print("해당 카테고리를 찾을 수 없습니다.")

#카테고리별 이용내역 조회
def search_category():
    input_category = input('확인할 지출 카테고리 : ').strip()
    
    result = list(household.find({"category":input_category},{"_id":0}))
    if result:
        for n in result:
            print("해당 카테고리의 지출 :",n)
    else:
        print("해당 카테고리를 찾을 수 없습니다.")

#프로그램 종료
def quit_program():
    sys.exit()