#!/usr/bin/env python3

#pip3 install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

vgm_url = 'https://clearoutside.com/forecast/48.68/8.90'
try:
    html_text = requests.get(vgm_url).text
except ConnectionError:
    print("Unable resolve clear outside.com")
    exit(1)

soup = BeautifulSoup(html_text, 'html.parser')

forecast = soup.find('div', attrs = {'class': 'fc', 'id': 'forecast'})

if not forecast:
    print("Unable to fetch forecast from clear outside.com")
    exit(1)

hours = forecast.find('div', attrs = {'class': 'fc_hours fc_hour_ratings'})
ul = hours.find('ul')

forecast_array = []
for hour in ul.find_all('li'):
    condition = hour.contents[2].text # Bad OK Good
    h = hour.contents[1].strip() # 19
    forecast_array.append({"hour": int(h), "condition" : condition})

details = forecast.find('div', attrs = {'class': 'fc_detail hidden-xs'})
rows = details.find_all('div', attrs = {'class': 'fc_detail_row'})

total_cloud = rows[0]
counter = 0
for column in total_cloud.div.find_all('li'):
    forecast_array[counter]['total_cloud'] = int(column.contents[0])
    counter += 1

precipitation = rows[7]
counter = 0
for column in precipitation.div.find_all('li'):
    forecast_array[counter]['precipitation'] = column.contents[0].text
    counter += 1

temperature = rows[12]
counter = 0
for column in temperature.div.find_all('li'):
    forecast_array[counter]['temperature'] = int(column.contents[0])
    counter += 1

daylight = forecast.find('div', attrs = {'class': 'fc_daylight'}).contents[1].text #'Sun - Rise: 06:32, Set: 20:14, Transit: 13:24.  Moon - Rise: 08:09, Set: 22:48. Civil Dark: 20:47 - 05:59. Nautical Dark: 21:28 - 05:18. Astro Dark: 22:12 - 04:33'
sunrise = daylight[daylight.find("Rise: ")+6:daylight.find(",")] # 06:32
sunset = daylight[daylight.find("Set: ")+5:daylight.find(", Tra")] # 20:14

sunrise_split = sunrise.split(":")
sunrise_int = int(sunrise_split[0]) + int(sunrise_split[1])/60

sunset_split = sunset.split(":")
sunset_int = int(sunset_split[0]) + int(sunset_split[1])/60

print("Sunrise: "+sunrise+" "+str(sunrise_int))
print("Sunset: "+sunset+" "+str(sunset_int))

for item in forecast_array:
    print(str(item["hour"])+"h => "+item["condition"]+" "+str(item["total_cloud"])+"% clouds "+str(item["temperature"])+"° == "+item['precipitation'])

day_avg_temp_morning = 0
day_avg_temp_morning_cnt = 0
day_avg_temp_afternoon = 0
day_avg_temp_afternoon_cnt = 0
for hour in forecast_array:
    if hour["hour"] < sunrise_int or hour["hour"] > sunset_int:
        # It is night time
    else:
        # It is daytime
        if hour["hour"] < 13:
            day_avg_temp_morning = hour["temperature"]
            day_avg_temp_morning_cnt += 1
        else:
            day_avg_temp_morning = hour["temperature"]
            day_avg_temp_morning_cnt += 1