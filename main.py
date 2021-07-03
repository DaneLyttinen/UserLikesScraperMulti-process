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

def worker(num):
    driver = webdriver.Chrome(PATH, options=chrome_options)
    wait = WebDriverWait(driver, 0.1)
    
    end = num + 10
    header = ['id', 'recipes']
    with open('recipes'+str(num)+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        while num <= (end):
            a_list = []
            try:
                
                driver.get("https://www.allrecipes.com/cook/" + str(num) + "/favorites/")
                """
                If the profile does not exist through the iterative process of simply adding 1
                to get each profile, we want to skip and go ahead to the next number.
                """
                try:
                    likes = driver.find_element_by_xpath(
                        '//*[@id="main-content"]/section/div[1]/ul/li[2]/ul[2]/li[2]/span')
                except Exception as e:
                    print(e)
                    num += 1
                    continue
                bool = True
                print('getting profile of user ' + str(num))
                count = 0
                """
                Try to load all the favorited recipes through clicking the load more button
                until it doesn't exist any more
                """
                while bool:
                    try:
                        driver.find_element_by_xpath('//*[@id="recipeBoxMoreBtn"]').click()
                        time.sleep(1)
                        count += 1
                    except:
                        print('clicked button ' + str(count) + ' times')
                        bool = False
                likes = likes.text
                """
                For large numbers the number of favourites might be abbreviated to 1k.
                the function convert_str_to_number() fixes this
                """
                try:
                    likes = int(likes)
                except:
                    likes = convert_str_to_number(likes)
                """
                I don't want to consider profiles which aren't active and won't give much information
                """
                if likes < 10:
                    num += 1
                    continue
                recipe_str = ""
                i = 0
                added = 0
                while added != likes:
                    i += 1
                    print(str(i))
                    """
                    Sometimes all recipes wouldn't be listed so below if statement will stop an infinite loop
                    """
                    if i > added + 50:
                        break
                    try:
                        recipe = wait.until(EC.presence_of_element_located(
                            (By.XPATH,
                             '(//*[@id="main-content"])/div[4]/div[1]/div[2]/div/div[1]/section/div/article[' + str(
                                 i) + ']/div/div/div/div[2]/h3/a/span')))
                    except:
                        continue

                   
                    a_list.append(recipe.text)
                    print(recipe.text)
                    added += 1
                """
                Finally write data to a file
                """
                a_list.append(str(num))
                a_list.append(recipe_str)
                writer.writerow(a_list)
                csvfile.flush()
                num += 1
            except:
                num += 1
                continue
        driver.quit()


def start_process():
    print ('Starting', mp.current_process().name)

def main():
    pool = mp.Pool(mp.cpu_count() + 2, initializer=start_process)

    jobs = []
    for i in range(14):
        job = pool.apply_async(worker, (i * 10,))
        jobs.append(job)
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()



