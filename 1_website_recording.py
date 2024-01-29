import time, subprocess, csv
from threading import Timer
import pandas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

DRIVER_PATH = '/Users/moonma/Downloads/chromedriver-mac-x64/chromedriver'
LEADS_FNAME = 'csv/100_batch.csv'
PAGE_LOAD_TIME = 4
SCROLL_WAIT_TIME = 2
video_time = PAGE_LOAD_TIME + SCROLL_WAIT_TIME*3

service = Service(executable_path=DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

df_raw = pandas.read_csv(LEADS_FNAME)
with open("csv/failed_urls.csv", 'a', newline='') as failed_url_csv:
    csvwriter = csv.writer(failed_url_csv, delimiter=',')

    for index, row in df_raw.iterrows():
        url = row['organization_primary_domain']
        if not url.startswith('http://www.'): url = 'http://www.' + url
        print(f"row#{index}: {url}")

        try:
            driver.get(url)
        except Exception:
            csvwriter.writerow(row)
            print(f"    {url} → NOT WORKING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            continue
        print(f"url split: {url.split('.')[-2]}")
        video_fname = str(index) + '_' + url.split('.')[-2] + "_" + row['first_name'] + "_" + row['last_name'] + '.mov'
        proc = subprocess.Popen(['screencapture', '-v', "video/1-recording/"+video_fname], stdin=subprocess.PIPE)
        kill = kill = lambda process: process.kill()
        video_timer = Timer(video_time, kill, [proc])

        last_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(PAGE_LOAD_TIME)
        
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_WAIT_TIME)

        # Scroll to top
        driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
        time.sleep(SCROLL_WAIT_TIME*2)

        try:
            video_timer.start()
            stdout, stderr = proc.communicate()
        finally:
            video_timer.cancel()