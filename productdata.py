from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

#Given a product URL, extract product details such as name, brand, price, category, model, and description.
#returns a dict
def get_product_details(driver, url):

    product_details = {}

    try:
        driver.get(url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
        # Create subpage soup
        subpage_soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            product_details['name'] = subpage_soup.find('h1', {'automation-id': 'productName'}).text.strip()
        except AttributeError:
            product_details['name'] = None

        try:
            product_details['brand'] = subpage_soup.find('div', attrs={'itemprop': 'brand'}).text.strip()
        except AttributeError:
            product_details['brand'] = None

        try:
            div_element = subpage_soup.find('div', {'id': 'pull-right-price', 'class': 'pull-right'})

            # Find the span element with the class "value" inside the div element
            span_element = div_element.find('span', class_='value')
            product_details['price'] = span_element.text.strip()
        except AttributeError:
            product_details['price'] = None

        try:
            nav_element = subpage_soup.find('nav', attrs={'aria-label': 'Breadcrumb'})
            if nav_element:
                anchor_element = nav_element.find('a', recursive=False)  # Stop searching at first level
                if anchor_element:
                    product_details['category'] = anchor_element.text.strip()
        except AttributeError:
            product_details['category'] = None

        try:
            features = []
            ul_element = subpage_soup.find('ul', {'class': 'pdp-features'})
            if ul_element:
                li_elements = ul_element.find_all('li')
                for li in li_elements:
                    features.append(li.text.strip())
            product_details['features'] = features
        except AttributeError:
            product_details['features'] = None

        try:
            product_details['item_number'] = subpage_soup.find('div', {'id': 'product-body-item-number'}).text.strip()
        except AttributeError:
            product_details['item_number'] = None
            
        try:
            product_details['model_number'] = subpage_soup.find('div', {'id': 'product-body-model-number'}).text.strip()
        except AttributeError:
            product_details['model_number'] = None

    except Exception as e:
        print("Error fetching {}: {}".format(url, e))
        product_details = {key: None for key in ['name', 'brand', 'price', 'category', 'features', 'item_number','model_number']}

    return product_details

#Given a list of product URLs, extract details for each product.
#returns list of dict
def extract_product_details(driver, urls):

    products = []
    for url in urls:
        product_details = get_product_details(driver, url)
        products.append(product_details)
    return products


def homepage_get_all_categories(driver,url):
    categories = []
    try:
        driver.get(url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        menu_elements = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "menu"))
        )

        menu_element = menu_elements[0]
        try:
            driver.execute_script("document.getElementById('shop-mt-mobile').click();")
            print("Clicked on the 'Shop' anchor successfully.")
        except TimeoutException:
            print("Timeout waiting for 'Shop' anchor in a menu element.")
        

        submenu = WebDriverWait(driver, 5).until(
              EC.element_to_be_clickable((By.ID, "navigation-v2-category-container")))

        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, 'level1-all-departments'))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        div = soup.find('div', {'id': 'level1-all-departments'})
        anchors = div.find_all('a')

        hrefs = [a['href'] for a in anchors]

        for href in hrefs:
            categories.append("https://www.costco.com" + href)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    print(categories)
    return categories

   

