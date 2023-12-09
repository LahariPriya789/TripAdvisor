import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

lisi = ['/Tourism-g295424-Dubai_Emirate_of_Dubai-Vacations.html','/Tourism-g255060-Sydney_New_South_Wales-Vacations.html']
for link in lisi:

    url = 'https://www.tripadvisor.in'+link
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}

    resp = requests.get(url,headers=headers)

    jsoup = BeautifulSoup(resp.content, 'html.parser')
    ul = jsoup.find('ul', attrs={'class':'TAcAQ'})
    li = jsoup.find_all('li', attrs={'class': 'Mkrpq Fg I _u'})

    main = []
    for lis in li:
        dummy = dict()
        a = lis.find('a', attrs={'class':'BMQDV _F Gv wSSLS SwZTJ hNpWR'})
        if a is None:
            continue
        div = a.find('div', attrs={'class': 'biGQs _P fiohW alXOW NwcxK GzNcM ytVPx UTQMg RnEEZ ngXxk'})
        div2 = a.find('div', attrs={'class': 'biGQs _P pZUbB hmDzD'})

        link = a['href']
        description = div2.text if div2 else None
        if link:
            for_extract = re.search('\/[a-zA-Z]*',link)
            type = for_extract.group(0).strip('/')

        # dummy['Link'] = link
        dummy['Type'] = type
        dummy['Description'] = description
        main.append(dummy)

print(len(main))
# for i in main:
#     print(i)

df = pd.DataFrame(main)
def clean_description(text):
    if text is not None:
        # Remove unwanted characters like '₹' and '•'
        text = text.replace('₹', '').replace('•', '').strip()
        # Encode and decode to handle encoding issues
        return text.encode('utf-8').decode('utf-8', 'ignore')
    else:
        return None

# Apply the clean_description function to the 'Description' column
df['Description'] = df['Description'].apply(clean_description)


print(df)





# for i,j in df.groupby('Type'):
#     print(i)


# custom_order = ['Attraction', 'Hotel', 'Restaurant', 'VacationRentalReview']
# df['Type'] = pd.Categorical(df['Type'], categories=custom_order, ordered=True)
# df = df.sort_values(['Type','Link'])
# df = df.reset_index(drop=True)
# print(df)
# df.to_csv('D:\\$PYTHON\\ travel.csv', index=False)