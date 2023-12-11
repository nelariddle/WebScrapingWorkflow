# pip install wikipedi-api
import wikipediaapi

# Boilerplate code for initializing the wikipedia object
wiki_wiki = wikipediaapi.Wikipedia("NelaProject (nelariddle@gmail.com)", "en")


def get_wikipedia_summary(page_title):
    """Function to print the summary of an article

    Args:
        page_title (string): title of the article to find
    """
    page = wiki_wiki.page(page_title)

    if page.exists():
        print("Title:", page.title)
        print("Summary:", page.summary)
    else:
        print("Page does not exist.")


def get_wikipedia_fulltext(page_title):
    """Function to print the text of an article

    Args:
        page_title (string): title of the article to find
    """
    page = wiki_wiki.page(page_title)

    if page.exists():
        print("Title:", page.title)
        print("Full text:", page.text)
    else:
        print("Page does not exist.")


# Calling the function we have defined
page_title = "Indiana University"
get_wikipedia_fulltext(page_title)
