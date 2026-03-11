import urllib.request
from bs4 import BeautifulSoup
import json

url = "https://www.numbeo.com/cost-of-living/rankings.jsp"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', id='t2')
    cities = []
    if table:
        for row in table.find('tbody').find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 7:
                city_name = cols[1].text.strip()
                col_index = float(cols[2].text.strip())
                rent_index = float(cols[3].text.strip())
                col_plus_rent = float(cols[4].text.strip())
                groceries = float(cols[5].text.strip())
                restaurant = float(cols[6].text.strip())
                local_purchasing = float(cols[7].text.strip())
                cities.append({
                    'city': city_name,
                    'col_index': col_index,
                    'rent_index': rent_index,
                    'col_plus_rent': col_plus_rent,
                    'groceries': groceries,
                    'restaurant': restaurant,
                    'local_purchasing': local_purchasing
                })

    print(json.dumps(cities[:35], indent=2))
except Exception as e:
    print(f"Error: {e}")
