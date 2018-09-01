import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

# Get first url data
my_url = input("Enter full newegg url on 1st page: ")
split_url = my_url.split("?")
u_client = urlopen(my_url)
page_html = u_client.read()
u_client.close()
page_soup = soup(page_html, "html.parser")

# Set max pages
nav_bar = page_soup.find_all("div", {"id": "page_NavigationBar"})
btns = nav_bar[-1].find_all("div", {"class": "btn-group-cell"})
max_pages = int(btns[9].button.text)

# Create csv file
filename = "products1.csv"
f = open(filename, "w")
headers = "brand, product_name, shipping\n"
f.write(headers)

# Loop through url pages and get product containers
for page in range(1, 54):
    paged_url = f"{split_url[0]}/Page-{page}?{split_url[1]}"
    u_client = urlopen(paged_url)
    page_html = u_client.read()
    u_client.close()
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.find_all("div", {"class": "item-container"})

# Loop through product containers
    for container in containers:
        brand = container.div.div.img["title"]
        product_name = container.a.img["alt"]
        shipping_container = container.find_all("li", {"class": "price-ship"})
        shipping = shipping_container[0].text.strip()
        f.write(f"{brand.replace(',', '|')},{product_name.replace(',', '|')},{shipping.replace(',', '|')}\n")

f.close()
