import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Get first url data
my_url = "https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709&cm_sp=Tab_Gaming-Video-Cards_1-_-LeftNav-_-All-Cards"
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

# Set max pages
nav = page_soup.find_all("div", {"id": "page_NavigationBar"})
btns = nav[-1].find_all("div", {"class": "btn-group-cell"})
max_pages = int(btns[9].button.text)

# Create csv file
filename = "products.csv"
f = open(filename, "w")
headers = "brand, product_name, shipping\n"
f.write(headers)

# Loop through url pages and get product containers
for page in range(1, 54):
    paged_url = f"https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48/Page-{page}?Tid=7709&cm_sp=Tab_Gaming-Video-Cards_1-_-LeftNav-_-All-Cards"
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.findAll("div", {"class": "item-container"})

# Loop through product containers
    for container in containers:
        brand = container.div.div.img["title"]
        product_name = container.a.img["alt"]
        shipping_container = container.findAll("li", {"class": "price-ship"})
        shipping = shipping_container[0].text.strip()
        f.write(f"{brand.replace(',', '|')},{product_name.replace(',', '|')},{shipping.replace(',', '|')}\n")

f.close()
