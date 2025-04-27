from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

assignments = []
assignment_counter = 1

@app.route('/form', methods=['GET'])
def form():
    return send_file('form.html')

@app.route('/api/assignments', methods=['POST'])
def assign_lesson():
    global assignment_counter

    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    required_fields = ['teacherId', 'studentId', 'lessonId']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    assignment = {
        "assignmentId": assignment_counter,
        "teacherId": data['teacherId'],
        "studentId": data['studentId'],
        "lessonId": data['lessonId'],
        "isCompleted": False
    }
    assignments.append(assignment)
    assignment_counter += 1

    return jsonify({
        "assignmentId": assignment["assignmentId"],
        "message": "Lesson assigned successfully."
    }), 201

@app.route('/api/assignments', methods=['GET'])
def get_all_assignments():
    return jsonify(assignments), 200

@app.route('/api/assignments/incomplete', methods=['GET'])
def view_incomplete_assignments():
    student_id = request.args.get('studentId')
    if not student_id:
        return jsonify({"error": "Missing studentId"}), 400

    result = [a for a in assignments if a["studentId"] == student_id and not a["isCompleted"]]
    return jsonify(result), 200

@app.route('/api/assignments/<int:assignment_id>/complete', methods=['PUT'])
def mark_assignment_complete(assignment_id):
    for assignment in assignments:
        if assignment["assignmentId"] == assignment_id:
            assignment["isCompleted"] = True
            return jsonify({"message": "Assignment marked as complete."}), 200

    return jsonify({"error": "Assignment not found"}), 404

@app.route('/api/assignments/status', methods=['GET'])
def view_assignment_status():
    teacher_id = request.args.get('teacherId')
    if not teacher_id:
        return jsonify({"error": "Missing teacherId"}), 400

    result = [a for a in assignments if a["teacherId"] == teacher_id]
    return jsonify(result), 200

@app.route('/')
def home():
    return "Welcome to the VOPA Assignment API!"

@app.route('/api/assignments/<int:assignment_id>', methods=['GET'])
def get_assignment(assignment_id):
    for assignment in assignments:
        if assignment["assignmentId"] == assignment_id:
            return jsonify(assignment), 200
    return jsonify({"error": "Assignment not found"}), 404
