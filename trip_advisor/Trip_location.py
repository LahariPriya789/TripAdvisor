import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.tripadvisor.in/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
response = requests.get(url,headers=headers)
page_source = response.content

jsoup = BeautifulSoup(page_source, 'html.parser')
ul = jsoup.find('ul', attrs={'class':'TAcAQ'})
li = ul.find_all('li', attrs={'class':'Mkrpq Fg I _u'})

final_result = []
for lis in li:
    dummy = dict()
    a = lis.find('a', attrs={'class':'BMQDV _F Gv wSSLS SwZTJ hNpWR'})
    name = a.text
    link = a['href']

    dummy['Location Name'] = name
    dummy['Link'] = link

    final_result.append(dummy)

if __name__ == '__main__':
    print(final_result)
    df = pd.DataFrame(final_result)
    print(df)
