# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import multiprocessing as mp
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K':1000, 'M':1000000, 'B':1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)

def worker(num, q):
    driver = webdriver.Chrome(PATH, options=chrome_options)
    wait = WebDriverWait(driver, 0.1)
    a_list = []

    while num <= (num + 1):
        try:
            driver.get("https://www.allrecipes.com/cook/" + str(num) + "/favorites/")
            try:
                likes = driver.find_element_by_xpath(
                    '//*[@id="main-content"]/section/div[1]/ul/li[2]/ul[2]/li[2]/span')
            except:
                continue
            bool = True
            print('getting profile of user ' + str(num))
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
                num += 1
                continue
            recipe_str = ""
            i = 0
            added = 0
            while added != int(likes):
                i += 1
                print(str(i))
                if i > added + 50:
                    break
                try:
                    recipe = wait.until(EC.presence_of_element_located(
                        (By.XPATH,
                         '(//*[@id="main-content"])/div[4]/div[1]/div[2]/div/div[1]/section/div/article[' + str(
                             i) + ']/div/div/div/div[2]/h3/a/span')))
                except:
                    continue

                # recipe = driver.find_element_by_xpath('//*[@id="main-content"]/div[4]/div[1]/div[2]/div/div[1]/section/div/article['+str(i)+']/div/div/div/div[2]/h3/a/span')
                if i == 1:
                    recipe_str += recipe.text
                else:
                    recipe_str += "," + recipe.text
                print(recipe_str)
                added += 1

            a_list.append([str(num), recipe_str])
        except:
            num += 1
            continue
    q.put(a_list)
    return a_list

def listener(q):
    with open('recipes2.csv', 'w', newline='') as csvfile:
        while 1:
            m = q.get()
            if m == 'kill':
                break
            writer = csv.writer(csvfile)
            writer.writerow(m)
            csvfile.flush()

def start_process():
    print ('Starting', mp.current_process().name)

def main():
    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(mp.cpu_count() + 2, initializer=start_process)

    watcher = pool.apply_async(listener, (q,))

    jobs = []
    for i in range(14):
        job = pool.apply_async(worker, (1 * i, q))
        jobs.append(job)

    for job in jobs:
        job.get()

    q.put('kill')
    pool.close()
    pool.join()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
