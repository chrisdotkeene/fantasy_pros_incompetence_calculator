from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import argparse

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
    accumulated_score = []
    # df = pd.DataFrame(columns=['Team Number', 'Scores'])

    for week in range(1, 15):
        # accumulated_score = []
        for i, value in enumerate(args.team_number):
            print('LOG: ' + str(i))
            team_id = value
            print('TEAM: ' + str(team_id))
            team_url = "https://fantasy.nfl.com/league/2535774/team/{}/gamecenter?week={}".format(
                team_id, week)
            driver.get(team_url)
            current_url = driver.current_url
            time.sleep(5)
            if team_url == current_url:
                time.sleep(5)
                element = driver.find_element(
                    By.XPATH, "//div[contains(@class, 'teamTotal teamId-{}')]".format(team_id))
                accumulated_score.append(element.text)
        print(accumulated_score)
        # df.loc[len(df)] = accumulated_score
        # print(df)
    return accumulated_score


def create_csv(score):
    df = pd.DataFrame(columns=['Team Number'])
    df.loc[len(df)] = score
    # df['Team Number'] = teams
    # df['Scores'] = score

    # weekly_scores = {
    #     'Team Number': teams,
    #     'Final Score': score
    # }
    # df = pd.DataFrame(weekly_scores)
    print(df)


url = "https://id.nfl.com/account/sign-in"
driver = webdriver.Chrome("./chromedriver/chromedriver",
                          chrome_options=init_options(), desired_capabilities=init_caps())

driver.implicitly_wait(10)

driver.get(url)

username = "batman313rd@gmail.com"
p_word_not_pussy = "oracle212rd"

time.sleep(1)

driver.find_element(
    By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/input').send_keys(username)
driver.find_element(
    By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div[1]/div[2]/input').send_keys(p_word_not_pussy)
driver.find_element(
    By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div/div').click()

time.sleep(10)
driver.implicitly_wait(10)

__gather_team_scores()
