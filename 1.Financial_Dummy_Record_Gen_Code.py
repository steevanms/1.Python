# 1. Import necessary libraries
import pandas as pd
import random
from datetime import datetime
from faker import Faker
import pyodbc
import os
import uuid
import decimal



# 2. Initialize Faker
faker = Faker()



# 3. Function to generate random banking transactions
def generate_transactions(num_records):
    data = []
    transaction_type_list = ['Deposit','Withdrawal','Transfer','Loan Payment']
    branch_list = ['Head Office Branch', 'City Branch 1', 'City Branch 2', 'City Branch 3', 'City Branch 4']
    currency_list = ['USD', 'GBP', 'SGD', 'EUR', 'AUD']

    customer_registry = {}  # To ensure same BKey for same customer name

    # Generate data fro each transaction
    for i in range(num_records):
        transaction_id = str(uuid.uuid4())
        account_number = faker.unique.credit_card_number()
        transaction_date = faker.date_this_year()
        transaction_type = random.choice(transaction_type_list)
        transaction_amount = round(random.uniform(100,10000),2)
        currency_bkey = random.choice(currency_list)
        branch = random.choice(branch_list)

    # Generate or reuse customer data
        customer_name = faker.name()

        
        if customer_name not in customer_registry:
            customer_bkey = f"C{random.randint(1, 999999):05d}"
            dob = faker.date_of_birth(minimum_age=18, maximum_age=85)
            contact_number = faker.phone_number()
            email = faker.email()
            location = faker.city()
             # Save consistent customer details
            customer_registry[customer_name] = (customer_bkey, dob, contact_number, email, location)
        else:
            customer_bkey, dob, contact_number, email, location = customer_registry[customer_name]

    # Add all the data to the list
        data.append([transaction_id, customer_bkey, account_number, transaction_date, transaction_type, transaction_amount, currency_bkey, branch,
                     customer_name, dob, contact_number, email, location])

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['TransactionID', 'CustomerBkey', 'AccountNumber', 'TransactionDate', 'TransactionType', 'TransactionAmount', 
                                     'CurrencyBkey', 'Branch', 'CustomerName', 'DOB', 'ContactNumber', 'Email', 'Location'])

    return df



# 4. Generate number of records
num_records = 500000 # Put the number of records to be generated here.
df = generate_transactions(num_records)



# 5. Function to export data to excel
def export_to_excel(df, file_name, num_of_records):
    df.to_excel(file_name, index=False)
    current_directory = os.getcwd()
    print(f'Data exported sucessfully to {file_name} in path: {current_directory}!')



# 6. Export to excel file
file_name = 'Banking_transaction_data.xlsx'
export_to_excel(df, file_name, 500)


# 7. Function to insert data into SQL server using SqlAlchemy
from sqlalchemy import create_engine

def insert_into_sqlalchemy(df, server, database, table_name):
    connection_string = f'mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(connection_string)

    # Insert data
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f'Data inserted into table {database}.dbo.{table_name}')



# 8. Insert into SQL server
server = <your-db-server-name>
database = <your-db-name>
table_name = <your-target-table-name>

insert_into_sqlalchemy(df, server, database, table_name)