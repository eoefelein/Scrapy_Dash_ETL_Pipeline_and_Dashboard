# SELENIUM IMPORTS
from selenium import webdriver  # import allows for browser initialization
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import (
    WebDriverWait,
)  # allows for wait period while web page loads
from selenium.webdriver.common.by import (
    By,
)  # import allows for implementation of specfic search params
from selenium.webdriver.support import (
    expected_conditions as EC,
)  # allows for specification of whether desired web element has been loaded
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import lxml
import os

# DATA CLEANING IMPORTS
import pandas as pd
import re

# READ DATA TO POSTGRES DB
from sqlalchemy import create_engine, MetaData, Table
import psycopg2

# specify Firefox driver location
driver_location = "C:/Users/oefel/Downloads/geckodriver-v0.26.0-win64"
os.environ["webdriver.firefox.driver"] = driver_location

driver = webdriver.Firefox(driver_location)  # create new instance of Firefox
driver.implicitly_wait(10)  # wait 10 seconds for page to load
driver.maximize_window()  # maximize the window

# create lists to capture scraped data
tiny_house_titles = []
tiny_bed_bath_area = []
tiny_property_type = []
tiny_house_price = []

page_count = 1
next_page = True

while next_page:
    driver.get(  # pass desired web url
        "https://www.tinyhomebuilders.com/tiny-house-marketplace/search?page={}".format(
            page_count
        )
    )
    # scrape tiny house titles
    scraped_titles = driver.find_elements_by_css_selector(
        "div.card-body > h3.card-title"
    )
    for title in scraped_titles: # strip and store to tiny_house_titles
        tiny_house_titles.append(title.text.strip())

    # scrape tiny house prices
    scraped_price = driver.find_elements_by_css_selector("div.card-body > div.price")
    for price in scraped_price: # strip and store to tiny_house_price
        tiny_house_price.append(price.text.strip())

    # scrape tiny house bed_bath_area
    scraped_bed_bath_size = driver.find_elements_by_css_selector(
        "div.card-body > div.beds_baths_sqft > span"
    )
    for size in scraped_bed_bath_size: # strip and store to tiny_bed_bath_area
        tiny_bed_bath_area.append(size.text.strip())
    
    # scrape tiny house property_type
    scraped_property_type = driver.find_elements_by_css_selector(
        "div.card-body > div.propertyType"
    )
    for property_type in scraped_property_type: # strip and store to tiny_property_type
        tiny_property_type.append(property_type.text.strip())

    if len(driver.find_elements_by_link_text(str(page_count+1))) > 0:
        driver.find_element_by_link_text(str(page_count+1)).click() # find the next page
        page_count += 1 # increment the page
    else:
        next_page = False

driver.close()

# create bedroom, bathroom and area lists from scraped tiny_bed_bath_area
tiny_bed_bath = tiny_bed_bath_area[::2]  # split to bed & bath and area

tiny_bedrooms = [bed_bath.split(',')[0] for bed_bath in tiny_bed_bath] # split to bedroom list
tiny_bathrooms = [bed_bath.split(',')[1] for bed_bath in tiny_bed_bath] # split to bathroom list
tiny_area = tiny_bed_bath_area[
    1::2
]  # read every other element and skip the first element to create area list
clean_tiny_area = [re.sub('\D', '', area) for area in tiny_area] # remove all but digits from area list

# create property_type, city & state lists from scraped tiny_property_type
clean_property_type = [property_type.split(' in ')[0] for property_type in tiny_property_type]

clean_city_state = [property_type.split(' in ')[1] for property_type in tiny_property_type]
clean_city = [city_state.split(',')[0] for city_state in clean_city_state] # split to city list
clean_state = [city_state.split(',')[1] for city_state in clean_city_state] # split to state list

tiny_house_marketplace = pd.DataFrame( # create tiny_house_marketplace dataframe
    list(
        zip(
            tiny_house_titles,
            clean_property_type,
            tiny_bedrooms,
            tiny_bathrooms,
            clean_tiny_area,
            clean_city,
            clean_state,
            tiny_house_price,
        )
    ),
    columns=["title", "property_type", "bedrooms", "bathrooms", "area", "city", "state", "price"],
)

# connect to postgres tiny_house db with sqlalchemy
engine = create_engine("postgresql+psycopg2://postgres:UTData20$@localhost:5432/tiny_house")
tiny_house_marketplace.to_sql('tiny_house_marketplace', con=engine, if_exists='append') # read to SQL DB
engine.execute("SELECT * FROM tiny_house_marketplace").fetchall() # verify data has been loaded successfully
