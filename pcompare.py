import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests

# Setup for Selenium (Flipkart)
chromedriver_path = r'E:\Project\chromedriver-win64\chromedriver-win64\chromedriver.exe'  # Correct path to the .exe file
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Headers for BeautifulSoup (Amazon)
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

# Function to fetch price from Flipkart using Selenium
def flipkart(name):
    try:
        name1 = name.replace(" ","+")
        flipkart=f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        
        # Open Flipkart with Selenium
        driver.get(flipkart)
        driver.implicitly_wait(5)  # Wait for the page to load
        
        price_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a/div[2]/div[2]/div[1]/div[1]/div")
        flipkart_price = price_element.text.strip()
        return flipkart_price
    except:
        return 'No price found on Flipkart'

# Function to fetch price from Amazon using BeautifulSoup
def amazon(name):
    try:
        name1 = name.replace(" ","-")
        name2 = name.replace(" ","+")
        amazon=f'https://www.amazon.in/{name1}/s?k={name2}'
        res = requests.get(f'https://www.amazon.in/{name1}/s?k={name2}', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        for i in range(len(amazon_page)):
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
            if name.upper() in amazon_name:
                amazon_price = soup.select('.a-price-whole')[i].getText().strip()
                return amazon_price
        return 'No price found on Amazon'
    except:
        return 'No price found on Amazon'

# Function to convert price from string to integer
def convert(a):
    b = a.replace(" ", '')
    c = b.replace("INR", '')
    d = c.replace(",", '')
    f = d.replace("₹", '')
    g = int(float(f))
    return g

# Streamlit UI setup
st.title("Product Price Comparison")
st.write("Enter the product name to compare prices between Flipkart and Amazon:")

# Input box for product name
product_name = st.text_input("Product Name:")

if product_name:
    # Fetch prices
    flipkart_price = flipkart(product_name)
    amazon_price = amazon(product_name)
    
    # Convert prices to integers for comparison
    flipkart_price = convert(flipkart_price) if flipkart_price != 'No price found on Flipkart' else 0
    amazon_price = convert(amazon_price) if amazon_price != 'No price found on Amazon' else 0

    # Display results
    st.subheader(f"Prices for {product_name}:")

    if flipkart_price > 0:
        st.write(f"**Flipkart Price:** ₹{flipkart_price}")
    else:
        st.write("**Flipkart:** No product found!")

    if amazon_price > 0:
        st.write(f"**Amazon Price:** ₹{amazon_price}")
    else:
        st.write("**Amazon:** No product found!")

    if flipkart_price > 0 and amazon_price > 0:
        min_price = min(flipkart_price, amazon_price)
        st.subheader(f"Minimum Price: ₹{min_price}")

        if min_price == flipkart_price:
            st.write(f"**Flipkart URL:** [Click here to buy](https://www.flipkart.com/search?q={product_name.replace(' ', '+')})")
        else:
            st.write(f"**Amazon URL:** [Click here to buy](https://www.amazon.in/{product_name.replace(' ', '-')}/s?k={product_name.replace(' ', '+')})")

    else:
        st.write("**No relevant products found in both Flipkart and Amazon.**")

# Close the Selenium WebDriver
driver.quit()
