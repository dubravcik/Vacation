from bs4 import BeautifulSoup
import json
import requests

def getUrl(country, locality):
    return 'http://last-minute.invia.cz/direct/tour_search/ajax-next-boxes/?nl_country_id%5B%5D='+str(country)+'&nl_locality_id%5B%5D='+str(locality)

text = requests.get('http://last-minute.invia.cz/direct/tour_search/ajax-next-boxes/?nl_country_id%5B%5D=28&nl_locality_id%5B%5D=291&page=9')

body = (json.loads(text.text)).get('boxes_html')
bodySoup = BeautifulSoup(body, 'html.parser')
bodySoup.find_all('li') #data-content-value
#bodySoup.find_all('li', attrs={"class":"item"})
lis = bodySoup.find_all('li', attrs={"class":"item"})
for li in lis:
    hotelId = json.loads(li.get('data-ua')).get('name').split(' ',1)[0]
    print hotelId

