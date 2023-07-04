# Create a program that collects articles from the https://www.bbc.com/news website. We are only interested in the sections "/business" (Business - without the "Features & Analysis", "Watch/Listen" and "Special reports" subsections) and "/technology" (Tech - without the Watch/Listen and Features & Analysis subsections).

# A. The script should save every article to a separate JSON file, keeping only the article content (TITLE and BODY). All non-relevant content (external links, links to categories, CSS, scripts, multimedia content, etc.) should be removed.

# B. Make sure to keep track of the downloaded content. If run again, the script should only collect articles we have not downloaded already.

# C. (bonus) Containerize your Python application. Outputs should be outside the container.

# The program should be written in Python and could use the Selenium framework.
# In order to keep formatting, please encode your script in Base64 and paste it bellow or you can put a link to your code (https://pastebin.com/ for example or a link to GitHub, GitLab, etc.)
# The scripts which are not working wouldn't be evaluated. Any comments are also welcome.
# Writing a code following PEP 8 is highly recommended.


import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

OUTPUT_DIR = "articles"

def initialize_driver():
    options = Options()
    options.add_argument("--headless")  
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def save_json_article(title,body,output_file):
    article={
        "title":title,
        "body":body
    }
    with open(output_file,"w",encoding="utf8") as file:
        json.dump(article,file, ensure_ascii=False, indent=4)
    print(f'Saved article: {title}')


def scrape_articles(SECTIONS):
    driver=initialize_driver()
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    for section in SECTIONS:
        url=f'https://www.bbc.com/news/{section}'
        driver.get(url)
        section_dir = os.path.join(OUTPUT_DIR, section)
        if not os.path.exists(section_dir):
            os.makedirs(section_dir)
        if section == "business":
            elements = driver.find_elements(By.XPATH, '//a[h3[contains(@class,"gs-c-promo-heading")] and not(ancestor::div[@role="region" and (@aria-labelledby="nw-c-Specialreports__title" or @aria-labelledby="nw-c-Watch/Listen__title" or @aria-labelledby="nw-c-Features&Analysis__title")]) and not(ancestor::nav)]')
            links = [element.get_attribute('href') for element in elements]
        if section == "technology":
            elements = driver.find_elements(By.XPATH, '//a[h3[contains(@class,"gs-c-promo-heading")] and not(ancestor::div[@role="region" and (@aria-labelledby="nw-c-Watch/Listen__title" or @aria-labelledby="nw-c-Features&Analysis__title")]) and not(ancestor::nav)]')
            links = [element.get_attribute('href') for element in elements]
      
        for link in links:
            driver.get(link)
            article_id = link.split("/")[-1]
            # .split("-")[-1]
            output_file=os.path.join(section_dir,f"{article_id}.json")
            if not os.path.exists(output_file):
                title_element = driver.find_element(By.XPATH, '//h1[@class="article-headline__text b-reith-sans-font b-font-weight-300"] | //h1[@id="main-heading"]')
                title = title_element.text
                body_elements = driver.find_elements(By.XPATH, '//div[@data-component="text-block"]//p | //div[@class="article__body-content"]')
                body = '\n'.join([element.text for element in body_elements])
            
                save_json_article(title,body,output_file)

    driver.quit()
if __name__=="__main__":
    SECTIONS = ["business", "technology"]
    scrape_articles(SECTIONS)