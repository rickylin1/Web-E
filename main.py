import pandas as pd
import time
from lxml import etree as et
from bs4 import BeautifulSoup
from selenium import webdriver
pd.options.mode.chained_assignment = None
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, JavascriptException

def extract_content(url):
    driver.get(url)
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    return soup

def click_url(driver):
        # Wait until the element is present
        parent_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".col-xs-4.col-md-2.eco-ftr")).click()
        )

        html_content = driver.page_source
        subpage_soup = BeautifulSoup(html_content, 'html.parser')
        return subpage_soup


driver = webdriver.Chrome()

url = 'https://www.costco.com/electronics.html'
driver.get(url)

url_links = []


try:
    parent_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".col-xs-4.col-md-2.eco-ftr"))
    )
    for parent in parent_elements:
        child_element = parent.find_element(By.CSS_SELECTOR, "a.external")
        link = child_element.get_attribute('href')
        url_links.append(link)
    
    time.sleep(3)

finally:
    driver.quit()

print(url_links)



# main_page_soup = extract_content(url)

# subpage_content =click_url(driver)

# # # Creating a dictionary with required columns
# data_dic = {'product_url': [], 'item_id': [], 'brand': [], 'product_name': [], 'category': [], 'model': [], 'price': [], 'description': []}

# # # Creating a dataframe
# data = pd.DataFrame(data_dic)

# links = product_links(soup)
# print('links is')
# print(links)


# for product_url in links:
#     print('test')
#     # print(product_url)
#     product_content = extract_content(product_url)

#     # Extract product details using defined functions
#     model = get_model(product_content)
#     brand = get_brand(product_content)
#     price = get_price(product_content)
#     item_id = get_item_id(product_content)
#     category = get_category(product_content)
#     description = get_description(product_content)
#     product_name = get_product_name(product_content)

#     # Append scraped data to DataFrame
#     data = data.append({'product_url': product_url, 'item_id': item_id, 'brand': brand,
#                         'product_name': product_name, 'category': category,
#                         'model': model, 'price': price, 'description': description}, ignore_index=True)
    
# data.to_csv('costco_data.csv')

