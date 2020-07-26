from format import Data, Row
from bs4 import BeautifulSoup
import requests
import re

results = Data()

baseURL = "https://assembly.nu.ca"

baseHTML = requests.get(baseURL+"/members/mla").content.decode("utf-8")
soup = BeautifulSoup(baseHTML, "html.parser")
members = soup.find_all("div", {"class": re.compile(r"member-photo")})


for member in members:
    url = baseURL + member.find("a")["href"]

    personal_page = BeautifulSoup(requests.get(url).content.decode("utf-8"), "html.parser")

    card = personal_page.find("div", {"class": re.compile(r"node-member")})

    bio = ""
    paragraphs = card.find("div", {"class": re.compile(r"content")}).find_all("p", recursive=False)
    for p in paragraphs:
        bio += p.text + " "

    name = personal_page.find("h1", {"class": "page-title"}).text
    name = re.sub(r"The Honourable ", "", name)
    first_name = name.split(" ")[0]
    last_name = name.split(" ")[1]

    email = card.find_all("span", {"class": "spamspan"})[0].text
    email = re.sub(r" \[dot\] ", ".", email)
    email = re.sub(r" \[at\] ", "@", email)

    alt_email = card.find_all("span", {"class": "spamspan"})[1].text
    alt_email = re.sub(r" \[dot\] ", ".", alt_email)
    alt_email = re.sub(r" \[at\] ", "@", alt_email)

    address = card.find("div", {"class": re.compile(r"constituency")}).find("p").text
    address = re.sub(r"(?<=Phone)(?s)(.*$)", "", address)
    address = re.sub(r"Phone", "", address)

    valid_num = re.findall(r"\([0-9]{3}\) [0-9]{3}-[0-9]{4}", str(card))

    alt_role = personal_page.find("div", {"class": re.compile(r"duties")})

    row = Row(
        "Nunavut",
        "Provincial",
        "Legislative Assembly",
        None,
        None, 
        None,
        None,
        "MLA",
        re.sub(r"\n+", ",", alt_role.text) if alt_role else None,
        bio,
        name,
        first_name,
        last_name,
        None,
        None,
        email + "," + alt_email,
        card.find("img")["src"],
        url,
        url,
        None,
        None,
        None,
        None,
        None,
        "Legislative and Constituency",
        address,
        valid_num[0]+","+valid_num[2],
        valid_num[1]+","+valid_num[3]
    )

    results.append(row)

results.export("nunavut.csv")