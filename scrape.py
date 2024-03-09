import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import http
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

# Bugs: Overall Rating, No Kindle Estore, Same person twice
driver = webdriver.Firefox()

def getReviews(address):
    reviews = []
    driver.get(address)

    next = 1
    qin = True
    if len(queue) > 199:
        qin = False

#finds all of the reviews matching the review class, adds them to reviews array
    while next == 1:

        # time.sleep(0.5)
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "review-text")))
            data = soup.find_all('span', attrs={'class': 'a-size-base review-text review-text-content'})
            driver.implicitly_wait(10)


            for x in data:
                reviews.append(x)

        except:
            print("exception here")

#finding the next page button, if it exists. If not, exiting the loop
        try:
            if qin == True:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                data = soup.find_all(attrs={'class': 'a-profile'})
                for x in data:
                    queue.append("https://www.amazon.com"+x.get('href'))
                if len(queue) > 199:
                    qin = False
                for x in queue:
                    print(x)
            a.click()
            # time.sleep(.2)
        except Exception:
            try:
                print("1")
                time.sleep(0.3)
                pagination = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-pagination")))
                button = pagination.find_element_by_class_name('a-last')
                a = WebDriverWait(button, 2).until(
        EC.element_to_be_clickable((By.TAG_NAME, "a")))
                a.click()
                # time.sleep(.2)
            except Exception:
                    try:
                        print("2")
                        time.sleep(2)
                        pagination = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "a-pagination")))
                        button = pagination.find_element_by_class_name('a-last')
                        a = WebDriverWait(button, 2).until(
                EC.element_to_be_clickable((By.TAG_NAME, "a")))
                        a.click()
                    except Exception:
                        traceback.print_exc()
                        print("END EXCEPTION")
                        next = 0

    print(len(reviews))

    for x in range(len(reviews)):
        # print(x)
        new = str(reviews[x])
        new = new.replace('<span>','')
        new = new.replace('</span>','')
        new = new.replace('<br/>','')
        new = new.replace('<span class="a-size-base review-text review-text-content" data-hook="review-body">','')
        reviews[x] = new
    return reviews

def getBookInfo(address):
    driver.get(address)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data = ""
    title = ""
    try:
        data = soup.find(attrs={'id': 'ebooksProductTitle'})
        title = purgeSpaces(data.text)
    except:
        data = soup.find(attrs={'id': 'productTitle'})
        title = purgeSpaces(data.text)

    print()
    print("Title: " + title)
    data = soup.find(attrs={'class': 'a-link-normal contributorNameID'})
    author = data.text
    print("Author: " + author)
    data = soup.find(attrs={'class': 'a-icon-star'})
    data = data.find("span")
    stars = data.text
    print("Stars: " + stars)
    driver.switch_to.frame("bookDesc_iframe");
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data = soup.find_all("p")
    desc = ""

    for x in data:
#finds whether the character before the added paragraph is a space or a character
        if len(desc)>0:
            if desc[len(desc)-1] != " ":
                desc += " "
        desc += x.text

    print()
    print("Description: ")
    print(desc)

    driver.get(address)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rankcontainers = soup.find_all(attrs={'class':'zg_hrsr_item'})
    ranks = []

    for x in rankcontainers:
        rank = [x.find(attrs={'class' : 'zg_hrsr_rank'}).text,x.find("a").text]
        ranks.append(rank)

    print()
    print("Ranks:")
    for x in ranks:
        print(x)

    rankings = soup.find(attrs={'id' : 'SalesRank'}).text
    id = rankings.find("#")

    overallRank = ""
    try:
        for x in range(len(rankings)):
            if rankings[id+x+1].isdigit():
                overallRank+=rankings[id+x+1]
            else:
                break
    except:
        overallRank = "NONE"

    print()
    print("Overall Rank: ")
    print(overallRank)

    for x in range(40):
        time.sleep(0.1)
        driver.execute_script("window.scrollTo(0, ((document.body.scrollHeight/40)*" + str(x) + "));")
    authorBio = ""
    try:
        WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "authorBio")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        authorBio = purgeSpaces(soup.find(attrs={'id' : 'authorBio'}).text)
        print()
        print("Author Biography: ")
        print(authorBio)
    except Exception:
        traceback.print_exc()
    return ([title,author,stars,desc,ranks,overallRank,authorBio])

def userBooks(address):

    links = []
    books = []

    driver.get(address)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    sections = soup.find_all(attrs={'class' : 'desktop card profile-at-card profile-at-review-box'})
    print(sections)
    for y in sections:
        try:
            stars = y.find(attrs={'class' : 'a-icon-alt'}).text
            print(stars)

            list = y.find(attrs={'class':'a-link-normal profile-at-product-box-link a-text-normal'})
            print(list)

            links.append(["http://www.amazon.com"+list.get('href'),stars])
        except Exception:
            traceback.print_exc()



    print(links)

    for x in links:
        driver.get(x[0])
        try:
            pagination = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "a-color-tertiary")))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            question = purgeSpaces(soup.find(attrs={'class' : 'a-link-normal a-color-tertiary'}).text)
            print(question)
            if question == 'Books':
                books.append([x[0],x[1][0]])
                print(x)
        except:
            print("epic fail")

    return books


    # soup.find(attrs={'class' : 'a-link-normal a-color-tertiary'})
def purgeSpaces(str):
    str = str
    while str[0]== " " or str[0] == "" or ord(str[0])== 10:
        str = str[1:]

    while str[len(str)-1]== " " or str[len(str)-1] == "" or ord(str[len(str)-1])== 10:
        str = str[:len(str)-1]
        # str = str[:len(str)-2]

    return str


def descriptionLinkToReviewLink(link):
    new = link.replace("/dp/","/product-reviews/")
    return new


queue = ["https://www.amazon.com/gp/profile/amzn1.account.AHUDZM3EAZ3BGMZGVRRKH67BDTQQ/ref=cm_cr_dp_d_gw_tr?ie=UTF8"]
data = []
limit = 1000

for x in range(limit):
    try:
        links = userBooks(queue[0])
        for x in links:
            y = getBookInfo(x[0])
            y.append(getReviews(descriptionLinkToReviewLink(x[0])))
            data.append(y)
    except Exception:
        traceback.print_exc()
    del queue[0]

driver.quit()







 #
# reviews = getReviews("https://www.amazon.com/Acer-Display-Graphics-Keyboard-A515-43-R19L/product-reviews/B07RF1XD36/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")
# print(reviews)

    # print(new)



    # for x in reviews:
#     print(x)





#
# for x in range(len(reviews)):
#     reviews[x] = reviews[x].replace('<span>','')
#     reviews[x] = reviews[x].replace('</span>','')
#     reviews[x] = reviews[x].replace('<br />','')
#
# for x in reviews:
#     print(x)
