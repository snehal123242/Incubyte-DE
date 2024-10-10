import pandas as pd
import psycopg2
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='etl/etl_process.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Database connection details
DB_DETAILS = {
    'host': 'localhost',
    'dbname': 'Incubyte',
    'user': 'postgres',
    'password': 'Neelima@03',
    'port': 5432
}

#load data from CSV
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, sep=',', skiprows=1, header=None,
                         names=['Type', 'Customer_Name', 'Customer_Id', 'Open_Date', 'Last_Consulted_Date', 
                                'Vaccination_Id', 'Dr_Name', 'State', 'Country', 'DOB', 'Is_Active'])
        df = df[df['Type'] == 'D']  # Filter only detail records
        logging.info(f"Loaded {len(df)} records from {file_path}")
        return df
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        return None
    
# Data Transformatiom
def transform_data(df):
    try:
        #Transformed Open_Date to format as '%Y%m%d. In source data it was given in ISO8601 format
        df['Open_Date'] = pd.to_datetime(df['Open_Date'], format='%Y%m%d', errors='coerce')
        df['Last_Consulted_Date'] = pd.to_datetime(df['Last_Consulted_Date'], format='%Y%m%d', errors='coerce')
        df['DOB'] = pd.to_datetime(df['DOB'], dayfirst=True, errors='coerce')

        #Managing only the dates where values are not null
        df['Last_Consulted_Date'] = df['Last_Consulted_Date'].where(pd.notnull(df['Last_Consulted_Date']), None)
        df['Open_Date'] = df['Open_Date'].where(pd.notnull(df['Open_Date']), None)
        df['DOB'] = df['DOB'].where(pd.notnull(df['DOB']), None)

        #current age cal. using current date and DOB
        current_year = datetime.now().year
        df['Age'] = (current_year - df['DOB'].dt.year).fillna(0).astype(int)  # Fill NaN with 0 for age
        df['Days_Since_Last_Consulted'] = (datetime.now() - df['Last_Consulted_Date']).dt.days.fillna(0).astype(int)  # Fill NaN with 0 for days since last consulted

        logging.info("Data transformation complete")
        return df
    except Exception as e:
        logging.error(f"Error transforming data: {str(e)}")
        return None

#load data to database
def load_to_database(df, conn, cur):
    try:
        for _, row in df.iterrows():
            table_name = f"Table_{row['Country']}"
# Insert Query to add data using table name to the data should be loaded according to country
            insert_query = f"""
                INSERT INTO {table_name} (Customer_Name, Customer_Id, Open_Date, Last_Consulted_Date, Vaccination_Id, 
                                          Dr_Name, State, Country, DOB, Is_Active, Age, Days_Since_last_Consulted)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (Customer_Id) DO UPDATE
                SET Last_Consulted_Date = EXCLUDED.Last_Consulted_Date""" 
                
#Executing the given query using cursor
            cur.execute(insert_query, (
    row['Customer_Name'], 
    row['Customer_Id'], 
    row['Open_Date'] if pd.notna(row['Open_Date']) else None, 
    row['Last_Consulted_Date'] if pd.notna(row['Last_Consulted_Date']) else None,
    row['Vaccination_Id'], 
    row['Dr_Name'], 
    row['State'], 
    row['Country'], 
    row['DOB'] if pd.notna(row['DOB']) else None, 
    row['Is_Active'], 
    row['Age'], 
    row['Days_Since_Last_Consulted']
))
        conn.commit()
        logging.info("Data loaded to database")
    except Exception as e:
        logging.error(f"Error loading data to database: {str(e)}")
        conn.rollback()

def main():
    file_path = 'data/sample_customer_data.csv'
    
    #get data from source(Sample_customer_data.csv)
    df = load_data(file_path)
    if df is None:
        return
    
    # transformations on imported data
    
    df = transform_data(df)
    if df is None:
        return
    
    #loading the transformed data to database
    try:
        conn = psycopg2.connect(**DB_DETAILS)
        cur = conn.cursor()
        load_to_database(df, conn, cur)
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")

if __name__ == "__main__":
    main()
