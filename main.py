from prometheus_client import start_http_server, Gauge
import time
from bs4 import BeautifulSoup
from config import Config
import requests
import logging


Config = Config()
logging.basicConfig(level=Config.LOG_LEVEL)
logging.basicConfig(format=Config.LOG_FORMAT)
url=Config.WEATHER_URL

logging.info("URL configured is: " + url)

# Create a Prometheus gauge to track the metric
weatherscraper_temp = Gauge('weatherscraper_temp', 'The scraped temperature value in degrees C')
weatherscraper_dewpoint = Gauge('weatherscraper_dewpoint', 'The scraped dewpoint value in degrees C')
weatherscraper_response_code = Gauge('weatherscraper_response_code', 'Response code from the http server')
weatherscraper_scrape_success = Gauge('weatherscraper_scrape_success', 'did we scrape ok or not')

# Function to scrap website
def getweather(url):
    data={}
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
            logging.error("Error: ", e)
            return data
    else:

        code = response.status_code
        logging.info("HTTP response code: "+ str(code))
        data['response_code'] = code
        if code == 200:
            data['scrape_success']=1
        else:
            data['scrape_success']=0
        
        doc = BeautifulSoup(response.text, "html.parser")
        cells = doc.findAll('td')
        currentweather = str(cells[3])
        currentweather_split = currentweather.split()
        currentweather_split2 = currentweather_split[1].split('>')
        currentweather_split3 = currentweather_split2[2].split('°')
        temperature = float(currentweather_split3[0])

        dewpointCell = str(cells[35])
        dewpointCell_split = dewpointCell.split('>')
        dewpointCell_split1 = dewpointCell_split[2].split('°')
        dewpoint = float(dewpointCell_split1[0])

        logging.info("Temperature is " + str(temperature) + "°C")
        logging.info("Dewpoint is " + str(dewpoint) + "°C")

        data['temperature']=temperature
        data['dewpoint']=dewpoint

    return data


if __name__ == '__main__':
    # Start the Prometheus exporter HTTP server
    start_http_server(8000)
    
   
    while True:
        # Update the metric values
        data = getweather(url)
        
        if len(data) > 0:

            # set output metrics
            weatherscraper_temp.set(data['temperature'])
            weatherscraper_dewpoint.set(data['dewpoint'])
            weatherscraper_response_code.set(data['response_code'])
            weatherscraper_scrape_success.set(data['scrape_success'])
        
        # Wait before updating again
        time.sleep(300)
