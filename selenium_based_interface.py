from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import keyboard
import matplotlib.pyplot as plt

"""

TODO: 
    figure out why score element sometimes dissapears

"""


def main():

    #set up objects for selenium
    gecko_path = r'geckodriver-v0.26.0-win64\\geckodriver.exe'
    driver = webdriver.Firefox(executable_path=gecko_path)
    driver.get('http://slither.io/')

    # set up some action chains for control
    action_enter = ActionChains(driver)
    action_enter.send_keys(Keys.ENTER)

    action_left = ActionChains(driver)
    action_left.key_up(Keys.ARROW_RIGHT)
    action_left.key_down(Keys.ARROW_LEFT) # selenium documentation actually says not to do this with non special keys but it seems to work fine

    action_right = ActionChains(driver)
    action_right.key_up(Keys.ARROW_LEFT)
    action_right.key_down(Keys.ARROW_RIGHT)

    #set a name and off we go
    start = ActionChains(driver)
    start.send_keys("butt")
    start.send_keys(Keys.ENTER)
    start.perform()
    time.sleep(3)

    max_rounds = 1
    num_rounds = 0
    while num_rounds < max_rounds:
        num_rounds = num_rounds + 1 
        score = 0
        past_scores = []
        flag = driver.find_element_by_id("lastscore").is_displayed()
        while flag is not None and flag is not True:
            # get the score. Score occasionally dissapears for reasons yet unkown hence the try except
            try:
                score_elem = driver.find_elements_by_xpath("//html//body//div[13]//span[1]//span[2]") 
                if score_elem is not None and len(score_elem) > 0:
                    score = int(score_elem[0].get_attribute('innerHTML'))
                    past_scores.append(score)

            except:
                # Exception as e:
                # print(e)
                pass


            action_right.perform()

            flag = driver.find_element_by_id("lastscore").is_displayed()


        # plt.plot(past_scores)

        # plt.show()

        action_enter.perform()
        time.sleep(3)     


    driver.quit()




if __name__=="__main__":
    main()