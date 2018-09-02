import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

# Get first url data, see if url has page listed
my_url = input("Enter newegg url(with a space after): ")
u_client = urlopen(my_url)
page_html = u_client.read()
u_client.close()
page_soup = soup(page_html, "html.parser")

# Set max pages
nav_bar = page_soup.find_all("div", {"id": "page_NavigationBar"})
btns = nav_bar[-1].find_all("div", {"class": "btn-group-cell"})
max_pages = int(btns[-2].button.text)

# Create csv file
filename = input("Enter csv file name(no extension): ") + ".csv"
f = open(filename, "w")
headers = "brand, product_name, price, shipping\n"
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

# Loop through url pages and get product containers.
# (first type is paged listed default, second type is page listed variant.)
for page in range(start, end+1):
    if my_url.split("?")[0][-7] == "/":
        split_url = [my_url.split("?")[0].split("/P")[0], my_url.split("?")[1]]
        paged_url = f"{split_url[0]}/Page-{page}?{split_url[1]}"
        print(f"first type: page {page}")
    elif ("IsNodeId=1&N" in my_url) or (my_url[-9:] == "IsNodeId=1 ") or (my_url[-7] == 'P') or ("Submit=ENE&N" in my_url):
        split_url = my_url.split("&Page=")[0][:-2]
        paged_url = f"{split_url}&Page={page}"
        print(f"second type: page {page}")
    elif ("IsNodeId=1&bop" in my_url) or ("IsNodeId=1&p" in my_url):
        split_url = [my_url.split("PageSize")[0].split("Page=")[0] + "Page=", "PageSize" + my_url.split("PageSize")[1]]
        paged_url = f"{split_url[0]}{page}{split_url[1]}"
        print(f"third type: page {page}")
    else:
        paged_url = f"{my_url[:-1]}/Page-{page}"
        print(f"fourth type: page {page}")
    u_client = urlopen(paged_url)
    page_html = u_client.read()
    u_client.close()
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.find_all("div", {"class": "item-container"})

    # Loop through product containers
    for container in containers:
        if not container.div.div.img:
            brand = "None"
        else:
            brand = container.div.div.img["title"]
        if not container.a.img:
            product_name = "None"
        else:
            product_name = container.a.img["alt"]
        shipping_container = container.find_all("li", {"class": "price-ship"})
        shipping = shipping_container[0].text.strip().split("Ship")[0]
        price_container = container.find_all("li", {"class": "price-current"})
        if not price_container[0].strong:
            price = "None"
        else:
            price = price_container[0].strong.text
        # fix for csv github quotes
        format_product_name = (product_name.replace(',', '|')).replace('"', "inch")
        f.write(f"{brand.replace(',', '|')},{format_product_name}, {price.replace(',', '')}, {shipping.replace(',', '')}\n")

f.close()
