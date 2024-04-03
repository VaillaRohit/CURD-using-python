import mysql.connector
from mysql.connector import Error

def load_data_from_csv(file_path):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='python',
            user='root',
            password='12345',
            auth_plugin='mysql_native_password'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Load data from CSV file into the 'question' table
            query = """
                LOAD DATA LOCAL INFILE %s
                INTO TABLE question
                FIELDS TERMINATED BY ','
                LINES TERMINATED BY '\n'
                IGNORE 1 ROWS
                (question_text, question_type, answer_a, answer_b, answer_c, answer_d, correct_answer, explanation)
            """
            
            cursor.execute(query, (file_path,))

            # Commit the transaction
            connection.commit()

            print("Data loaded successfully from CSV file.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Example usage
csv_file_path = 'C:/Users/rg540/Desktop/a.csv'
load_data_from_csv(csv_file_path)
