import httpx
import json
import csv
import mysql.connector


base_url = 'https://bama.ir/cad/api/search?seller=1&pageIndex='

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://example.com"
}

response = httpx.get(base_url + '1', headers=headers)

data = json.loads(response.text)

ads = data['data']['ads']
cars = []

for ad in ads:
    cars.append({
        'brand' : ad['detail']['title'],
        'mileage' : ad['detail']['mileage'],
        'year' : ad['detail']['year'],
        'city' : ad['detail']['location'],
        'price' : ad['price']['price']
    })

sql = mysql.connector.connect(user='root', password='3365',host='127.0.0.1', database='cars', charset='utf8')
cursor=sql.cursor()
for car in cars:
    cursor.execute('''insert into details (brand,mileage,year,city,price)
                    values(%s,%s,%s,%s,%s)'''
                   ,(car['brand'],car['mileage'],car['year'],car['city'],car['price']))
    
sql.commit()
sql.close()