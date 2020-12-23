import re, logging, platform, math
import data_cleaning_functions #self made modules only
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO, format=' %(asctime)s -  %(levelname)s -  %(message)s')
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

def get_URL(driver,page):
    #function gets URL based on page number, will wait 30 seconds before closing script
    driver.get('https://www.harristeeter.com/shop/store/378/search/beer?pageNo='+str(page)+'&appliedFilter=,category%253A1298,category%253A628,category%253A1363,category%253A627&appliedSort=Relevance')#opens webpage
    try:
        element = WebDriverWait(driver, 60).until( #wait 30 sec to see if first item on page exists
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/hts-layout/span/hts-search/div/section/div/div[2]/div[2]/ul/hts-product-info[1]/li/span/a[2]/span[2]/span[1]"))
        )
    except TimeoutException:
        logging.error('took longer than 60 seconds to return page, exiting script')
        driver.close()
        quit()
    finally:
        logging.info('Loading page #'+str(page))


def xpath_extractor(x, xpath):
    #function extracts text from webpage based on xpath
    BASE_XPATH = '/html/body/app-root/div/hts-layout/span/hts-search/div/section/div/div[2]/div[2]/ul/hts-product-info['+str(x)+']/li/span/a[2]'
    try:
        OUTPUT = driver.find_element_by_xpath(BASE_XPATH+xpath).text
        return OUTPUT
    except:
        pass


TS_QUERY = str(date.today())
options = webdriver.ChromeOptions()

#options.add_argument('headless') #headless means it will run without popping up a window, no GUI involved
DRIVER_PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

driver = webdriver.Chrome(executable_path=DRIVER_PATH,chrome_options=options)


get_URL(driver,1)#get first URL

title_of_page = driver.title
total_pages = re.findall('Search Results: beer \((.*)\)',title_of_page)[0] #get total results based on title of webpage
number_of_loops = math.ceil(float(total_pages)/20.0)#determine how many times for loops will be executed in for loop


for loop in range(1,int(number_of_loops)+1): #loop through each page
    get_URL(driver,loop)#get next webpage before looping
    for x in range(1,21): #loop through 20 items listed on the page
        PRODUCT_NAME = PRICE = VICS_PRICE = ON_SALE = SIZE = ''
        try:
            PRODUCT_NAME = xpath_extractor(x, '/span[2]/span[1]') #name
            PRICE = xpath_extractor(x, '/span[2]/span[2]/div[1]/span') #price
            VICS_PRICE = xpath_extractor(x, '/span[2]/span[2]/div[2]/span')# vics price
            ON_SALE = xpath_extractor(x, '/span[1]/span')#is it on sale?
            SIZE = xpath_extractor(x, '/span[2]/span[2]/span[1]')#size of pack'

            PRICE = data_cleaning_functions.CLEAN_PRICE(PRICE)
            VICS_PRICE = data_cleaning_functions.CLEAN_VICS_PRICE(VICS_PRICE)
            SIZE = data_cleaning_functions.CLEAN_SIZE(SIZE)

            ROW = [PRODUCT_NAME.encode("utf-8"), PRICE, VICS_PRICE, ON_SALE, SIZE, TS_QUERY] #create row to be written to file, PRODUCT_NAME had issues with ASCII characters
            print(ROW)

        except:
            logging.error(error)
            pass

driver.close()
logging.info('Script Completed')
exit()

#if __name__ == "__main__":
#    main()
