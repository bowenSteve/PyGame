from flask_restful import Resource
from flask import Flask, request, make_response, jsonify, session
from models import db, User, Quiz, Question, Choice, Score
from config import bcrypt, app, db, api


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username=data.get('username')
    password=data.get('password')
    if password and username:
        user = User.query.filter_by(name=username).first()
        if user and user.authenticate(password):
            session['user_id'] = user.id
        else:
            return jsonify({"fail":"Invalid user inputs"})


@app.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None) 
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/quizzes', methods=['GET'])
def get_quizzes():
    quizzes = [quiz.to_dict() for quiz in Quiz.query.all()]
    return jsonify(quizzes)
@app.route('/quizzes/<int:quiz_id>/questions', methods=['GET'])
def get_questions_for_quiz(quiz_id):
    # Query the questions for the specified quiz ID
    quiz = Quiz.query.get(quiz_id)
    
    if not quiz:
        return jsonify({'message': 'Quiz not found'}), 404
    
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    questions_list = []
    
    for question in questions:
        choices = Choice.query.filter_by(question_id=question.id).all()
        choices_list = [{'id': choice.id, 'text': choice.text, 'is_correct': choice.is_correct} for choice in choices]
        
        questions_list.append({
            'id': question.id,
            'text': question.text,
            'choices': choices_list
        })
    
    return jsonify(questions_list)
class CheckSession(Resource):

    def get(self):
        user_id = session['user_id']
        print(user_id)
        if user_id:
            user=User.query.filter(User.id==user_id).first()
            return user.to_dict(),200

        return {}, 401

api.add_resource(CheckSession, '/check_session')

@app.route('/submit-answers', methods=['POST'])
def submit_answers():
    data = request.json
    
    user_id = data.get('userId')
    quiz_id = data.get('quizId')
    answers = data.get('answers')  # Expected format: [{"questionId": 1, "choiceId": 3}, ...]

    if not user_id or not quiz_id or not answers:
        return jsonify({'message': 'Invalid input'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'message': 'Quiz not found'}), 404

    score = 0

    for answer in answers:
        question_id = answer.get('questionId')
        choice_id = answer.get('choiceId')

        question = Question.query.get(question_id)
        if not question:
            return jsonify({'message': f'Question {question_id} not found'}), 404

        choice = Choice.query.get(choice_id)
        if not choice:
            return jsonify({'message': f'Choice {choice_id} not found'}), 404

        # Check if the selected choice is correct
        if choice.is_correct:
            score += 1

    # Update the user's score in the database
    existing_score = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
    if existing_score:
        existing_score.score = score
    else:
        new_score = Score(user_id=user_id, quiz_id=quiz_id, score=score)
        db.session.add(new_score)

    db.session.commit()

    return jsonify({'message': 'Score updated successfully', 'score': score}), 200

@app.route('/users', methods=['POST'])
def signup():
    data = request.get_json()

    # Extract and validate data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'All fields are required.'}), 400

    if len(password) < 6:
        return jsonify({'message': 'Password must be at least 6 characters long.'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User with this email already exists.'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(name=username, email=email, password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully.'}), 201

if __name__ == '__main__':
    app.run(debug=True)
