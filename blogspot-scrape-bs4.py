import sys
import io
import requests
from bs4 import BeautifulSoup
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Fetch the pages
result = requests.get("https://perfectrecipeproject.blogspot.com/")
content = result.text

# Create soup
soup = BeautifulSoup(content, "lxml")

# Find all archive link with the id 'ArchiveList'
box = soup.find('div', id='ArchiveList')
archives = box.find_all('a')

# Create lists needed for stored data
links = []
dates = []
titles = []
writes = []
images = []
labels = []


for archive in archives:
    soup2 = BeautifulSoup(requests.get(archive['href']).text, "lxml")
    posts = soup2.find_all('div', class_='snippet-thumbnail')

    for post in posts:
        link = post.find('a')
        links.append(link)


for post in links:
    soup3 = BeautifulSoup(requests.get(post['href']).text, "lxml")

    post_date = soup3.find('time', class_='published')
    dates.append(post_date['datetime'])

    post_title = soup3.find('h3', class_='post-title entry-title')
    titles.append(post_title.get_text(strip=True, separator=' '))

    post_body = soup3.find('div', class_='post-body-container')
    if post_body:
        writes.append(post_body.get_text(strip=True, separator=' '))
    else:
        writes.append('')

    post_img = post_body.find('img')
    if post_img:
        images.append(post_img['src'])
    else:
        images.append('')

    post_labels = soup3.find('span', class_='byline post-labels')
    if post_labels:
        labels.append(post_labels.get_text(strip=True, separator=','))
    else:
        labels.append('')

df = pd.DataFrame({'date': dates, 'title': titles, 'content': writes, 'image': images, 'label': labels})
df.to_excel('perfectrecipeproject.xlsx', index=False)

print("Program finished")
