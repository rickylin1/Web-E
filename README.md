Web-E is a webscraper dedicated to finding the cheapest and best deals for you at your most frequented stores! 
Currently deployed for Amazon & Costco
Built w/ Selenium, Beautiful Soup, Pandas

## Features
- Search query for products based on name, price, brand, category, model, description
- Fetch newest deals relevant to your interests
- Help plan future shopping lists

## Challenges
- Number of page redirect requrests potentially can violate TOS and seem like a bot, so ethics is a problem
- Did not upload amazon info, since I don't want to get banned from amazon

## Lessons
- Learned how to use chrome page inspector and DOM console to target elements and information I am interested in
- Using time to make sure elements are loaded in, using try except to catch problems
- Navigating urls and subpage directories

## Future Goals
- More efficient searching and page redirecting
- Work on making data more descriptive, have more attributes for each product object (ex. reviews, company info, instructions)
- Some data extracted can be NAN, may be issue with ID identifying
- Deploy a friendly UI to prompt
