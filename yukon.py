
from format import Data, Row
from bs4 import BeautifulSoup
import requests
import re
import urllib

results = Data()

baseURL = "https://yukonassembly.ca"

baseHTML = requests.get(baseURL+"/mlas").content.decode("utf-8")

soup = BeautifulSoup(baseHTML, "html.parser")

members = soup.find_all("div", {"class": "views-row"})


for member in members:

    url = baseURL + member.find("a")["href"]

    req = urllib.request.Request(url, data=None)
    html = urllib.request.urlopen(req).read().decode("utf-8")

    personal_page = BeautifulSoup(html, "html.parser")
    content = personal_page.find("div", {"class": "content"})
    
    bio = ""

    if content:
        segments = content.find("div", {"class": re.compile(r"summary")}).find_all("p")
        for segment in segments:
            bio += segment.text + " "

    name = content.find("h1", {"class": "page-header"}).text
    if "Hon." in name:
        first_name = name.split(" ")[1]
        last_name = name.split(" ")[2]
    else:
        first_name = name.split(" ")[0]
        last_name = name.split(" ")[1]

    sidebar = personal_page.find("div", {"class": re.compile(r"sidebar")})

    row = Row(
        "Yukon",
        "Provincial",
        "Legislative Assembly",
        None,
        None,
        None,
        None,
        "MLA",
        None,
        bio,
        name,
        first_name,
        last_name,
        None,
        content.find("div", {"class": re.compile(r"party")}).text,
        sidebar.find("a").text,
        baseURL + sidebar.find("img")["src"],
        url,
        url,
        None,
        None,
        None,
        None,
        None,
        None,
        sidebar.find("address").text,
        re.findall(r"[0-9]{3}-[0-9]{3}-[0-9]{4}", str(sidebar))[0],
        re.findall(r"[0-9]{3}-[0-9]{3}-[0-9]{4}", str(sidebar))[1]
    )

    results.append(row)


results.export("yukon.csv")