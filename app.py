from flask import Flask, render_template, request, jsonify, redirect, url_for
from question_dao import QuestionDAO
import os

app = Flask(__name__)

# Replace these database connection details with your actual values
db_config = {
    'host': 'localhost',
    'database': 'python',
    'user': 'root',
    'password': '12345',
}

question_dao = QuestionDAO(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            # Retrieve form data
            question_text = request.form['question_text']
            question_type = request.form['question_type']
            answer_a = request.form['answer_a']
            answer_b = request.form['answer_b']
            answer_c = request.form['answer_c']
            answer_d = request.form['answer_d']
            correct_answer = request.form['correct_answer']
            explanation = request.form['explanation']

            # Create a new question
            question_id = question_dao.create_question(
                question_text, question_type, answer_a, answer_b, answer_c, answer_d, correct_answer, explanation
            )

            return jsonify({'message': f'Question created successfully with ID: {question_id}'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('create.html')

@app.route('/retrieve', methods=['GET'])
def retrieve():
    question_id = request.args.get('question_id')
    question = question_dao.retrieve_question(question_id)
    return render_template('retrieve.html', question=question)


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        try:
            # Retrieve form data for updating a question
            question_id = request.form['update_question_id']
            question_text = request.form['update_question_text']
            question_type = request.form['update_question_type']
            answer_a = request.form['update_answer_a']
            answer_b = request.form['update_answer_b']
            answer_c = request.form['update_answer_c']
            answer_d = request.form['update_answer_d']
            correct_answer = request.form['update_correct_answer']
            explanation = request.form['update_explanation']

            # Update the question
            question_dao.update_question(
                question_id, question_text, question_type, answer_a, answer_b, answer_c, answer_d, correct_answer, explanation
            )

            return jsonify({'message': f'Question with ID {question_id} updated successfully.'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        try:
            # Retrieve form data for deleting a question
            question_id = request.form['delete_question_id']

            # Delete the question
            question_dao.delete_question(question_id)

            return jsonify({'message': f'Question with ID {question_id} deleted successfully.'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('delete.html')


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/load_csv_page', methods=['GET'])
def load_csv_page():
    return render_template('load_csv.html')

@app.route('/load_csv', methods=['POST'])
def load_csv():
    try:
        # Check if the post request has the file part
        if 'csv_file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        csv_file = request.files['csv_file']

        # If user does not select file, browser also
        # submit an empty part without filename
        if csv_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the file to a temporary location
        if csv_file and allowed_file(csv_file.filename):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_file.filename)
            csv_file.save(file_path)

            # Load data from the CSV file
        new_question_ids, total_questions = question_dao.load_data_from_csv(file_path)

        if new_question_ids is not None and total_questions is not None:
            message = f'CSV file loaded successfully. New Question IDs: {", ".join(map(str, new_question_ids))}'
        else:
            message = 'Error loading data from CSV.'

        return render_template('load_csv.html', message=message, total_questions=total_questions)

    except Exception as e:
        return render_template('load_csv.html', error=str(e))

@app.route('/download_csv', methods=['GET'])
def download_csv():
    try:
        # CSV file path for download
        csv_download_path = 'C:/Users/rg540/Desktop/downloaded_data.csv'

        # Call the download_data_to_csv method
        question_dao.download_data_to_csv(csv_download_path)

        return jsonify({'message': f'Data downloaded to: {csv_download_path}'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
            

if __name__ == '__main__':
    app.run(debug=True)
