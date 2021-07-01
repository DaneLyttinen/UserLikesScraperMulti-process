# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
import time

PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

THREADS = 5;

def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K':1000, 'M':1000000, 'B':1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)

"""
scrapes allrecpies for user: (num) likes

Returns:
    {"user (int): [ Likes ](strings) "}
"""
def scrapper(num, file):
    
    driver = webdriver.Chrome(PATH, options=chrome_options)
    wait = WebDriverWait(driver, 0.1)
    file.write('[')
    a_list = []
    userNum = 1040 + num
    while(1):
        try:
            driver.get("https://www.allrecipes.com/cook/" + str(userNum) + "/favorites/")
            try:
                likes = driver.find_element_by_xpath(
                    '//*[@id="main-content"]/section/div[1]/ul/li[2]/ul[2]/li[2]/span')
            except:
                print('error 1')
            bool = True
            # print('getting profile of user ' + str(num))
            count = 0
            while bool:
                try:
                    driver.find_element_by_xpath('//*[@id="recipeBoxMoreBtn"]').click()
                    time.sleep(1)
                    count += 1
                    print('found ' + str(count))
                except:
                    bool = False
            likes = likes.text
            print(likes)
            try:
                int(likes)
            except:
                likes = convert_str_to_number(likes)
            if int(likes) < 10:
                # num += 1
                userNum += num + THREADS
                print('error2')
            recipe_str = ""
            i = 0
            added = 0
            while added != int(likes):
                i += 1
                # print(str(i))
                if i > added + 50:
                    break
                try:
                    recipe = wait.until(EC.presence_of_element_located(
                        (By.XPATH,
                            '(//*[@id="main-content"])/div[4]/div[1]/div[2]/div/div[1]/section/div/article[' + str(
                                i) + ']/div/div/div/div[2]/h3/a/span')))
                except:
                    pass

                    # recipe = driver.find_element_by_xpath('//*[@id="main-content"]/div[4]/div[1]/div[2]/div/div[1]/section/div/article['+str(i)+']/div/div/div/div[2]/h3/a/span')
                    if i == 1:
                        recipe_str += recipe.text
                    else:
                        recipe_str += "," + recipe.text
                    # print(recipe_str)
                    added += 1

                a_list.append([str(userNum), recipe_str])
        except:
            # num += 1
            userNum += num + THREADS
        try:
            a_list.pop()
            UserLikes = {userNum: a_list[-1][1]}
            file.write(f"{str(UserLikes)},")
            file.flush()
            # return UserLikes
        except:
            # return
            continue
        userNum += num + THREADS

def main():
    workerPool = [] 
    for i in range(1, THREADS + 1):
        workerPool.append(i) 
    workerPool = tuple(workerPool)
    print(workerPool)
    with open("worker1.txt", 'w') as worker1, open("worker2.txt", 'w') as worker2,  open("worker3.txt", 'w') as worker3,  open("worker4.txt", 'w') as worker4,  open("worker5.txt", 'w') as worker5:
        with ThreadPoolExecutor(max_workers=THREADS) as worker:
            worker.map(scrapper, workerPool, (worker1,worker2,worker3,worker4,worker5))
            worker.shutdown()



def test(num):
    a = 1000+num
    print(a)
if __name__ == '__main__':
    main()