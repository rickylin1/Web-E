from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import productdata
import urllib.parse
import pandas as pd

def is_absolute(url):
    return bool(urllib.parse.urlparse(url).netloc)

def subpage_subcategory_links(soup):
    category_link = []
    for div in soup.find_all('div', attrs={"class": "eco-ftr"}):
        for links in div.find_all('a', class_ = "external"):
            category_link.append(links['href'])
    return category_link

def product_links(subpage_categories):
    product_urls = []
    if not subpage_categories:  # If subpage_categories is empty, extract product links from product image holders
        content = BeautifulSoup(driver.page_source, 'html.parser')
        for product_link in content.find_all('a', class_='product-image-url'):
            product_urls.append(product_link['href'])
            product_url = product_link['href']
    else:     
        for link in subpage_categories:
            if not is_absolute(link):
                full_url = "https://www.costco.com" + link
            else:
                full_url = link
            print('line 28 main.py' + full_url)
            driver.get(full_url)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            content = BeautifulSoup(driver.page_source, 'html.parser')
            for product_section in content.find_all('div', {'automation-id': 'productList'}):
                for product_link in product_section.find_all('a'):
                    product_urls.append(product_link['href'])
                    product_url = product_link['href']
    #this should remove duplicates by first converting to a set, then making it a list 
    product_urls = list(set(product_urls))
    valid_urls = [url for url in product_urls if url.endswith('.html')]
    product_details = productdata.extract_product_details(driver,valid_urls)
    df = pd.DataFrame(product_details)
    df.to_csv('costco_data.csv', index=False, mode='a', header=False)


    return valid_urls



# Set up Selenium WebDriver
driver = webdriver.Chrome()
url = "https://www.costco.com"

driver.get(url)

#list of dicts
product_details = []

all_categories = productdata.homepage_get_all_categories(driver,url)

for category_url in all_categories:
        url_links = []
        print(category_url + " is being processed")
        driver.get(category_url)
        parent_elements = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".eco-ftr"))
        )

        # Extract URLs using Beautiful Soup
        for parent in parent_elements:
            # Parse HTML content of the parent element
            soup = BeautifulSoup(parent.get_attribute('innerHTML'), 'html.parser')
            # Find the child element within the parsed HTML
            child_element = soup.find('a', class_='external')
            if child_element:
                # Get the href attribute value
                link = child_element['href']
                url_links.append(link)

        print("the first of link of  " + category_url +  " is " + url_links[0])

        # img_elements = WebDriverWait(driver, 10).until(
        # EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.img-responsive.btn-block"))
        # )
        
        print("url links is")
        print(url_links)
            
        # Loop through each link and click
        for link in url_links:
            try:
                full_url = "https://www.costco.com" + link
                print('line 91 main.py' + full_url)
                driver.get(full_url)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                subpage_soup = BeautifulSoup(driver.page_source, 'html.parser')
                product_links(subpage_subcategory_links(subpage_soup))

            finally:
                # Go back to the previous page
                driver.back()
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
        
        url_links.clear()

        time.sleep(3)

