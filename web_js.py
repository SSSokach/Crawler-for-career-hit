from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains,ActionBuilder
from selenium.webdriver.support.ui import WebDriverWait
from pathlib import Path
import time
import datetime
today = datetime.date.today()
mouth_info=datetime.date.today().month
browser = webdriver.Chrome()
browser.implicitly_wait(10) 
browser.get(r'http://career.hit.edu.cn/zhxy-xszyfzpt/')


def get_all_info():
    huirightcontent=browser.find_element(by=By.CLASS_NAME,value='huirightcontent')
    rightone_list=huirightcontent.find_elements(by=By.CLASS_NAME,value='rightone')
    for one_info_element in rightone_list:
        text=one_info_element.text
        ActionChains(browser)\
            .click(one_info_element)\
            .perform()

    info_list=[]
    original_handle=browser.window_handles[0]
    for handle in browser.window_handles[1:]:
        browser.switch_to.window(handle)
        url=browser.current_url
        title=browser.find_element(by=By.ID,value='zczphxq_zczphmc').text
        time_detial=browser.find_element(by=By.ID,value='zczphxq_zphsj').text
        day_detail=time_detial.split(' ')[0]
        # year,month,day=[int(i) for i in day_detail.split('-')]
        # if month==today.month and day<today.day:
        #     break
        location=browser.find_element(by=By.ID,value='zczphxq_zphcd').text
        info_list.append({
            'title':title,
            'time_detial':time_detial,
            'location':location,
            'url':url
        })
        browser.close()
    browser.switch_to.window(original_handle)

    result=[]
    for one_info in info_list:
        result.append('\n'.join([v for v in one_info.values()]))
    result='\n\n'.join(result)

    
    Path('./info_list').mkdir(parents=True,exist_ok=True,mode=755)
    with open(f'./info_list/{day_detail}', 'w', encoding='utf-8') as file:
        file.write(result)


calendar=browser.find_element(by=By.ID,value='calendar')
all_days=calendar.find_elements(by=By.CLASS_NAME,value='on')

today_and_after=False
for one_day_element in all_days:
    if 'today' in one_day_element.get_attribute('class'):
        print('find today')
        today_and_after=True
    print('class',one_day_element.get_attribute('class'))
    if today_and_after==False:
        continue

    ActionChains(browser)\
        .click(one_day_element)\
        .perform()
    get_all_info()
    ActionBuilder(browser).clear_actions()