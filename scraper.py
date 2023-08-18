import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
# import csv

URL = 'https://mad.firstmark.com/card'

DATA_DICT = {}

# PART 1: SCRAPE
response = requests.get(URL)

if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'html.parser')

    categories_selector = "div#__next > main > div > ul > li > h2"
    category_elements = soup.select(categories_selector)
    
    for category_element in category_elements:

        # get category
        category = category_element.get_text().strip()

        subcategory_list = category_element.find_next_siblings('ul')[0]
        h3_elements = subcategory_list.find_all_next('h3')

        for h3_element in h3_elements:

            # get subcategory
            subcategory = h3_element.get_text().strip()

            # get card
            card_list = h3_element.find_next_siblings('ul')[0]
            card_elements = card_list.find_all_next('li')

            for card_element in card_elements:
                
                name = card_element.find('h2').get_text().strip()
                url = card_element.find('a').get('href').strip()
                description = card_element.find('p').get_text().strip()

                # year_selector = 'div:nth-child(2) > span:nth-child(1)'
                # year_text = card_element.select_one(year_selector).get_text().strip()
                # founding_year = re.search(r'(\d{4})', year_span).group(1)

                # TODO: fix funding selector
                # total_funding_text = ''
                
                # funding_selector = 'div:nth-child(2) > span:nth-child(2)'
                # total_funding_text = card_element.select_one(funding_selector).get_text().strip()
                # if re.search(r'^Total Funding', total_funding_text)
                #     total_funding = total_funding_text

                # span_elements = card_element.find_all_next('span')
                # span_text = [span_element.get_text() for span_element in span_elements]

                DATA_DICT[name] = {
                    'category': category,
                    'subcategory': subcategory,
                    'name': name,
                    'url': url,
                    'description': description,
                    # 'founding_year': founding_year,
                    # 'total_funding': total_funding
                }

                # print (f"{name} founded {founding_year} funding: {total_funding}")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

# PART 2: Write out to csv

# Option 1: Pandas Dataframes

# Create lists to hold the data for each column
subcategories = []
categories = []
names = []
urls = []
descriptions = []
# founding_years = []
# total_fundings = []

# Loop over the data dictionary
for _, item in DATA_DICT.items():
    names.append(item['name'])
    urls.append(item['url'])
    descriptions.append(item['description'])
    categories.append(item['category']),
    subcategories.append(item['subcategory']),
    # founding_years.append(item['founding_year'])
    # total_fundings.append(item['total_funding'])

# Create a Pandas DataFrame
df = pd.DataFrame({
    'Category': categories,
    'Subcategory': subcategories,
    'Name': names,
    'URL': urls,
    # 'Founding Year': founding_years,
    # 'Total Funding': total_fundings,
    'Description': descriptions,
})

# Write the DataFrame to a CSV file
csv_filename = 'output.csv'

# UNCOMMENT THIS LINE TO WRITE DF OUT TO CSV
df.to_csv(csv_filename) 
# print(f'Data written to {csv_filename}')

# UNCOMMENT THIS SECTION TO WRITE DATA_DICT DIRECTLY TO CSV W/O PD.DF 

# # Option 2: python csv library

# csv_filename = 'output.csv'

# # Open the CSV file in write mode
# with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
#     # Create a CSV writer
#     csv_writer = csv.writer(csv_file)

#     # Write the header row
#     csv_writer.writerow(['Key', 'Name', 'URL', 'Description'])

#     # Write data from the data dictionary
#     for _, item in data.items():
#         row = [key, item['name'], item['url'], item['description']]
#         csv_writer.writerow(row)

 

