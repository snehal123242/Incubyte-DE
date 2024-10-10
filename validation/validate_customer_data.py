import pandas as pd
import logging

# Setup logging
logging.basicConfig(filename='validation.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def validate_data(df):
    """
    Validate data for mandatory fields and report any missing or invalid data.
    :param df: DataFrame to validate
    :return: Boolean value indicating whether validation passed or failed
    """
    mandatory_columns = ['Customer_Name', 'Customer_Id', 'Open_Date', 'DOB', 'Country']
    
    # Check for missing mandatory fields
    missing_data = df[mandatory_columns].isnull().sum()
    if missing_data.any():
        logging.error(f"Missing mandatory fields: {missing_data}")
        return False
    
    logging.info("Data validation passed.")
    return True
