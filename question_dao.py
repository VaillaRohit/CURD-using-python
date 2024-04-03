import mysql.connector
from mysql.connector import Error
import pandas as pd

class QuestionDAO:
    def __init__(self, host, database, user, password):
        self.connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            auth_plugin='mysql_native_password'
        )

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()

    def create_question(self, question_text, question_type, answer_a, answer_b, answer_c, answer_d, correct_answer, explanation):
        try:
            cursor = self.connection.cursor()

            # Insert a new question into the database without specifying 'question_id'
            query = "INSERT INTO question (question_text, question_type, answer_a, answer_b, answer_c, answer_d, correct_answer, explanation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (question_text, question_type, answer_a, answer_b, answer_c, answer_d, correct_answer, explanation)
            cursor.execute(query, values)

            # Commit the transaction
            self.connection.commit()

            return cursor.lastrowid  # Return the ID of the newly created question

        except Error as e:
            print(f"Error creating question: {e}")

        finally:
            cursor.close()

    def retrieve_question(self, question_id):
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Retrieve a question from the database by ID
            query = "SELECT * FROM question WHERE question_id = %s"
            values = (question_id,)
            cursor.execute(query, values)
            question = cursor.fetchone()

            return question

        except Error as e:
            print(f"Error retrieving question: {e}")

        finally:
            cursor.close()

    def update_question(self, question_id, question_text=None, question_type=None, answer_a=None, answer_b=None, answer_c=None, answer_d=None,
                        correct_answer=None, explanation=None):
        try:
            cursor = self.connection.cursor()

            # Update the question in the database
            query = "UPDATE question SET question_text = %s, question_type = %s, answer_a = %s, answer_b = %s, answer_c = %s, answer_d = %s, correct_answer = %s, explanation = %s WHERE question_id = %s"
            values = (question_text, question_type, answer_a, answer_b, answer_c, answer_d, correct_answer, explanation, question_id)
            cursor.execute(query, values)

            # Commit the transaction
            self.connection.commit()

        except Error as e:
            print(f"Error updating question: {e}")

        finally:
            cursor.close()

    def delete_question(self, question_id):
        try:
            cursor = self.connection.cursor()

            # Delete a question from the database by ID
            query = "DELETE FROM question WHERE question_id = %s"
            values = (question_id,)
            cursor.execute(query, values)

            # Commit the transaction
            self.connection.commit()

        except Error as e:
            print(f"Error deleting question: {e}")

        finally:
            cursor.close()

    def load_data_from_csv(self, file_path):
        try:
            cursor = self.connection.cursor()

            # Load data from the CSV file into the 'question' table
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
            self.connection.commit()

            # Get the IDs of the newly created questions
            query = "SELECT question_id FROM question ORDER BY question_id DESC LIMIT 5"  # Adjust the LIMIT as needed
            cursor.execute(query)
            new_question_ids = [row[0] for row in cursor.fetchall()]

            # Get the total number of questions
            total_questions = self.get_total_questions()

            return new_question_ids, total_questions

        except Error as e:
            print(f"Error loading data from CSV: {e}")
            return None, None  # Return None for both variables in case of an error

        finally:
            cursor.close()
    
    def get_total_questions(self):
        try:
            cursor = self.connection.cursor()

            # Count the total number of questions
            query = "SELECT COUNT(*) FROM question"
            cursor.execute(query)
            total_questions = cursor.fetchone()[0]

            return total_questions

        except Error as e:
            print(f"Error getting total questions: {e}")
            return None

        finally:
            cursor.close()

    def download_data_to_csv(self, csv_path):
        try:
            cursor = self.connection.cursor()

            # SQL statement to select all data from the MySQL table
            select_query = "SELECT * FROM question"

            # Use pandas to read the SQL query result directly into a DataFrame
            df = pd.read_sql_query(select_query, self.connection)

            # Export the DataFrame to CSV
            df.to_csv(csv_path, index=False)

            print(f"Data downloaded to: {csv_path}")

        except Error as e:
            print(f"Error: {e}")

        finally:
            cursor.close()


# Example usage:
# Replace the connection details with your MySQL database credentials
host = "localhost"
database = "python"
user = "root"
password = "12345"
auth_plugin='mysql_native_password'

# question_dao = QuestionDAO(host, database, user, password)

# # Create a new question
# new_question_id = question_dao.create_question("What is your favorite color?", "Multiple Choice", "Blue", "I like the color blue.")

# # Retrieve the created question
# retrieved_question = question_dao.retrieve_question(new_question_id)
# print("Retrieved Question:", retrieved_question)

# # Update the question
# question_dao.update_question(new_question_id, question_text="What is your favorite animal?", question_type="Essay")

# # Retrieve the updated question
# updated_question = question_dao.retrieve_question(new_question_id)
# print("Updated Question:", updated_question)

# # Delete the question
# question_dao.delete_question(new_question_id)

# # Close the connection
# question_dao.close_connection()


# Create a new question
# created_question_id = question_dao.create_question(
#     question_text='What is your question?',
#     question_type='Multiple Choice',
#     answer_a='Option A',
#     answer_b='Option B',
#     answer_c='Option C',
#     answer_d='Option D',
#     correct_answer='Option A',
#     explanation='This is the explanation.'
# )

# # Retrieve the created question
# retrieved_question = question_dao.retrieve_question(created_question_id)
# print(f"Retrieved Question: {retrieved_question}")

# # Update the question
# question_dao.update_question(
#     question_id=created_question_id,
#     question_text='What is your updated question?',
#     question_type='True/False',
#     answer_a='True',
#     answer_b='False',
#     correct_answer='True',
#     explanation='Updated explanation.'
# )

# # Retrieve the updated question
# updated_question = question_dao.retrieve_question(created_question_id)
# print(f"Updated Question: {updated_question}")

# # Delete the question
# question_dao.delete_question(created_question_id)

# # Close the database connection
# question_dao.close_connection()
