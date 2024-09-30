import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Dictionary of product categories with corresponding URLs
categories = {
    "Mobiles": "https://priceoye.pk/mobiles?page=",
    "Wireless Earbuds": "https://priceoye.pk/wireless-earbuds?page=",
    "Smart Watches": "https://priceoye.pk/smart-watches?page=",
    "Trimmers & Shavers": "https://priceoye.pk/trimmers-shaver?page=",
    "Power Banks": "https://priceoye.pk/power-banks?page=",
    "Mobile Chargers": "https://priceoye.pk/mobile-chargers?page=",
    "Bluetooth Speakers": "https://priceoye.pk/bluetooth-speakers?page=",
    "Tablets": "https://priceoye.pk/tablets?page=",
    "Laptops": "https://priceoye.pk/laptops?page="
}

# Function to scrape data from PriceOye
def scrape_data(url, pages):
    products = []
    for page in range(pages):
        full_url = f"{url}{page+1}"
        response = requests.get(full_url)
        html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")

        for i in soup.find_all("div", class_="productBox b-productBox"):
            original_price = None
            discount_percent = None
            name = None
            discounted_price = None
            link = i.find("a", class_="")["href"]

            for item in i.find_all("div", class_="detail-box"):
                name = item.find("div", class_="p-title bold h5").get_text(strip=True)
                discounted_price = item.find("div", class_="price-box p1").get_text(strip=True)

                price_diff = item.find_all("div", class_="price-diff")
                if price_diff:
                    original_price = item.find("div", class_="price-diff-retail").get_text(strip=True)
                    discount_percent = item.find("div", class_="price-diff-saving").get_text(strip=True)

            context = {
                "Name": name,
                "Discounted Price": discounted_price,
                "Original Price": original_price,
                "Discount Percent": discount_percent,
                "Product Link": "https://priceoye.pk" + link
            }

            products.append(context)

    return products

# Streamlit UI
st.title("PriceOye Product Data Scraper By Muhammad Abrar")

# Select category from the dropdown
category = st.selectbox("Select Product Category", list(categories.keys()))

# Input number of pages to scrape
pages = st.number_input("Enter number of pages to scrape:", min_value=1, max_value=100, value=1)

# Scrape button
if st.button("Scrape Data"):
    st.write(f"Scraping {pages} pages of {category} data from PriceOye...")
    show_link=categories[category].split("?")
    st.write(f"Your can confirm scraping data form the following link\n{show_link[0]}")
    url = categories[category]
    data = scrape_data(url, pages)

    if data:
        # Display heading and DataFrame
        st.header(f"{pages} Pages of {category} Data from PriceOye")
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.warning("No data found, please try again later.")
