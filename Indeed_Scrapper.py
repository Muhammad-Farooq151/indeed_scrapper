from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
import time
import pandas as pd

keywords_to_check = ["ReactJs", "angular", "React js", "React.js", "front end", "front-end", "frontend", "javascript"]
keywords_to_skip = ["401", "php", "wordpress", "Shopify", " Ruby on Rails", "ROR", "SysOps"]

chrome_options = Options()
proxy = ""  # HOST:PORT
chrome_options.add_argument(f'--proxy-server={proxy}')

driver = webdriver.Chrome(options=chrome_options)

Job_data = []
current_page = 0

while True:
    driver.get(
        f'https://www.indeed.com/jobs?q=frontend+reactjs&l=United+States&sc=0kf%3Aattr%28DSQF7%29%3B&sc=0kf&fromage=1&start={current_page}')
    time.sleep(random.uniform(8.5, 10.9))

    try:
        close = driver.find_element(By.XPATH, '//button[@class="popover-x-button-close"]')
        close.click()
    except:
        pass

    jobs = driver.find_elements(By.XPATH, '//div[@class="slider_item css-kyg8or eu4oa1w0"]')

    for job in jobs:
        job.location_once_scrolled_into_view  # Scroll into view
        job.click()
        time.sleep(random.uniform(4.6, 6.9))

        job_url = driver.current_url
        try:
            job_title = driver.find_element(By.XPATH,
                                            '//h2[@class="jobsearch-JobInfoHeader-title css-161nklr e1tiznh50"]').text.strip()
        except:
            job_title = 'NaN'
        try:
            company = driver.find_element(By.XPATH, '//div[@data-testid="jobsearch-CompanyInfoContainer"]').text.strip()
        except:
            company = 'NaN'
        try:
            location = driver.find_element(By.XPATH,
                                           '//div[@data-testid="jobsearch-CompanyInfoContainer"]').text.strip()
        except:
            location = 'NaN'
        try:
            salary = driver.find_element(By.XPATH, '//div[@id="salaryInfoAndJobType"]').text.strip()
        except:
            salary = 'NaN'
        try:
            job_description = driver.find_element(By.XPATH,
                                                  '//div[@class="jobsearch-JobComponent-description css-10ybyod eu4oa1w0"]').text.strip()
        except:
            job_description = 'NaN'

        skip_job = any(keyword.lower() in job_description.lower() for keyword in keywords_to_skip)

        keyword_matches = [keyword for keyword in keywords_to_check if keyword.lower() in job_description.lower()]

        if not skip_job and keyword_matches:
            data = {'Job_Title': job_title, 'Company': company, 'Location': location, 'Salary': salary,
                    'Job_Description': job_description, 'Job_URL': job_url, 'Keyword_Matches': ', '.join(keyword_matches)}
            Job_data.append(data)
            print(len(Job_data))
            print(Job_data)
            print('[*] Saving')
            print("\n")

    try:
        next_page_link = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next Page"]')
        next_page_link.click()
        current_page += 10
        time.sleep(random.uniform(8.5, 10.9))
    except:
        break

df = pd.DataFrame(Job_data)

excel_filename = 'reactjs.xlsx'
df.to_excel(excel_filename, index=False)

driver.quit()
