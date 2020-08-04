from bs4 import BeautifulSoup
from format import Data, Row
import requests
import re

result = Data()

baseURL = "https://www.victoria.ca/EN/main/city"

soup = BeautifulSoup(requests.get(baseURL+"/mayor-council.html").content.decode("utf-8"), "html.parser")

links = soup.find_all("a", {"href": re.compile(r"mayor-council"), "class": "plain"})
for link in links:
    role = None
    if "Councillor" in link.text:
        role = "Councillor"
    elif link.text.startswith("Mayor"):
        role = "Mayor"
    else:
        continue
    personal_page = BeautifulSoup(requests.get("https://www.victoria.ca"+link["href"]).content.decode("utf-8"), "html.parser")
    segments = personal_page.find("div", {"id": "content"}).find_all(["p", "h2", "h3"], recursive=False)

    bio = ""
    start = False
    for s in segments:
        if "<h2>" in str(s) or "<h3>" in str(s):
            if "About" in s.text or "Biography" in s.text:
                start = True
            else:
                start = False
        else:
            if start:
                bio += s.text + " "

    name = re.sub(r"Councillor ", "", personal_page.find("h1").text)
    name = re.sub(r"Mayor ", "", name)

    contact = personal_page.find("div", {"id": "contact-blurb"})
    tmp = contact.find_all("a")
    email = None
    for t in tmp:
        if "@" in t.text:
            email = t.text

    row = Row(
        "British Colombia",
        "Municipal",
        "City Council",
        None,
        None,
        None,
        None,
        role,
        None,
        bio,
        name,
        name.split(" ")[0],
        name.split(" ")[1],
        None,
        None,
        email,
        "https://www.victoria.ca" + personal_page.find("img", {"src": re.compile(r"Council")})["src"],
        "https://www.victoria.ca" + link["href"],
        "https://www.victoria.ca" + link["href"],
        None,
        None,
        None,
        None,
        None,
        None,
        "1 Centennial Square Victoria, BC V8W 1P6", # or use: contact.find_all("p")[1].text
        ",".join(re.sub(r"\.", "-", n) for n in set(re.findall(r"[0-9]{3}\.[0-9]{3}\.[0-9]{4}", str(contact)))),
        None
    )

    result.append(row)

result.export("victoria.csv")

