# BS imports
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests


def get_school_info(soup):
    """A function that reads a given soup object and returns the school name and ratings

    Args:
        soup (object): a BeautifulSoup object from a RateMyProfessors website

    Returns:
        list: the information about the school as one list
    """

    def get_ratings():
        """A sub-function that gets just the ratings from a given site.

        Returns:
            list: the ratings of the school
        """
        rating_tags = soup.find_all(
            "div",
            attrs={"class": re.compile(r"^GradeSquare__ColoredSquare-sc-6d97x2-0")},
        )
        rating_tags_text = [tag.text for tag in rating_tags]
        return rating_tags_text[:10]

    def get_school_name():
        """A sub-function that gets just the school's name from the title tag.

        Returns:
            string: the school's name
        """
        school_tag = soup.title
        return school_tag.text.split("|")[0].strip()

    return [get_school_name()] + get_ratings()


def get_rankings(n):
    """A function that scrapes a given number of schools off RMP and writes their information to a file.

    Args:
        n (int): the number of schools to scrape.
    """

    # We store the output as a list
    info = []
    for i in range(1, n):
        # Updates the user on scraping process
        print("Scraping school", i)
        # Boilerplate scraping code
        url = "https://www.ratemyprofessors.com/school/" + str(i)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Actually calling the function we have defined to produce a list of lists
            info.append(get_school_info(soup))
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

    # A convenient method from pandas for turning a list of lists into a file
    df = pd.DataFrame(info)
    df.to_csv("schools.csv")


# Executing the function
get_rankings(10)

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# An alternative, but deprecated method of initializing the Driver.
# driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")

driver = webdriver.Chrome()
url = "https://www.ratemyprofessors.com/school/440"
driver.get(url)

# A concise way to locate the button -- credited to ChatGPT
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Show More")]'))
)

# Click the button until we get to the bottom of the page
while True:
    button.click()

# Extracting the html for manipulation and passing into a BS object
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")


def top_n(soup, n):
    """A function to find the most common words on a school's website.

    Args:
        soup (object): a BeautifulSoup object obtained from a RMP site
        n (int): we obtain the top-n words

    Returns:
        list: the top-n words and counts as a list of tuples
    """
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
        in [
            "and",
            "is",
            "the",
            "to",
            "a",
            "i",
            "of",
            "in",
            "are",
            "you",
            "for",
            "it",
            "with",
        ]
    ]
    word_counts = Counter(all_words)

    top_n_words = word_counts.most_common(n)

    return top_n_words


print(top_n(soup, 100))

# Challenge: write the data to a file
