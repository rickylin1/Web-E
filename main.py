from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import productdata

def subpage_subcategory_links(soup):
    category_link = []
    for div in soup.find_all('div', attrs={"class": "eco-ftr"}):
        for links in div.find_all('a', class_ = "external"):
            category_link.append(links['href'])
    return category_link

def product_links(subpage_categories):
    product_urls = []
    for link in subpage_categories:
        full_url = "https://www.costco.com" + link
        driver.get(full_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        content = BeautifulSoup(driver.page_source, 'html.parser')
        for product_section in content.find_all('div', {'automation-id': 'productList'}):
            for product_link in product_section.find_all('a'):
                product_urls.append(product_link['href'])
    product_urls = list(set(product_urls))
    valid_urls = [url for url in product_urls if url.endswith('.html')]
    print(valid_urls)
    return valid_urls


# Set up Selenium WebDriver
driver = webdriver.Chrome()
url = 'https://www.costco.com/electronics.html'
driver.get(url)

# List to store extracted URLs
url_links = []

try:
    # Wait for parent elements to load
    parent_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".col-xs-4.col-md-2.eco-ftr"))
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
            print(product_links(subpage_subcategory_links(subpage_soup)))
            # Do something with subpage_soup
            # For example, print the title
            print(subpage_soup.title.text)

        finally:
            # Go back to the previous page
            driver.back()
            # Wait for the page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
    # Wait for 3 seconds (optional)
    time.sleep(3)

finally:
    # Quit the WebDriver
    driver.quit()

# Now you have the URLs extracted and stored in url_links list
print(url_links)
