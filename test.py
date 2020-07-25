import requests
from bs4 import BeautifulSoup

page = requests.get("https://sencanada.ca/en/senators/")
print(page)
soup = BeautifulSoup(page.content, 'html.parser')
all = list(soup.find_all('div', class_="senators-page-card-speaker"))
all.extend(list(soup.find_all('div', class_="senators-page-card-officer")))
all.extend(list(soup.find_all('div', class_="senators-page-card")))

for item in all:
    a = list(item.parent.find_all('h4', class_="red roboto-bold"))

    print(a)
    for items in a:

        print(items.get_text())
