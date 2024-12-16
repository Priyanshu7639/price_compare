from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

chromedriver_path = r'E:\Project\chromedriver-win64\chromedriver-win64\chromedriver.exe'  # Correct path to the .exe file
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

flipkart = ''
amazon = ''

def flipkart(name):
    try:
        global flipkart
        name1 = name.replace(" ","+")
        flipkart=f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        
        driver.get(flipkart)
        driver.implicitly_wait(2)  # Wait for the page to load
        
        print("\nSearching in Flipkart....")
        
        try:
            price_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a/div[2]/div[2]/div[1]/div[1]/div")
            flipkart_price = price_element.text.strip()
            print("Flipkart Price:", flipkart_price)
            return flipkart_price
        except:
            print("Flipkart: No price found!")
            return '0'
    except:
        print("Flipkart: No product found!")
        return '0'

# Fetch price from Amazon using BeautifulSoup
def amazon(name):
    try:
        global amazon
        name1 = name.replace(" ","-")
        name2 = name.replace(" ","+")
        amazon=f'https://www.amazon.in/{name1}/s?k={name2}'
        res = requests.get(f'https://www.amazon.in/{name1}/s?k={name2}', headers=headers)
        print("\nSearching in Amazon...")
        soup = BeautifulSoup(res.text, 'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        amazon_page_length = len(amazon_page)
        
        for i in range(amazon_page_length):
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
            if name.upper() in amazon_name:
                amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip()
                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
                print("Amazon Price: ₹", amazon_price)
                return amazon_price
        print("Amazon: No product found!")
        return '0'
    except:
        print("Amazon: No product found!")
        return '0'

# Function to convert price from string to integer
def convert(a):
    b = a.replace(" ", '')
    c = b.replace("INR", '')
    d = c.replace(",", '')
    f = d.replace("₹", '')
    g = int(float(f))
    return g

# Input product name
name = input("Product Name:\n")
flipkart_price = flipkart(name)
amazon_price = amazon(name)

# Convert the price for comparison
if flipkart_price == '0':
    print("Flipkart: No product found!")
    flipkart_price = 0
else:
    flipkart_price = convert(flipkart_price)

if amazon_price == '0':
    print("Amazon: No product found!")
    amazon_price = 0
else:
    amazon_price = convert(amazon_price)

# Compare the prices
lst = [flipkart_price, amazon_price]
lst2 = [price for price in lst if price > 0]

if len(lst2) == 0:
    print("No relative product found in all websites....")
else:
    min_price = min(lst2)
    print("\nMinimum Price: ₹", min_price)

    price = {
        f'{amazon_price}': f'{amazon}',
        f'{flipkart_price}': f'{flipkart}',
    }
    
    for key, value in price.items():
        if int(key) == min_price:
            print('URL:', value, '\n')

    print("---------------------------------------------------------URLs--------------------------------------------------------------")
    print("Flipkart : \n", flipkart)
    print("\nAmazon : \n", amazon)
    print("---------------------------------------------------------------------------------------------------------------------------")

# Close the Selenium WebDriver
driver.quit()
