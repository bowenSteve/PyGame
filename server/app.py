from flask import Flask, request, jsonify, session, current_app
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, bcrypt, User, Quiz, Question, Choice, Score

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key_here'
    app.json.compact = False
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

    # Initialize extensions
    bcrypt.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    jwt = JWTManager(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Define resources
    class Login(Resource):
        def post(self):
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            user = User.query.filter_by(name=username).first()
            if user:# and bcrypt.check_password_hash(user.password_hash, password):
                access_token = create_access_token(identity=username)
                return jsonify(access_token=access_token)
            else:
                return jsonify({'errors': ['Invalid username or password']}), 401

    api.add_resource(Login, '/login')

    @app.route('/check_session', methods=['GET'])
    @jwt_required()
    def check_session():
        current_user = get_jwt_identity()
        user = User.query.filter_by(name=current_user).first()
        if user:
            return jsonify(logged_in_as=current_user, user=user.to_dict()), 200
        return jsonify({'error': 'User not found'}), 404

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

    @app.route('/submit-answers', methods=['POST'])
    def submit_answers():
        data = request.json
        user_id = data.get('userId')
        quiz_id = data.get('quizId')
        answers = data.get('answers')

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

    @app.route('/scores', methods=['POST'])
    @jwt_required()
    def submit_score():
        current_user = get_jwt_identity()
        user = User.query.filter_by(name=current_user).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        quiz_id = data.get('quiz_id')
        score = data.get('score')

        if not quiz_id or score is None:
            return jsonify({'error': 'Invalid data'}), 400

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404

        existing_score = Score.query.filter_by(user_id=user.id, quiz_id=quiz_id).first()
        if existing_score:
            existing_score.score = score
        else:
            new_score = Score(user_id=user.id, quiz_id=quiz_id, score=score)
            db.session.add(new_score)

        db.session.commit()

        return jsonify({'message': 'Score submitted successfully'}), 201


    @app.route('/user_scores', methods=['GET'])
    @jwt_required()
    def user_scores():
        current_user = get_jwt_identity()
        user = User.query.filter_by(name=current_user).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get all scores for the user
        scores = db.session.query(Quiz.name, Score.score).join(Score).filter(Score.user_id == user.id).all()
        
        # Format the results
        scores_list = [{'quiz_name': quiz_name, 'score': score} for quiz_name, score in scores]
        print(scores_list)
        return jsonify(scores_list), 200
    

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



    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
