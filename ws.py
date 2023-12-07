import re
import pandas as pd
from bs4 import BeautifulSoup
import requests


def get_school_info(soup):
    def get_ratings():
        rating_tags = soup.find_all(
            "div",
            attrs={"class": re.compile(r"^GradeSquare__ColoredSquare-sc-6d97x2-0")},
        )
        rating_tags_text = [tag.text for tag in rating_tags]
        return rating_tags_text[:10]

    def get_school_name():
        school_tag = soup.title
        return school_tag.text.split("|")[0].strip()

    return [get_school_name()] + get_ratings()


def get_rankings(n):
    info = []
    for i in range(1, n):
        print("Scraping school", i)
        url = "https://www.ratemyprofessors.com/school/" + str(i)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            info.append(get_school_info(soup))
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

    df = pd.DataFrame(info)
    df.to_csv("schools.csv")


get_rankings(10)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
driver = webdriver.Chrome()
url = "https://www.ratemyprofessors.com/school/440"

driver.get(url)

button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Show More")]'))
)

# Click the button
while True:
    button.click()

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")


def top_n(soup, n):
    strings_list = [
        tag.text
        for tag in soup.find_all(
            "div", {"class": "SchoolRating__RatingComment-sb9dsm-6 eNyCKI"}
        )
    ]
    from collections import Counter

    big_string = " ".join(strings_list)
    all_words = [
        word
        for word in big_string.split(" ")
        if not word.lower()
        in ["and", "is", "the", "to", "a", "i", "of", "in", "are", "you"]
    ]
    word_counts = Counter(all_words)

    top_n_words = word_counts.most_common(n)

    return top_n_words


print(top_n(soup, 100))
