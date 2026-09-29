import os
import logging
import pandas as pd
import mysql.connector

# Configure logging to report status in each function
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def read_data(filename: str) -> pd.DataFrame:
    """
    Loads a CSV file into a pandas DataFrame.
    
    Args:
        filename (str): The path to the CSV file.
        
    Returns:
        pd.DataFrame: The loaded data.
    """
    logger.info(f"Reading data from file: {filename}")
    try:
        df = pd.read_csv(filename)
        logger.info(f"Successfully loaded {len(df)} rows from {filename}")
        return df
    except Exception as e:
        logger.error(f"Failed to read CSV file {filename}: {e}")
        raise

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares the DataFrame for upload by removing rows with missing values.
    
    Args:
        data (pd.DataFrame): The raw DataFrame.
        
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    logger.info("Starting data cleaning process...")
    try:
        # Remove rows with missing values as required
        cleaned_data = data.dropna().copy()
        logger.info(f"Data cleaning complete. Remaining rows: {len(cleaned_data)}")
        return cleaned_data
    except Exception as e:
        logger.error(f"Error during data cleaning: {e}")
        raise

def load_data(data: pd.DataFrame, table: str = "mock") -> None:
    """
    Writes the DataFrame to MySQL using row-by-row parameterized inserts 
    within a try/except/finally block. Always passes 'mock' as the table name.
    
    Args:
        data (pd.DataFrame): The cleaned DataFrame to upload.
        table (str): The destination table name (defaults to 'mock').
    """
    logger.info(f"Connecting to database to upload data into table '{table}'...")
    
    # Lab setup uses DBHOST/DBUSER/DBPASS/DBNAME; accept those names.
    host = os.getenv("DBHOST", os.getenv("DB_HOST", "localhost"))
    database = os.getenv("DBNAME", os.getenv("DB_NAME"))
    user = os.getenv("DBUSER", os.getenv("DB_USER"))
    password = os.getenv("DBPASS", os.getenv("DB_PASSWORD"))
    port = int(os.getenv("DBPORT", os.getenv("DB_PORT", "3306")))

    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        cursor = connection.cursor()
        
        # Create the 'mock' table if it doesn't exist
        columns_def = ", ".join([f"`{col}` TEXT" for col in data.columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{table}` ({columns_def});"
        cursor.execute(create_table_query)
        
        # Use parameterized queries (%s) to prevent SQL injection vulnerabilities
        cols = ", ".join([f"`{col}`" for col in data.columns])
        placeholders = ", ".join(["%s"] * len(data.columns))
        insert_query = f"INSERT INTO `{table}` ({cols}) VALUES ({placeholders})"
        
        # Loop over DataFrame rows and insert
        for _, row in data.iterrows():
            cursor.execute(insert_query, tuple(row))
            
        connection.commit()
        logger.info(f"Successfully inserted {len(data)} rows into table '{table}'.")
        
    except Exception as e:
        logger.error(f"Database error occurred during load: {e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            logger.info("Database connection closed.")

def main():
    """Main execution flow calling read_data, clean_data, and load_data in sequence."""
    csv_filename = "MOCK_DATA.csv"
    
    try:
        raw_df = read_data(csv_filename)
        cleaned_df = clean_data(raw_df)
        load_data(cleaned_df, table="mock")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")

if __name__ == "__main__":
    main()
