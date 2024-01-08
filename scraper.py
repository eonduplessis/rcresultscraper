import requests
import re
from bs4 import BeautifulSoup

BASE_URL = 'https://www.rc-results.com'

RACE_URL = '/Viewer/Main/MeetingSummary?meetingId=10354'

URL = BASE_URL + RACE_URL
page = requests.get(URL, verify=False)

soup = BeautifulSoup(page.content, "html.parser")

race = soup.find('h3').text

links = soup.find_all('a', href=True)

pattern = re.compile("^Race ")

event_links = []



def write_to_file(result):
    with open('results.csv', 'a') as file:
       file.writelines(result + '\n')

for link in links:
  print("Link:", link.get("href"), "Text:", link.string)

  if pattern.match(link.string):
    event_links.append(link.get("href"))

for event in event_links:
  event_page = requests.get(BASE_URL + event, verify=False)
  event_soup = BeautifulSoup(event_page.content, 'html.parser')

  print(event_soup.title.string)

  table = event_soup.find('table', {'class': 'table table-bordered table-responsive table-hover table-fit table-nowrap'})
  
  rows = table.findAll('tr')

  driver_event_result_links = []
  
  for tr in rows:
    cols = tr.findAll('td')
    
    if len(cols) >= 6:
        link = cols[2].find('a').get('href')
        driver_event_result_links.append(link)
    
  for driver_results in driver_event_result_links:
    driver_result_page = requests.get(BASE_URL + driver_results, verify=False)
    driver_result_soup = BeautifulSoup(driver_result_page.content, 'html.parser')

    print(driver_result_soup.title.string)

    headers = driver_result_soup.find_all('h3')

    table_driver_details = driver_result_soup.find('table', {'class':'table table-condensed table-responsive table-hover table-fit table-nowrap'})

    table_lap_times = driver_result_soup.find('table', {'class':'table table-ultra-condensed table-responsive table-hover table-fit table-nowrap'})
    print('done')

    driver_details_tr = table_driver_details.findAll('tr')
    for tr in driver_details_tr:
       columns = tr.findAll('td')
       
       if columns[0].text == 'Driver ':
          driver_name = columns[1].text
    
    driver_lap_times_tr = table_lap_times.findAll('tr')

    driver_lap_times = []
    for tr in driver_lap_times_tr[1:]:
       columns = tr.findAll('td')
       driver_lap_times.append(columns[1].text)




    for lap in driver_lap_times:
       result = race + ',' + headers[0].string + ',' + headers[1].string + ',' + driver_name + ',' + lap
       write_to_file(result)