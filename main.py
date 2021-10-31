from bs4 import BeautifulSoup
import requests
import re

search_term = input('What Product you are looking for? ')

url = f'https://www.newegg.ca/p/pl?d={search_term}&N=4131'

page = requests.get(url).text

doc = BeautifulSoup(page, 'html.parser')

page_text = doc.find(class_= 'list-tool-pagination-text').strong
pages = int(str(page_text).split('/')[-2].split('>')[-1][:-1])

items_found = {}

for page in range(1, pages + 1):
    url = f'https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page}'

    page = requests.get(url).text

    doc = BeautifulSoup(page, 'html.parser')

    div = doc.find(class_= 'item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell')

    items = div.find_all(text=re.compile(search_term))
    for item in items:
        parent = item.parent
        if parent.name != 'a':
            continue
        link = parent['href']

        next_parent = item.find_parent(class_= 'item-container')
        price = next_parent.find(class_= 'price-current').strong.string

        items_found[item] = {'price': int(price.replace(',', '')), 'link': link}

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])
#.items create a tuple with all the keys and values from dictionary like [('3080 FTW', {'price':299, 'link': 'http:.....')].
#then we created a lambda fucntion that allows us to grab second item which is the dictionary
#then we grabbed price.

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
