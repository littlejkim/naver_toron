import webbrowser
import re
from selenium import webdriver

regexp = re.compile('[^0-9a-zA-Z]+')

options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(
    'C:/Users/NHWM/Downloads/chromedriver', chrome_options=options)


countries_list = "m_gtsnation.txt"
stock_list = "m_gtsstock_m.txt"

failed = []


usa = []
# NQQ = 나스닥
# NYY = 뉴욕증권거래소
# BTQ = 아멕스

china = []
# SHZ = 선강퉁
# SHC = 후강퉁

hongkong = []
# HKG = 홍콩 > 앞에 0 제거하고 조회함

japan = []
# TYO = 일본

vietnam = []
# HSX = 호치민
# HNX = 하노이

total_count = 0

with open(stock_list) as f:
    content = f.readlines()
    content = [x.strip() for x in content]
    for line in content:
        line = line.split("|", 5)
        market = line[4]
        country = line[0][0:3]
        code = line[0][3:]
        if(country == "USA"):
            usa.append(market + code)
            total_count += 1
        elif(country == "CHN"):
            china.append(market + code)
            total_count += 1
        elif(country == "HKG"):
            hongkong.append(market + code)
            total_count += 1
        elif(country == "JPN"):
            japan.append(market + code)
            total_count += 1
        elif(country == "VNM"):
            vietnam.append(market + code)
            total_count += 1

total = len(usa) + len(china) + len(hongkong) + len(vietnam) + len(japan)
print(total)


def checkNaver(code):
    url = "https://m.stock.naver.com/worldstock/index.html#/stock/" + code + "/total"
    browser.implicitly_wait(2)
    browser.get(url)
    try:
        element = browser.find_element_by_class_name("GraphMain_name__2HcQl")
        print("Stock found: " + element.text)
        return True
    except:
        print("Failed to find stock")
        failed.append(code)
        return False


def findVietnam():
    success = 0
    for data in vietnam:
        print("Searching for stock: " + data)
        market = data[0:3]
        code = data[3:]
        # 호치민 (HSX)는 ".HM", 하노이 (HNX)는 ".HN" 붙힘
        if(market == "HSX"):
            code = code + ".HM"
        elif(market == "HNX"):
            code = code + ".HN"
        if(checkNaver(code) == True):
            success += 1
    return success


def findJapan():
    success = 0
    for data in japan:
        print("Searching for stock: " + data)
        # 일본은 모두 ".T" 뒤에 붙힘
        code = data[3:] + ".T"
        if(checkNaver(code) == True):
            success += 1
    return success


def findHongKong():
    success = 0
    for data in hongkong:
        print("Searching for stock: " + data)
        # 홍콩은 모두 ".HK" 뒤에 붙힘
        code = data[4:] + ".HK"
        if(checkNaver(code) == True):
            success += 1
    return success


def findChina():
    success = 0
    for data in china:
        print("Searching for stock: " + data)
        market = data[0:3]
        code = data[3:]
        # 선강퉁 (SHZ)은 뒤에 ".SZ", 후강퉁 (SHC)는 뒤에 ".SS" 붙힘
        if(market == "SHZ"):
            code = code + ".SZ"
        elif(market == "SHC"):
            code = code + ".SS"
        if(checkNaver(code) == True):
            success += 1
    return success


def findUS():
    success = 0
    for data in usa:
        print("Searching for stock: " + data)
        market = data[0:3]
        code = data[3:]
        # 나스닥 종목은 뒤에 모두 ".O" 붙음
        if(market == "NQQ"):
            code = code + ".O"
        # 이외 거래소
        else:
            addK = False

            # 4자리 티커는 뒤에 ".K" 붙힘
            if(len(code) == 4 and '_' not in code and '.' not in code):
                addK = True
            elif(regexp.search(code)):
                temp = re.split('[. _]', code)
                if(len(temp[0]) == 4):
                    addK = True

            # 티커 뒤에 "." 붙는 경우 특수 종목
            if "." in code:
                split = code.split('.', 1)
                # A class, B class 등
                if split[1] == 'A' or split[1] == 'B' or split[1] == "C" or split[1] == 'V':
                    code = split[0] + split[1].lower()
                elif(split[1] == 'U'):  # stock unit
                    code = split[0] + "_" + split[1].lower()
                elif(split[1] == 'RT'):  # stock rights
                    code = split[0] + "_" + split[1][0:1].lower()
                elif(split[1] == 'RT.WI'):  # stock rights when issued
                    code = split[0] + "_r_w"

            # 티커 뒤에 "_P" 붙는 경우 우선주 (A, B, C 등)
            if "_" in code:
                split = code.split('_', 1)
                code = split[0] + '_' + split[1].lower()
            if (addK == True):
                code = code + ".K"

        if(checkNaver(code) == True):
            success += 1
    return success


# result = findUS() + findChina() + findHongKong() + findJapan() + findVietnam()
# print("Number of stocks searched: " + str(total_count))
# print("Number of succeeded search: " + str(result))
# print("Failed stocks: " + str(failed))

browser.close()
