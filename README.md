#Car Data Collector and Price Predictor
This repository contains a Python script (car_data_collector.py) that builds a car price prediction model from data scraped from Bama.ir. Bama.ir is a leading online marketplace for new and used cars in Iran
linkedin.com
. The script uses the httpx library to fetch data from the public API, extracts key features (brand, model, year, mileage, city, price, etc.), and converts listing dates from the Gregorian calendar to the Jalali (Persian) calendar using the jdatetime library
python-httpx.org
pypi.org
. After extraction, the data is cleaned and saved to a MySQL database, where duplicate entries are removed to ensure data integrity
medium.com
. Categorical features (like brand and model) are encoded into numerical form using scikit-learn’s LabelEncoder
scikit-learn.org
. A DecisionTreeRegressor model (a supervised learning algorithm for regression) is then trained on the prepared data to predict car prices
ibm.com
. The model’s performance is evaluated using the R² (coefficient of determination) metric
scikit-learn.org
. Finally, the script prompts the user to input a car’s details (brand, model, year, mileage) and outputs the estimated market price. This end-to-end pipeline—from web scraping to database storage to machine learning prediction—demonstrates data engineering and machine learning integration in Python.
Key Features
Web Scraping with httpx: Retrieves car listing data from the Bama.ir API using httpx, an HTTP client for Python
python-httpx.org
.
Feature Extraction: Parses the API response to extract relevant fields (brand, model, year, mileage, city, price, etc.).
Date Conversion: Converts Gregorian dates to the Jalali (Persian) calendar using jdatetime, which is a Python implementation of the Jalali date system
pypi.org
.
Data Cleaning & Storage: Cleans the dataset and inserts it into a MySQL database. Duplicate records are removed via SQL commands, improving data quality and consistency
medium.com
.
Categorical Encoding: Uses scikit-learn’s LabelEncoder to transform textual categories (e.g. car brand names) into numerical labels for model training
scikit-learn.org
.
Machine Learning Model: Trains a DecisionTreeRegressor to learn the relationship between car features and price. Decision trees are a popular non-parametric method for regression tasks
ibm.com
.
Model Evaluation: Computes the R² score on a test set to evaluate how well the model explains the variance in car prices
scikit-learn.org
.
Interactive Prediction: After training, the script prompts the user to enter a car’s brand, model, year, and mileage, then outputs the predicted market price (in Iranian Rial).
Technologies Used
Python 3
httpx – Async-capable HTTP client for making API requests
python-httpx.org
jdatetime – Python library for handling Jalali (Persian) dates
pypi.org
MySQL – Relational database to store and query the collected data
scikit-learn – Machine learning library (for LabelEncoder, DecisionTreeRegressor, r2_score, etc.)
mysql-connector-python or PyMySQL – Python libraries to connect to the MySQL database
Installation Requirements
Python 3.9+: Ensure Python is installed.
MySQL Server: Install and run a MySQL database. Create a database (e.g. cars_db) for the project.
Python Libraries: Install required packages using pip:
nginx
Copy
Edit
pip install httpx jdatetime scikit-learn mysql-connector-python
(Alternatively, use PyMySQL instead of mysql-connector-python if preferred.)
Database Configuration: Update the database connection settings (host, port, user, password, database name) in car_data_collector.py or via environment variables, so the script can connect to MySQL.
How to Run the Script
Clone the repository to your local machine.
Configure Database: Verify that the MySQL database is running and that the credentials in the script match your setup. The script will create tables if they do not exist.
Run the Script: Open a terminal in the project directory and execute:
nginx
Copy
Edit
python "car_data_collector.py"
Follow Prompts: When prompted, enter the car’s brand, model, manufacturing year, and mileage.
The script will display the predicted price based on the trained model. Internally, it also prints evaluation metrics such as the R² score on a held-out test set to indicate model performance.
Example Output Structure
Below is an example interaction when running the script. User inputs are in italics:
yaml
Copy
Edit
Enter car brand: *Toyota*
Enter car model: *Corolla*
Enter manufacturing year: *2018*
Enter mileage (km): *50000*

Predicted market price: 1,500,000,000 IRR
R² score on test data: 0.85
The output shows the estimated price (in Iranian Rial) for the given car details, along with the model’s R² score. Prices in the dataset and output are typically represented in IRR (Iranian Rials).
License
This project is licensed under the MIT License. See the LICENSE file for details.
