from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv
import pandas as pd
import argparse
import json

with open('./pwd_1.json') as json_file:
    data = json.load(json_file)

parser = argparse.ArgumentParser(
    description='Accepts teams to collect score values.')
parser.add_argument('team_number', nargs='+', type=str)
args = parser.parse_args()


def init_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    return options


def init_caps():
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True
    caps['acceptSslCerts'] = True
    return caps


def __gather_team_scores():
    time.sleep(10)
    with open('incompetence_score.csv', mode='w') as incompetence_score:
        incompetence_writer = csv.writer(incompetence_score, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        team_header = []
        for week in range(1, 15):
            accumulated_score = []
            last_item = len(args.team_number)-1
            for i, value in enumerate(args.team_number):
                team_id = value
                if week == 1:
                    print('setting column names ...')
                    team_header.append(team_id)
                    if i == last_item:
                        incompetence_writer.writerow(team_header)
                        print('Header complete')
                team_url = "https://fantasy.nfl.com/league/2535774/team/{}/gamecenter?week={}".format(
                    team_id, week)
                driver.get(team_url)
                current_url = driver.current_url
                print("Team URL:", team_url)
                print("Current URL:", current_url)
                time.sleep(2)
                try:
                    element = WebDriverWait(driver, 20).until(
                        EC.url_to_be(team_url)
                    )
                    if team_url == current_url:
                        try:
                            element = WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'teamTotal teamId-{}')]".format(team_id))))
                            print("URL:", team_url)
                            print("Element:", element.text)
                            accumulated_score.append(element.text)
                        except TimeoutException:
                            print("Element not found for URL:", team_url)
                except TimeoutException:
                            print("Team URL is not the same:", team_url)
            print(accumulated_score)
            incompetence_writer.writerow(accumulated_score)
    print('CSV saved.')


def read_csv(csv):
    df = pd.read_csv(csv)
    print(df)
    print('-- std --')
    print(df.std())
    

url = "https://fantasy.nfl.com/league/2535774/team/1/gamecenter?week=1"
# driver = webdriver.Chrome("./chromedriver/chromedriver",
#                           chrome_options=init_options(), desired_capabilities=init_caps())
driver = webdriver.Chrome("../chromedriver/chromedriver",
                          chrome_options=init_options(), desired_capabilities=init_caps())  # Mac Driver

driver.implicitly_wait(10)

driver.get(url)

username = data['username']
password = data['password']

time.sleep(1)

driver.find_element(
    By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/input').send_keys(username)
driver.find_element(
    By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div[1]/div[2]/input').send_keys(password)
driver.find_element(
    By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div/div').click()


__gather_team_scores()

print('opening CSV')

time.sleep(5)

print('opening CSV ...')

read_csv('incompetence_score.csv')
