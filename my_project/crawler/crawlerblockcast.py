from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def fetch_to_blockcast(click_time=3,time_sleep=5):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get("https://blockcast.it/")

    time.sleep(20)

    #調整按下顯示更多次數
    for push in range(click_time):
        load_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[5]/div/div[1]/div/div/section[2]/div/div/div/div/div/div/div[2]/div[2]/a")))
    
    driver.execute_script("arguments[0].scrollIntoView(true);", load_button)
    
    time.sleep(1)
    
    driver.execute_script("arguments[0].click();", load_button)
    
    time.sleep(5)

    articles=[]

    article_elements = driver.find_elements(By.TAG_NAME,"article")

    for article in article_elements:
        title_tag = article.find_element(By.TAG_NAME,"h3")
        link_tag = article.find_element(By.TAG_NAME,"a")

        if not title_tag or not link_tag:
            continue

        title = title_tag.text
        href = link_tag.get_attribute("href")


    driver.quit()
    return articles
