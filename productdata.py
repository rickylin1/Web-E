# productdata.py
from bs4 import BeautifulSoup
import requests

def get_product_details(product_url):
    try:
        # Fetch HTML content from the product URL
        response = requests.get(product_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        html_content = response.text
        
        # Create a BeautifulSoup object
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract product name
        product_name = soup.find('h1', {'automation-id': 'productName'}).text.strip()
        
        # Extract product price
        product_price = soup.find('span', {'class': 'value', 'automation-id': 'productPriceOutput'}).text.strip()
        
        return {'name': product_name, 'price': product_price}
    except Exception as e:
        print(f"Error occurred while extracting details for {product_url}: {e}")
        return None
