import requests
from bs4 import BeautifulSoup
from format import Data, Row


def getInfo(url):
    dict = {}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # -------------------------- pic
    pic = 'https://www.edmonton.ca/' +  list(soup.find_all('img', class_="left"))[0]['src']
    dict['pic'] = pic
    bioLst = list(soup.find_all('div', class_="content"))[0]
    # -------------------------- bio
    bio = ''
    bioLst = list(bioLst.find_all('p'))
    for item in bioLst:
        bio += item.get_text() + "\n"
    dict['bio'] = bio
    # -------------------------- many info
    info = list(soup.find_all('tr'))[1:]
    for item in info:
        key = list(item.find_all('th'))[0].get_text()
        value = list(item.find_all('td'))[0].get_text()
        dict[key] = value
    # -------------------------- address
    addr = list(soup.find_all('address'))[0]
    addr  = list(addr.find_all('p'))[0].get_text()
    dict['addr'] = addr

    return dict



if __name__ == '__main__':
    page = requests.get("https://www.edmonton.ca/city_government/city_organization/city-councillors.aspx")

    soup = BeautifulSoup(page.content, 'html.parser')
    data = Data()
    all = list(soup.find_all('div', class_="documentexcerpt-module__item"))
    #print(all)
    for item in all:
        line = 'https://www.edmonton.ca/' + item.find_all('a')[0]['href']
        name = item.find_all('h3')[0].get_text().split("-")[-1].strip()
        #print(line)
        #print(name)
        dict = getInfo(line)
        #----------------------------------

        source_url = line
        Website = dict.get("Website")
        Province = "Edmonton"
        Affiliation = None
        Telephone = dict.get("Telephone")
        Fax = dict.get("Fax")
        Email = dict.get("Email")
        Staff = None
        name = name
        bio = dict.get("bio")
        first_name = name.split()[0]
        last_name = name.split()[-1]
        photo_url = dict.get("pic")
        facebook = dict.get("Facebook")
        instagram = dict.get("Instagram")
        twitter = dict.get("Twitter")
        linkedin = None
        youtube = None
        address = dict.get("addr")
        # ----------------------------------


        # --------------------------------------------------------------------------- add to ROW

        row = Row(Province, 'Senate', 'Senate', None, None, \
                  None, None, 'Senator', None, bio, name, first_name, last_name, \
                  None, None, Email, photo_url, source_url, Website, facebook, instagram, twitter, linkedin, \
                  youtube, None, address, Telephone, Fax)

        data.append(row)

        # ------------------------------------------------------------------------------ export data
    data.export('edmonton.csv')
    print('done')

    '''
        print(Website)
        print(Province)
        print(Telephone)
        print(Fax )
        print(Email )
        print(name)
        print(bio )
        print(first_name )
        print(last_name )
        print(photo_url )
        print(facebook  )
        print(instagram )
        print(twitter)
    '''