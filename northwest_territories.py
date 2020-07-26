# Northwest territories representatives
# TODO: Paulie Chinna, missing
from bs4 import BeautifulSoup
import pandas as pd
from format import Row, Data
import requests
import re
from typing import Tuple

def parse_bio(html) -> str:
    """
    Extract the biography
    """
    txt_elements = html.find_all("div", {"class": "field-items"})[1].find_all("p")
    start = False
    result = ""
    for element in txt_elements:
        if element.text == "Oath of Office":
            break
        if start:
            result += " " + element.text
        if element.text == "Biography":
            start = True
    return result

def parse_email(html) -> str:
    """
    extract the email
    """
    txt_elements = html.find_all("div", {"class": "field-items"})[1].find_all("p")
    for element in txt_elements:
        a = element.find("a")
        if a:
            if "@" in a.text: 
                return a.text
    return None

baseURL = "https://www.ntassembly.ca"

results = Data()

baseHTML = requests.get(baseURL+"/members").content.decode("utf-8")
soup = BeautifulSoup(baseHTML, "html.parser")

reps = soup.find_all("td", {"class": re.compile(r"views-row-members")})

for rep in reps:
    url = baseURL + str(rep.find("a", {"href": re.compile("meet-members")})["href"])
    personal_page = BeautifulSoup(requests.get(url).content.decode("utf-8"), "html.parser")
    name = personal_page.find("h1", {"id": "page-title"}).text
    phone = re.findall(r"[0-9]{3}-[0-9]{3}-[0-9]{4}", str(requests.get(url).content))

    row = Row(
        "Northwest Territories",
        "Provincial",
        "Legislative Assembly",
        None,
        None,
        None,
        None,
        "MLA",
        None,
        parse_bio(personal_page),
        name,
        name.split(" ")[0],
        name.split(" ")[1],
        None,
        None,
        parse_email(personal_page),
        personal_page.find("img")["src"],
        url,
        url,
        None,
        None,
        None,
        None,
        None,
        "Member's Office",
        "P.O. Box 1320 Yellowknife NT  X1A 2L9",
        phone[0] if phone else None,
        None
    )

    results.append(row)

results.export("northwest_territories.csv")