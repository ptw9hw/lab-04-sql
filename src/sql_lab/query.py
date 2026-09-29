import os
import logging
import mysql.connector

# Configure logging for functions (as required in Step 7)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def get_data_by_group(value: str):
    """
    Retrieves all rows from the mock table where the 'group' column equals the given value.
    
    Args:
        value (str): The group value to filter by.
        
    Returns:
        list: A list of matching database rows.
    """
    logger.info(f"Querying data where group = {value}")
    
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
        
        # Using backticks around `group` since it's a reserved keyword in MySQL
        query = "SELECT * FROM `mock` WHERE `group` = %s;"
        cursor.execute(query, (value,))
        results = cursor.fetchall()
        
        logger.info(f"Successfully retrieved {len(results)} rows for group '{value}'.")
        return results
    except Exception as e:
        logger.error(f"Error executing get_data_by_group: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def plot_counts(groupby: str):
    """
    Counts rows per distinct value for a given column name in the mock table.
    
    Args:
        groupby (str): The column name to group and count by.
        
    Returns:
        list: A list of tuples containing (group_value, count).
    """
    logger.info(f"Counting row frequencies grouped by column: {groupby}")
    
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
        
        # Dynamically reference the column safely with backticks
        query = f"SELECT `{groupby}`, COUNT(*) FROM `mock` GROUP BY `{groupby}`;"
        cursor.execute(query)
        results = cursor.fetchall()
        
        logger.info(f"Successfully counted rows grouped by '{groupby}'.")
        return results
    except Exception as e:
        logger.error(f"Error executing plot_counts: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    """Main execution flow demonstrating query functions."""
    print("Starting query demonstrations...")
    
    # Example demonstration of get_data_by_group
    test_group_value = "dom"  # A value present in MOCK_DATA.csv
    try:
        rows = get_data_by_group(test_group_value)
        print(f"Rows for group '{test_group_value}':")
        for row in rows[:5]:  # Print the first few rows
            print(row)
    except Exception as e:
        print(f"Failed to fetch data by group: {e}")

    # Example demonstration of plot_counts
    test_column = "group"  # Update to match a column name in your table
    try:
        counts = plot_counts(test_column)
        print(f"Counts grouped by '{test_column}':")
        for val, count in counts:
            print(f"  {val}: {count}")
    except Exception as e:
        print(f"Failed to print counts: {e}")

if __name__ == "__main__":
    main()
