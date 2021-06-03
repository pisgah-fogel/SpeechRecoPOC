#!/usr/bin/env python3

try:
    import constants
except ModuleNotFoundError:
    print("ERROR: A file named 'constants.py' cannot be found.")
    exit(1)

try:
    import requests
except ModuleNotFoundError:
    print("ERROR: Your need 'requests' for this script to work.")
    print("Use: python3 -m pip install requests")
    exit(1)
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print("ERROR: Your need 'beatifulsoup' for this script to work.")
    print("Use: python3 -m pip install beautifulsoup4")
    exit(1)


if constants.DEBUG:
    with open(constants.DEBUG_HTML_FILE) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
else:
    vgm_url = constants.CLEAROUTSIDE_URL
    try:
        html_text = requests.get(vgm_url).text
    except ConnectionError:
        print("Unable resolve clearoutside.com")
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

# Going through the datas and print the forecast
# Example: 3 hours of rain this morning, at 9, 11 and 12 o clock, with an average temperature of 7 degrees. ... afternoon, ... 5 hours to watch the stars.

# Morning forecast
index = 0
count_rain = 0
count_sun = 0
count_temp = 0
sum_temp = 0
while index < len(forecast_array) and forecast_array[index]["hour"] >= sunrise_int and forecast_array[index]["hour"] < 13:
    sum_temp += forecast_array[index]["temperature"]
    count_temp += 1
    if forecast_array[index]["precipitation"] == "None":
        count_sun += 1
    else:
        count_rain += 1
    index += 1
if count_temp != 0:
    avg_temp = sum_temp / count_temp
    print("This morning, ")
    if count_rain == 0:
        print("No rain, ")
    elif count_sun == 0:
        print("Rain, ")
    else:
        print(str(count_sun)+" hours of sun and "+str(count_rain)+" hours of rain, ")
    print("With an average temperature of " + str(avg_temp) + "degrees")

# Afternoon
count_rain = 0
count_sun = 0
count_temp = 0
sum_temp = 0
while index < len(forecast_array) and forecast_array[index]["hour"] <= sunset_int:
    sum_temp += forecast_array[index]["temperature"]
    count_temp += 1
    if forecast_array[index]["precipitation"] == "None":
        count_sun += 1
    else:
        count_rain += 1
    index += 1
if count_temp != 0:
    avg_temp = sum_temp / count_temp
    print("This afternoon, ")
    if count_rain == 0:
        print("No rain, ")
    elif count_sun == 0:
        print("Rain, ")
    else:
        print(str(count_sun)+" hours of sun and "+str(count_rain)+" hours of rain, ")
    print("With an average temperature of " + str(avg_temp) + "degrees")

# Night
count_temp = 0
sum_temp = 0
count_good = 0
while index < len(forecast_array) and (forecast_array[index]["hour"] > sunset_int or forecast_array[index]["hour"] < sunrise_int):
    sum_temp += forecast_array[index]["temperature"]
    count_temp += 1
    if forecast_array[index]["condition"] == "Good": # or forecast_array[index]["total_cloud"] < 20
        count_good += 1
    index += 1
if count_temp != 0:
    avg_temp = sum_temp / count_temp
    print("This night, ")
    if count_good == 0:
        print("Nothing to see.")
    elif count_good == count_temp:
        print("No cloud, you have to look at the sky.")
    else:
        print(str(count_good)+" over "+str(count_temp)+" hours without clouds")
    print("With an average temperature of " + str(avg_temp) + "degrees")

# Tomorrow Morning
index = 0
count_rain = 0
count_sun = 0
count_temp = 0
sum_temp = 0
while index < len(forecast_array) and forecast_array[index]["hour"] >= sunrise_int and forecast_array[index]["hour"] < 13:
    sum_temp += forecast_array[index]["temperature"]
    count_temp += 1
    if forecast_array[index]["precipitation"] == "None":
        count_sun += 1
    else:
        count_rain += 1
    index += 1
if count_temp != 0:
    avg_temp = sum_temp / count_temp
    print("Tomorrow morning, ")
    if count_rain == 0:
        print("No rain, ")
    elif count_sun == 0:
        print("Rain, ")
    else:
        print(str(count_sun)+" hours of sun and "+str(count_rain)+" hours of rain, ")
    print("With an average temperature of " + str(avg_temp) + "degrees")

# Tomorrow Afternoon
count_rain = 0
count_sun = 0
count_temp = 0
sum_temp = 0
while index < len(forecast_array) and forecast_array[index]["hour"] < sunset_int:
    sum_temp += forecast_array[index]["temperature"]
    count_temp += 1
    if forecast_array[index]["precipitation"] == "None":
        count_sun += 1
    else:
        count_rain += 1
    index += 1
if count_temp != 0:
    avg_temp = sum_temp / count_temp
    print("Tomorrow afternoon, ")
    if count_rain == 0:
        print("No rain, ")
    elif count_sun == 0:
        print("Rain, ")
    else:
        print(str(count_sun)+" hours of sun and "+str(count_rain)+" hours of rain, ")
    print("With an average temperature of " + str(avg_temp) + "degrees")

# Tomorrow Night
count_temp = 0
sum_temp = 0
count_good = 0
while index < len(forecast_array) and (forecast_array[index]["hour"] > sunset_int or forecast_array[index]["hour"] < sunrise_int):
    sum_temp += forecast_array[index]["temperature"]
    count_temp += 1
    if forecast_array[index]["condition"] == "Good": # or forecast_array[index]["total_cloud"] < 20
        count_good += 1
    index += 1
if count_temp != 0:
    avg_temp = sum_temp / count_temp
    print("Tomorrow night, ")
    if count_good == 0:
        print("Nothing to see.")
    elif count_good == count_temp:
        print("No cloud, you have to look at the sky.")
    else:
        print(str(count_good)+" over "+str(count_temp)+" hours without clouds")
    print("With an average temperature of " + str(avg_temp) + "degrees")