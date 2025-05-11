import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import io
import base64
from exam_scheduler import ExamScheduler

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

@app.route('/', methods=['GET'])
def index():
    """
    Render the main page of the exam scheduler
    """
    # Initialize with example data
    example_subjects = ['Math', 'Physics', 'Chemistry', 'Biology', 'English']
    example_students = {
        'Alice': ['Math', 'Physics', 'English'],
        'Bob': ['Math', 'Chemistry'],
        'Charlie': ['Physics', 'Biology'],
        'Daisy': ['Math', 'English', 'Biology'],
        'Eve': ['Chemistry', 'Biology']
    }
    
    return render_template('index.html', 
                          example_subjects=json.dumps(example_subjects),
                          example_students=json.dumps(example_students))

@app.route('/schedule', methods=['POST'])
def schedule():
    """
    Process the form data and generate an exam schedule
    """
    try:
        # Get data from the form
        subjects_str = request.form.get('subjects', '')
        students_str = request.form.get('students', '')
        
        # Parse the subjects
        subjects = [s.strip() for s in subjects_str.split(',') if s.strip()]
        
        # Parse the students data
        students_data = {}
        student_lines = students_str.strip().split('\n')
        for line in student_lines:
            if ':' in line:
                student_name, student_subjects = line.split(':', 1)
                student_name = student_name.strip()
                student_subjects = [s.strip() for s in student_subjects.split(',') if s.strip()]
                students_data[student_name] = student_subjects
        
        # Create an exam scheduler
        scheduler = ExamScheduler(subjects, students_data)
        
        # Generate the schedule
        exam_schedule = scheduler.generate_schedule()
        
        # Generate the graph visualization
        graph_image = scheduler.visualize_graph()
        
        # Convert the plot to a base64 encoded image
        buffer = io.BytesIO()
        graph_image.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Generate schedule table data
        time_slots = {}
        for subject, slot in exam_schedule.items():
            if slot not in time_slots:
                time_slots[slot] = []
            time_slots[slot].append(subject)
        
        # Store the results in session
        session['exam_schedule'] = exam_schedule
        session['time_slots'] = time_slots
        session['graph_image'] = image_base64
        
        return render_template('result.html', 
                              schedule=exam_schedule,
                              time_slots=time_slots,
                              graph_image=image_base64)
    
    except Exception as e:
        logging.exception("Error generating schedule")
        flash(f"Error generating schedule: {str(e)}", "danger")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
