import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from Trip_Location import final_result


do_result = []
for i,dummy in enumerate(final_result):
    location = dummy['Location Name']
    link = dummy['Link']
    # print(location)

    url = 'https://www.tripadvisor.in'+link
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}

    resp = requests.get(url,headers=headers)

    jsoup = BeautifulSoup(resp.content, 'html.parser')
    ul = jsoup.find('ul', attrs={'class':'TAcAQ'})
    li = jsoup.find_all('li', attrs={'class': 'Mkrpq Fg I _u'})

    for lis in li:
        do_dict = dict()
        a = lis.find('a', attrs={'class':'BMQDV _F Gv wSSLS SwZTJ hNpWR'})
        if a is None:
            continue

        div = a.find('div', attrs={'class':'biGQs _P fiohW alXOW NwcxK GzNcM ytVPx UTQMg RnEEZ ngXxk'})

        div2 = a.find('div', attrs={'class':'biGQs _P pZUbB hmDzD'})

        name = div.text
        link = a['href']
        if link:
            for_extract = re.search('\/[a-zA-Z]*',link)
            type = for_extract.group(0).strip('/')

        description = div2.text if div2 else None


        do_dict['Id'] = i+1
        do_dict['Location'] = location
        do_dict['Name'] = name
        do_dict['Link'] = link
        do_dict['Description'] = description
        do_dict['Type'] = type

        do_result.append(do_dict)

print(do_result)

df = pd.DataFrame(do_result)
df = df[df['Type'] != 'Trips']
df = df.sort_values(['Id','Type'])
df.to_csv('D:\\$PYTHON\\ travel.csv', index=False)