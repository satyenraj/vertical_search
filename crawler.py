import requests
from bs4 import BeautifulSoup
import robotexclusionrulesparser

rerp = robotexclusionrulesparser.RobotExclusionRulesParser()

def crawl_website(url):
    #Request the page with list of publications
    response = requests.get(url)
    rerp.parse(response.text)
    
    if rerp.is_allowed("*", url):
        #Fetch the page only if it is allowed by robots.txt
        response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        #Find container element for publication collection
        publication_items = soup.find_all("div", class_="result-container")

        publications = []

        for publication_item in publication_items:
            publications.append(extract_publication_info(publication_item))

        return publications
    
def extract_publication_info(publication_item):
    publication_dict = {
        "title": "",
        "authors": [],
        "publication_year":"",
        "publication_link":""
    }

    #extracts publication title
    title = publication_item.find("h3", class_="title")
    if title:
        publication_dict["title"] = title.get_text(strip = True)

    authors_elements =publication_item.find_all("a", class_="link person")
    authors_with_link = []

    #extracts publication authors with link
    for author in authors_elements:
        author_name = author.get_text(strip = True)
        author_profile_link = author["href"]
        author_dict = {
            "name": author_name,
            "link": author_profile_link
        }
        authors_with_link.append(author_dict)

    authors = []
    #extracts publication authors
    for author in publication_item.find_all("span", class_="")[1:-1]:
        author_dict = {
            "name": author.get_text(strip = True),
            "link": ""
        }
        for author_with_link in authors_with_link:
            if author_with_link["name"] == author.get_text(strip = True):
                author_dict["link"] = author_with_link["link"]
        authors.append(author_dict)
    publication_dict["authors"] = authors

    #publication date
    publication_year = publication_item.find("span", class_="date")
    if publication_year:
        publication_dict["publication_year"] = publication_year.get_text(strip = True)

    #publication link
    publication_link = publication_item.find("a", class_="link")
    if publication_link:
        publication_dict["publication_link"] = publication_link["href"]

    return publication_dict