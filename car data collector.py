import httpx
import json
import mysql.connector
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np
from jdatetime import date as jdate
from datetime import date
from sklearn.metrics import r2_score

base_url = 'https://bama.ir/cad/api/search?seller=1&pageIndex='

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://example.com"
}

sql = mysql.connector.connect(user='root', password='3365',host='127.0.0.1', database='cars', charset='utf8')
cursor=sql.cursor()
cursor.execute('''create table if not exists detail(
               id INT AUTO_INCREMENT PRIMARY KEY,
               brand varchar(225),
               model varchar(225),
               mileage varchar(225),
                year int,
               city varchar(225),
               price bigint)''')

for page in range(1,6) :
    print('collecting data from page ',page)
    response = httpx.get(base_url + str(page), headers=headers)

    data = json.loads(response.text)

    ads = data['data']['ads']
    cars = []
    for ad in ads:
        brand_model = ad['detail']['title']
        brand_model = brand_model.split('،')

        brand = brand_model[0]
        model = brand_model[1]
        price = ad['price']['price']
        year = ad['detail']['year'].replace(",", "").replace(" ", "").strip()

        if int(year) > 1800 :
            year = date(int(year), 6, 15)
            shamsi_date = jdate.fromgregorian(date=year)
            year = shamsi_date.year
        else:
            continue

        mileage = ad['detail']['mileage'].replace(",", "").replace(" ", "").replace("km","").strip()
        if mileage == 'صفرکیلومتر':
             mileage = 0
        elif mileage == 'کارکرده':
             mileage = ''
        values = [brand, model, mileage, year, ad['detail']['location'], price]

        invalid = (None, '', '0', 'None', 'NaN')
        if all(v not in invalid and v != None for v in values):
            cars.append({
                'brand' : brand.replace(",", "").replace(" ", "").strip(),
                'model' : model.replace(",", "").replace(" ", "").strip(),
                'mileage' : int(mileage),
                'year' : year,
                'city' : ad['detail']['location'].replace(",", "").replace(" ", "").strip(),
                'price' : int(price.replace(",", "").replace(" ", "").strip())
            })

    for car in cars:
        brand = car['brand']
        model = car['model']
        if brand.isascii():
            brand = brand.lower()
        if model.isascii():
            model = model.lower()
        cursor.execute('''insert into detail (brand,model,mileage,year,city,price)
                        values(%s,%s,%s,%s,%s,%s)'''
                       ,(brand,model,car['mileage'],car['year'],car['city'],car['price']))
    
    sql.commit()
cursor.execute('''DELETE t1 FROM detail t1
                JOIN detail t2 
                ON 
                t1.brand = t2.brand AND
                t1.model = t2.model AND
                t1.mileage = t2.mileage AND
                t1.year = t2.year AND
                t1.city = t2.city AND
                t1.price = t2.price AND
                t1.id > t2.id;
               ''')

print('learning from database...')

cursor.execute('''select brand,model,mileage,year from detail''')
data_raw = cursor.fetchall()
cursor.execute('''select price from detail''')
result_raw = cursor.fetchall()

brands = [row[0] for row in data_raw]
models = [row[1] for row in data_raw]
mileages = [row[2] for row in data_raw]
years = [row[3] for row in data_raw]

prices = [row[0] for row in result_raw]

brand_encoder = LabelEncoder()
model_encoder = LabelEncoder()
mileage_encoder = LabelEncoder()

brands_encoded = brand_encoder.fit_transform(brands)
models_encoded = model_encoder.fit_transform(models)
mileages_encoded = mileage_encoder.fit_transform(mileages)

data = np.column_stack((brands_encoded, models_encoded, mileages_encoded, years))
result = np.array(prices).reshape(-1, 1)
cursor.close()
sql.close()

learn = DecisionTreeRegressor()
learn = learn.fit(data,result)

predictions = learn.predict(data)
r2 = r2_score(result, predictions)
accuracy_percent = r2 * 100
user_car_raw = []
print('Please write the required data in Persian\nAnd if you want to exit, press ctrl + C \n')
while(user_car_raw!='exit') :
    user_car_raw = ({
        'brand' : input('Enter car brand : '),
        'model' : input('Enter car model : '),
        'mileage' : int(input('Enter mileage (km) : ')),
        'year' : int(input('Enter manufacturing year : '))
    })

    in_brand = user_car_raw['brand'].replace(" ", "").strip()
    in_model = user_car_raw['model'].replace(" ", "").strip()
    if in_brand.isascii():
            in_brand = in_brand.lower()
    if in_model.isascii():
            in_model = in_model.lower()
    user_brand = in_brand
    user_model = in_model
    user_mileage = user_car_raw['mileage']
    user_year = user_car_raw['year']

    if user_brand not in brand_encoder.classes_:
        print(f"The brand '{user_brand}' does not exist in the trained data.")

    if user_model not in model_encoder.classes_:
        print(f"The brand '{user_model}' does not exist in the trained data.")

    user_brand_encoded = brand_encoder.transform([user_brand])
    if user_model is int:
         continue
    else:
        user_model_encoded = model_encoder.transform([user_model])

    user_car_encoded = np.column_stack((user_brand_encoded, user_model_encoded, [user_mileage], [user_year]))

    user_price = learn.predict(user_car_encoded)
    user_price = int(user_price[0])

    print(f"Predicted market price is {user_price:,} million tomans. ")
    print(f"\nModel accuracy (R² score) : {accuracy_percent:.2f}%")
