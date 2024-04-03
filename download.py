import mysql.connector
import pandas as pd
from mysql.connector import Error

# MySQL database connection parameters

# CSV file path for download
csv_download_path = 'C:/Users/rg540/Desktop/downloaded_data.csv'

# SQL statement to select all data from the MySQL table
select_query = "SELECT * FROM question;"

try:
    # Connect to the MySQL database
    connection = mysql.connector.connect(
            host='localhost',
            database='python',
            user='root',
            password='12345',
            auth_plugin='mysql_native_password'
        )

    if connection.is_connected():
        # Use pandas to read the SQL query result directly into a DataFrame
        df = pd.read_sql_query(select_query, connection)

        # Export the DataFrame to CSV
        df.to_csv(csv_download_path, index=False)

        print(f"Data downloaded to: {csv_download_path}")

except Error as e:
    print(f"Error: {e}")

finally:
    # Close the database connection
    if connection.is_connected():
        connection.close()
        print("Connection closed.")
