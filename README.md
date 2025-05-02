# Car Data Collector and Price Predictor

This repository contains a Python script (`car_data_collector.py`) that builds a car price prediction model from data scraped from Bama.ir. The script uses `httpx` to fetch data from the public API, extracts features (brand, model, year, mileage, city, price), and converts dates to the Jalali calendar. It saves cleaned data to a MySQL database, trains a machine learning model, and predicts car prices based on user input.

## Key Features

- **Web Scraping with httpx:** Retrieves car listing data from Bama.ir API.
- **Feature Extraction:** Extracts brand, model, year, mileage, city, and price.
- **Date Conversion:** Converts Gregorian dates to Jalali using `jdatetime`.
- **Data Cleaning & Storage:** Stores data in MySQL and removes duplicates.
- **Categorical Encoding:** Encodes string fields (brand/model) to numbers.
- **Machine Learning Model:** Trains a `DecisionTreeRegressor` to estimate prices.
- **Model Evaluation:** Uses R² score to measure prediction accuracy.
- **Interactive Prediction:** Takes user input and outputs estimated price.

## Technologies Used

- Python 3
- httpx
- jdatetime
- MySQL
- scikit-learn
- mysql-connector-python

## Installation Requirements

1. **Python 3.9+**
2. **MySQL Server**
3. **Python Packages:**

   ```bash
   pip install httpx jdatetime scikit-learn mysql-connector-python

4.Database Setup: Create a MySQL database (e.g., cars), and update credentials in the script.

## How to Run the Script

1.Clone the repository:
    
    git clone https://github.com/your-username/your-repository.git
    cd your-repository

2.Configure the database connection inside the script.

3.Run the script:
   
    
    python car_data_collector.py

3.Enter the requested car details when prompted.

### Example Output

    Enter car brand : هیوندای
    Enter car model : سوناتا
    Enter mileage (km) : 50000
    Enter manufacturing year : 1393

    Predicted market price is 2,850,000,000 million tomans.
    Model accuracy (R² score) : 85.00%

## License
•This project is licensed under the MIT License.

## Notes
•This project is for educational and personal use only.

•Always respect the terms of service of websites you scrape.
