# pip install wikipedi-api
import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia("NelaProject (nelariddle@gmail.com)", "en")


def get_wikipedia_summary(page_title):
    page = wiki_wiki.page(page_title)

    if page.exists():
        print("Title:", page.title)
        print("Summary:", page.summary)
    else:
        print("Page does not exist.")


def get_wikipedia_fulltext(page_title):
    page = wiki_wiki.page(page_title)

    if page.exists():
        print("Title:", page.title)
        print("Summary:", page.text)
    else:
        print("Page does not exist.")


page_title = "Indiana University"

get_wikipedia_fulltext(page_title)
