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
        school_tag = soup.find("title")
        return school_tag.text.split("|")[0].strip()

    return [get_school_name()] + get_ratings()


info = []
for i in range(1, 100):
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


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Assuming you have installed and set up the appropriate web driver (e.g., Chrome WebDriver)
# Replace 'path_to_chromedriver' with the path to your Chrome WebDriver executable
driver = webdriver.Chrome(executable_path="chromedriver.exe")

# URL of the webpage containing the button
url = "https://www.ratemyprofessors.com/school/440"  # Replace this with the URL of the webpage

driver.get(url)

# Wait for the button to be clickable
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Show More")]'))
)

# Click the button
button.click()

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

print(
    [
        tag.text
        for tag in soup.find_all(
            "div", {"class": "SchoolRating__RatingComment-sb9dsm-6 eNyCKI"}
        )
    ]
)

# After clicking, you can continue with further interactions or scraping on the updated page
