from app import app
from models import db, User, Quiz, Question, Choice, Score

def seed_data():
    with app.app_context():
        print("Deleting data...")
        User.query.delete()
        Quiz.query.delete()
        Question.query.delete()
        Choice.query.delete()
        Score.query.delete()

        db.session.commit()

        print("Creating users...")
        user1 = User(name='Alice Smith', email='alice@example.com')
        user1.password_hash = 'password123'
        
        user2 = User(name='Jared Bowen', email='bowen@example.com')
        user2.password_hash = 'password123'
        
        user3 = User(name='Stephen Bowen', email='stephen@example.com')
        user3.password_hash = 'password123'
        
        db.session.add_all([user1, user2, user3])
        db.session.commit()

        print("Creating quizzes...")
        quiz1 = Quiz(name='Variables in Python')
        quiz2 = Quiz(name='Loops in Python')
        quiz3 = Quiz(name='Functions in Python')
        
        db.session.add_all([quiz1, quiz2, quiz3])
        db.session.commit()

        # Ensure quizzes are refreshed and have IDs
        db.session.refresh(quiz1)
        db.session.refresh(quiz2)
        db.session.refresh(quiz3)

        print("Creating questions and choices...")
        questions = [
            Question(text='What is the correct way to declare a variable in Python?', quiz_id=quiz1.id),
            Question(text='Which of the following is a valid variable name in Python?', quiz_id=quiz1.id),
            Question(text='How do you create a while loop in Python?', quiz_id=quiz2.id),
            Question(text='How do you create a for loop in Python?', quiz_id=quiz2.id),
            Question(text='How do you define a function in Python?', quiz_id=quiz3.id),
            Question(text='How do you call a function in Python?', quiz_id=quiz3.id),
        ]

        db.session.add_all(questions)
        db.session.commit()

        # Ensure questions are refreshed and have IDs
        for question in questions:
            db.session.refresh(question)

        choices = [
            Choice(text='var x = 5', is_correct=False, question_id=questions[0].id),
            Choice(text='x = 5', is_correct=True, question_id=questions[0].id),
            Choice(text='int x = 5', is_correct=False, question_id=questions[0].id),
            Choice(text='x := 5', is_correct=False, question_id=questions[0].id),

            Choice(text='1variable', is_correct=False, question_id=questions[1].id),
            Choice(text='_variable', is_correct=True, question_id=questions[1].id),
            Choice(text='variable-1', is_correct=False, question_id=questions[1].id),
            Choice(text='var$', is_correct=False, question_id=questions[1].id),

            Choice(text='while x > 5 { }', is_correct=False, question_id=questions[2].id),
            Choice(text='while x > 5:', is_correct=True, question_id=questions[2].id),
            Choice(text='while (x > 5)', is_correct=False, question_id=questions[2].id),
            Choice(text='while x > 5 then', is_correct=False, question_id=questions[2].id),

            Choice(text='for x to 5 { }', is_correct=False, question_id=questions[3].id),
            Choice(text='for x in range(5):', is_correct=True, question_id=questions[3].id),
            Choice(text='foreach x in range(5)', is_correct=False, question_id=questions[3].id),
            Choice(text='for x > 5', is_correct=False, question_id=questions[3].id),

            Choice(text='def functionName():', is_correct=True, question_id=questions[4].id),
            Choice(text='function functionName():', is_correct=False, question_id=questions[4].id),
            Choice(text='define functionName():', is_correct=False, question_id=questions[4].id),
            Choice(text='functionName() define:', is_correct=False, question_id=questions[4].id),

            Choice(text='functionName()', is_correct=True, question_id=questions[5].id),
            Choice(text='call functionName()', is_correct=False, question_id=questions[5].id),
            Choice(text='execute functionName()', is_correct=False, question_id=questions[5].id),
            Choice(text='run functionName()', is_correct=False, question_id=questions[5].id),
        ]

        db.session.add_all(choices)
        db.session.commit()

        print("Creating scores...")
        scores = [
            Score(user_id=user1.id, quiz_id=quiz1.id),
            Score(user_id=user1.id, quiz_id=quiz2.id),
            Score(user_id=user2.id, quiz_id=quiz3.id),
            Score(user_id=user3.id, quiz_id=quiz1.id),
        ]

        db.session.add_all(scores)
        db.session.commit()

        print("Seeding complete!")

if __name__ == '__main__':
    seed_data()
