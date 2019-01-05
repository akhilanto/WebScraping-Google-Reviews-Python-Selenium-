from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

chrome = webdriver.Chrome("C:\chromedriver\chromedriver.exe")
webdriver = chrome

webdriver.get('https://www.google.com/search?q=greensky+atlanta&oq=greensky+atlanta&aqs=chrome..69i57j0l5.4031j0j4&sourceid=chrome&ie=UTF-8#lrd=0x88f5062f2d23c123:0x8750051f97cc88ef,1,,')

#Reviewer,ReviewDate,ReviewRating,ReviewDescription,TotalReviewsByUser,webdriver_obj,thisreview =([],) * 7
Reviewer =[]
ReviewDate = []
ReviewRating =[]
ReviewDescription = []
TotalReviewsByUser = []
webdriver_obj = []
thisreview =[]
print '!!!'
time.sleep(3)
last_len = 0

def  get_reviews(thisreview):
    global last_len
    print "Don't Stop"
    for webdriver_obj in thisreview.find_elements_by_class_name("WMbnJf"):
        Name = webdriver_obj.find_element_by_class_name("Y0uHMb")
        Reviewer.append(Name.text)
        try:
            ReviewByuser = webdriver_obj.find_element_by_class_name("A503be")
            TotalReviewsByUser.append(ReviewByuser.text)
        except NoSuchElementException:
            TotalReviewsByUser.append("")
        star = webdriver_obj.find_element_by_class_name("fTKmHE99XE4__star")
        ReviewStar =star.get_attribute("aria-label")
        ReviewRating.append(ReviewStar)
        Date = webdriver_obj.find_element_by_class_name("dehysf")
        ReviewDate.append(Date.text)
        Body = webdriver_obj.find_element_by_class_name('Jtu6Td')
        try:
            webdriver_obj.find_element_by_class_name('review-snippet').click()
            s_32B = webdriver_obj.find_element_by_class_name('review-full-text')
            ReviewDescription.append(s_32B.text)
        except NoSuchElementException:
            ReviewDescription.append(Body.text)
        print("Yes..")
        element = webdriver_obj.find_element_by_class_name('PuaHbe')
        webdriver.execute_script("arguments[0].scrollIntoView();", element)
    print("ah!..Go")
    time.sleep(3)
    reviews = webdriver.find_elements_by_class_name("gws-localreviews__general-reviews-block")
    r_len = len(reviews)
    if r_len > last_len:
        last_len = r_len
        get_reviews(reviews[r_len-1])

reviews = webdriver.find_elements_by_class_name("gws-localreviews__general-reviews-block")
last_len = len(reviews)
get_reviews(reviews[last_len-1])

data = pd.DataFrame ( { 'Reviewer' : Reviewer, 'TotalReviewsByUser': TotalReviewsByUser,
                               'ReviewRating':ReviewRating,'ReviewDate':ReviewDate,
                               'ReviewDescription':ReviewDescription})
