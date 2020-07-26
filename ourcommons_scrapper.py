import requests
from bs4 import BeautifulSoup
from format import Data, Row

def getPersonalPage(url):
    lst = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    info = list(soup.find_all('div', class_="ce-mip-mp-profile-container"))[0]
    #print(info.get_text())
    # --------------------------------------------- img
    img = list(info.find_all('img'))[0]['src']
    lst.append(img)
    # --------------------------------------------- party
    party = list(info.find_all('dd', class_="mip-mp-profile-caucus"))[0].get_text()
    lst.append(party)
    # --------------------------------------------- city
    city = list(info.find_all('a'))[0].get_text()
    lst.append(city)
    # --------------------------------------------- province
    province = list(info.find_all('dd'))[2].get_text()
    lst.append(province)


    #---------------------------------------------- contact infos
    contact = list(soup.find_all('div', id="contact"))[0]

    #---------------------------------------------- email
    subcontainer = list(contact.find_all('p'))
    email = subcontainer[0].get_text()
    lst.append(email)

    # ---------------------------------------------- contact infos new
    subcontainers = list(contact.find_all('div', class_='ce-mip-contact-constituency-office col-lg-6 col-md-6 col-sm-12 col-12'))
    subcontainer = subcontainers[0]
    subcontainer_info = list(subcontainer.find_all('p'))

    # ---------------------------------------------- address
    addr_lst = subcontainer_info[0].get_text().split('\n')
    addr_lst = [i.strip() for i in addr_lst if i.strip() != ''][1:]
    addr = ' '.join(addr_lst)
    lst.append(addr)

    # ---------------------------------------------- tel and fax
    tel = subcontainer_info[1].get_text().strip()[subcontainer_info[1].get_text().strip().find(" ") + 1:].strip()
    fax = ''
    if 'Fax' in tel:
        tel = tel.split(' ')[0]
        fax = tel.split(' ')[-1]
    lst.append(tel)
    lst.append(fax)
    name = list(soup.find_all('h1'))[0].get_text()
    lst.append(name)
    return lst




if __name__ == '__main__':

    # set up data frame
    data = Data()

#------------------------------------------------ prepare data
    page = requests.get("https://www.ourcommons.ca/Members/en/search")
    print(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    all=list(soup.find_all('div', class_="col-lg-4 col-md-6 col-xs-12"))

    for item in all:
        link = list(item.find_all('a'))[0]['href']
        source_url = 'https://www.ourcommons.ca' + link
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
        party = None
        address = None

#--------------------------------------------------- parser
        photo_url = lst[0]
        party = lst[1]
        Province = lst[3]
        Email = lst[4]
        address = lst[5]
        Telephone = lst[6]
        name = lst[-1]
        first_name = name.split(' ')[0]
        last_name = ' '.join(name.split(' ')[1:])
        if lst[7] != '':
            Fax = lst[7]

# --------------------------------------------------------------------------- test print
        print('------------------------------------------------------------')
        print('name', ":  ", name)
        print('first_name', ":  ", first_name)
        print('last_name', ":  ", last_name)
        print('Province: ', Province)

        print('Telephone: ', Telephone)
        print('Fax: ', Fax)
        print('Email: ', Email)

        print('photo_url: ', photo_url)
        print('party: ', party)
        print('address: ', address)


# --------------------------------------------------------------------------- add to ROW

        row = Row( Province, 'Senate', 'Senate', None, None,\
        None, None, 'Senator', None, bio, name, first_name, last_name,\
        None, party, Email, photo_url, source_url, Website, facebook, instagram, twitter, linkedin,\
        youtube, None, address, Telephone, Fax)

        data.append(row)

#------------------------------------------------------------------------------ export data
    data.export('sencanada.csv')
    print('done')











