from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import productdata
import pandas as pd

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
            full_url = "https://www.costco.com" + link
            driver.get(full_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            content = BeautifulSoup(driver.page_source, 'html.parser')
            for product_section in content.find_all('div', {'automation-id': 'productList'}):
                for product_link in product_section.find_all('a'):
                    product_urls.append(product_link['href'])
                    product_url = product_link['href']
    #this should remove duplicates by first converting to a set, then making it a list 
    product_urls = list(set(product_urls))
    valid_urls = [url for url in product_urls if url.endswith('.html')]
    # print(valid_urls)
    product_details = productdata.extract_product_details(driver,valid_urls)
    df = pd.DataFrame(product_details)
    df.to_csv('costco_data.csv', index=False, mode='a', header=False)
    # print(product_details)


    return valid_urls



# Set up Selenium WebDriver
driver = webdriver.Chrome()
url = "https://www.costco.com"

driver.get(url)

#list of dicts
product_details = []

# List to store extracted URLs
url_links = []

all_categories = productdata.homepage_get_all_categories(driver,url)


    # Wait for parent elements to load
    # parent_elements = WebDriverWait(driver, 10).until(
    #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".col-xs-4.col-md-2.eco-ftr"))
    # )

for category_url in all_categories:
        print(category_url + "is being processed")
        driver.get(category_url)
        parent_elements = WebDriverWait(driver, 10).until(
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

            img_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.img-responsive.btn-block"))
        )

        # for img_element in img_elements:
        #     soup = BeautifulSoup(img_element.get_attribute('innerHTML'), 'html.parser')
        #     # Navigate to the parent's parent of the img element using BeautifulSoup
        #     parent_parent_element = img_element.parent().parent
        #     # Assuming href attribute is in the parent's parent element
        #     href_attribute = parent_parent_element['href']
        #     if href_attribute:
        #         url_links.append(href_attribute)
        
        # Loop through each link and click
        for link in url_links:
            try:
                full_url = "https://www.costco.com/" + link
                # Click on the link
                driver.get(full_url)
                # Wait for the page to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                # Create subpage soup
                subpage_soup = BeautifulSoup(driver.page_source, 'html.parser')
                product_links(subpage_subcategory_links(subpage_soup))

            finally:
                # Go back to the previous page
                driver.back()
                # Wait for the page to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
            
        url_links.clear()
        
        # Wait for 3 seconds (optional)
        time.sleep(3)

