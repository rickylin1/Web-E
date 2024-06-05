from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Assuming 'driver' is your initialized Selenium WebDriver instance
#returns a dict
def get_product_details(driver, url):
    """
    Given a product URL, extract product details such as name, brand, price, category, model, and description.
    """
    product_details = {}

    try:
        driver.get(url)
        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
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

            # Find the span element with the class "value" inside the div elementcl
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
        # Handle exceptions
        print("Error fetching {}: {}".format(url, e))
        product_details = {key: None for key in ['name', 'brand', 'price', 'category', 'features', 'item_number','model_number']}

    for key, value in product_details.items():
        print(f"{key}: {value}")
    return product_details

#returns list of dict
def extract_product_details(driver, urls):
    """
    Given a list of product URLs, extract details for each product.
    """
    products = []
    counter = 0
    for url in urls:
        print('enter' + str(counter))
        product_details = get_product_details(driver, url)
        print('added')
        counter +=1
        products.append(product_details)
    return products

# Assuming driver is already initialized and url_links is your list of URLs
# extracted_products = extract_product_details(driver, url_links)
