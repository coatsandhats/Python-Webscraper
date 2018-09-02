import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

# Get first url data, see if url has page listed
my_url = input("Enter full newegg paged url: ")
if my_url.split("?")[0][-7] == "/":
        split_url = [my_url.split("?")[0].split("/P")[0], my_url.split("?")[1]]
else:
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
filename = input("Enter csv file name(no extension): ") + ".csv"
f = open(filename, "w")
headers = "brand, product_name, shipping\n"
f.write(headers)

# Get and check page range
while True:
    start = int(input("Enter page range start: "))
    if 1 <= start < max_pages:
        break
while True:
    end = int(input("Enter page range end: "))
    if 1 < end <= max_pages:
        break

# Loop through url pages and get product containers
for page in range(start, end):
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
        # fix for csv github quotes
        format_product_name = (product_name.replace(',', '|')).replace('"', "")
        f.write(f"{brand.replace(',', '|')},{format_product_name},{shipping.replace(',', '|')}\n")

f.close()
