import mysql.connector as sql1
from sqlalchemy import create_engine as cengine
import pandas as pd
from dotenv import load_dotenv
import os
# import the dataset
data = pd.read_csv("D:\\Data set\\customer_shopping_behavior.csv")
# print(data)

# predict the null values
print(data.isnull().sum())

#to check the structure 
print(data.info())

# describe  the dataset
print(data.describe(include="all"))

# show the all null values
print(data.isnull().isna().sum())

# see the dataset columns names
print(data.columns)

# fill the data the according to catergory
data["Review Rating"] = data.groupby(
    "Category")["Review Rating"].transform(lambda x: x.fillna(x.median()))


# see the again the dataset
print(data.isnull().sum())

# covert the dataset the column name  to lower case
data.columns = data.columns.str.lower()

# remove the spaces and underline of the column name
data.columns = data.columns.str.replace(" ", "_")

# rename the column name according the dataset
data = data.rename(columns={"purchase_amount_(usd)": "purchase_amount"})
print(data.columns)

# create group of ages
labels = ["Young Adult", "Adult", "Middle-aged", "Senior"]
data["age_group"] = pd.qcut(data['age'], q=4, labels=labels)

print(data[["age", "age_group"]].head(100))

# create column purchase_frequancy_days

frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Mouth': 90
}

data['purchase_frequency_days'] = data['frequency_of_purchases'].map(
    frequency_mapping)
print(data[['purchase_frequency_days', 'frequency_of_purchases']].head(10))

print(data[['discount_applied', 'promo_code_used']])

# the both column are same value
print((data['discount_applied'] == data["promo_code_used"]).all())

# then drop the column
data = data.drop('promo_code_used', axis=1)

print(data['review_rating'].isnull())

# load env
load_dotenv()
dataBase = sql1.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    passwd=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB")
)
createengine = cengine(
    'mysql+mysqlconnector://root:vivek@localhost/customer_behaviours')
# cursorobject = dataBase.cursor()

# 1. query="create database customer_behaviours"

# 2. cols = ", ".join([f"{col} VARCHAR(255)" for col in data.columns])
# 2. cursorobject.execute(f"CREATE TABLE IF NOT EXISTS customer_data_table({cols})")

query = "select *from customer_data_table"
# cursorobject.execute(query)

# ""CREATE THE DATA TO ANOTHER DATAFRAME ADDING NEW VARIABLE""
new_data = pd.DataFrame(data)

# Insert  the data  into MySQL
new_data.to_sql("customer_data_table", createengine,
                if_exists="append", index=False)


df = pd.read_sql(query, createengine)
print(df)
print("Query Succefully Run!!!")
# dataBase.commit()
dataBase.close()
