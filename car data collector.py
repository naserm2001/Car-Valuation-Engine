import httpx
import json
import mysql.connector
from sklearn.tree import DecisionTreeRegressor
import numpy as np
from jdatetime import date as jdate
from datetime import date
from sklearn.metrics import r2_score
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
import pandas as pd


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
               price bigint)''')

for page in range(1,51) :
    print('collecting data from page ',page)
    
    try:
        response = httpx.get(base_url + str(page), headers=headers)
    except Exception as e:
         print('Error in prediction : ', e)

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
                'year' : int(year),
                'price' : int(price.replace(",", "").replace(" ", "").strip())
            })

    for car in cars:
        brand = car['brand']
        model = car['model']
        if brand.isascii():
            brand = brand.lower()
        if model.isascii():
            model = model.lower()
        cursor.execute('''insert into detail (brand,model,mileage,year,price)
                        values(%s,%s,%s,%s,%s)'''
                       ,(brand,model,car['mileage'],car['year'],car['price']))
    
    sql.commit()
    os.system('cls')
cursor.execute('''DELETE t1 FROM detail t1
                JOIN detail t2 
                ON 
                t1.brand = t2.brand AND
                t1.model = t2.model AND
                t1.mileage = t2.mileage AND
                t1.year = t2.year AND
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

df_features = pd.DataFrame({
     'brand' : brands,
     'model' : models,
     'mileage' : mileages,
     'year' : years
})

df_target = pd.Series(prices)

preprocessor = ColumnTransformer(
     transformers=[
          ('categorical', OneHotEncoder(handle_unknown='ignore'),['brand', 'model']),
          ('numerical', 'passthrough', ['mileage', 'year'])
     ]
)

model_pipeline = make_pipeline(preprocessor, DecisionTreeRegressor())

x_train, x_test, y_train, y_test = train_test_split(df_features, df_target, test_size=0.2, random_state=42)

model_pipeline.fit(x_train, y_train)

predictions = model_pipeline.predict(x_test)

r2 = r2_score(y_test, predictions)
accuracy_percent = r2 * 100

cursor.close()
sql.close()

attemps = 10
while attemps > 0 :

    os.system('cls')
    
    print(f'Please write the required data in Persian\nAnd if you want to exit, press ctrl + C \n\t\tYou have {attemps} attemps left')

    user_car_raw = []

    for user in range(0,10) :
        user_car_raw = ({
            'brand' : input('Enter car brand : '),
            'model' : input('Enter car model : '),
            'mileage' : int(input('Enter mileage (km) : ')),
            'year' : int(input('Enter manufacturing year : '))
        })

        if int(user_car_raw['year']) > 1800 :
                year = date(int(year), 6, 15)
                shamsi_date = jdate.fromgregorian(date=year)
                user_car_raw['year'] = int(shamsi_date.year)

        user_brand = user_car_raw['brand'].replace(" ", "").strip()
        user_model = user_car_raw['model'].replace(" ", "").strip()
    
        if user_brand.isascii():
                user_brand = user_brand.lower()
        if user_model.isascii():
                user_model = user_model.lower()
    
        df_input = pd.DataFrame([{ 
            'brand' : user_brand,
            'model' : user_model,
            'mileage' : user_car_raw['mileage'],
            'year' : user_car_raw['year']
        }])

        if user_brand not in df_features['brand'].unique() :
            print(f"The brand '{user_brand}' does not exist in the trained data.")
            continue
        if user_model not in df_features['model'].unique() :
            print(f"The brand '{user_model}' does not exist in the trained data.")
            continue

        try:
            user_price = model_pipeline.predict(df_input)
            user_price = int(user_price[0])

            print(f"\nPredicted market price is {user_price:,} million tomans. ")
            print(f"\nModel accuracy : {accuracy_percent:.2f}%\nAnd you have {attemps} attemps left")
        except Exception as e:
            print('Error in prediction : ', e)
        
        attemps -= 1
