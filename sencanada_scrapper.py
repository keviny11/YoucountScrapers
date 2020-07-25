import requests
from bs4 import BeautifulSoup
from format import Data, Row

def getPersonalPage(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    name = list(soup.find_all('h1', class_="biography_card_name"))[0].get_text()[7:].strip()
    Staff = list(soup.find_all('ul', class_="biography_card_details"))
    Staff = Staff[0].get_text()
    lst = Staff.strip().split("\n")
    for i in range(len(lst)):
        lst[i] = lst[i].strip()[lst[i].find(" ") + 1:]

    lst = [i for i in lst if i != ""]
    lst1 = []
    for i in range(len(lst)):
        if lst[i] == 'Follow:':
            lst1 = lst[0:i]
            lst1.append(lst[i + 1:])
    if len(lst1) != 0:
        lst = lst1

    if len(lst) > 6 and not type(lst[6]) == list:
        lst[6] = lst[6][lst[6].find(" ") + 1:]
    lst.append(name)

    # ------------------- bio info ---------------------
    bio = ''
    bioList = list(soup.find_all('h2', class_='section_title'))[0].parent
    bioList = list(bioList.find_all('p'))
    for item in bioList:
        bio += item.get_text() + '\n'
    lst.append(bio)

    # ------------------- profile pic ---------------------
    pic = 'https://sencanada.ca' + list(soup.find_all('img', class_="biography_image"))[0]['src']
    lst.append(pic)

    return lst




if __name__ == '__main__':

    # set up data frame
    data = Data()

#------------------------------------------------ prepare data
    page = requests.get("https://sencanada.ca/en/senators/")
    print(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    all=list(soup.find_all('div', class_="senators-page-card-speaker"))
    all.extend(list(soup.find_all('div', class_="senators-page-card-officer")))
    all.extend(list(soup.find_all('div', class_="senators-page-card")))

    for item in all:

        source_url = 'https://sencanada.ca' + list(item.find_all('a'))[0]['href']
        lst = getPersonalPage(source_url)

#----------------------------------------------- empty variables
        Website = None
        Social = []
        Province = None
        Affiliation = None
        Telephone = None
        Fax = None
        Email = None
        Staff = None
        name = None
        bio = None
        first_name = None
        last_name = None
        photo_url = None
        facebook = None
        instagram = None
        twitter = None
        linkedin = None
        youtube = None

#--------------------------------------------------- parser
        name = lst[-3]
        first_name = name.split(' ')[0].strip()
        last_name = "".join(name.split(' ')[1:]).strip()
        bio = lst[-2]
        photo_url = lst[-1]
        lst = lst[:-3]
        Province = lst[0]
        Affiliation = lst[1]
        if len(lst) > 2:
            Telephone = lst[2]
        if len(lst) > 3:
            Fax = lst[3]
        if len(lst) > 4:
            Email = lst[4]
        if len(lst) > 5:
            Staff = lst[5]
        if len(lst) > 6:
            if not type(lst[6]) == list:
                Website = lst[6]
            else:
                Social = lst[6]
        if len(lst) > 7 and lst[7] != name:
            Social = lst[7]

        #------------------- classify social media
        for item in Social:
            if 'twitter' in item:
                twitter = item
            elif 'facebook' in item:
                facebook = item
            elif 'instagram' in item:
                instagram = item
            elif 'youtube' in item:
                youtube = item

# --------------------------------------------------------------------------- add to ROW

        row = Row( Province, 'Senate', 'Senate', None, None,\
        None, None, 'Senator', None, bio, name, first_name, last_name,\
        None, None, Email, photo_url, source_url, Website, facebook, instagram, twitter, linkedin,\
        youtube, None, None, Telephone, Fax)

        data.append(row)

#------------------------------------------------------------------------------ export data
    data.export('sencanada')
    print('done')





#--------------------------------------------------------------------------- test print
'''
        print('------------------------------------------------------------')
        print('name', ":  ", name)
        print('first_name', ":  ", first_name)
        print('last_name', ":  ", last_name)
        print('Province: ', Province)
        print('Affiliation: ', Affiliation)
        print('Telephone: ', Telephone)
        print('Fax: ', Fax)
        print('Email: ', Email)
        print('Staff: ', Staff)
        print('Website: ', Website)
        print('Social: ', Social)
        print('photo_url: ', photo_url)
        print('bio: ', bio)
'''


