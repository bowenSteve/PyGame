from app import create_app
from models import db, User, Quiz, Question, Choice, Score

def seed_data():
    app = create_app()
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
        quiz4 = Quiz(name='Data types in python')
        quiz5 = Quiz(name='Object-Oriented Programming in Python')
        quiz6 = Quiz(name='Error Handling in Python')
        quiz7 = Quiz(name='File I/O in Python')

        db.session.add_all([quiz1, quiz2, quiz3, quiz4, quiz5, quiz6, quiz7])
        db.session.commit()

        print("Creating questions and choices...")
        questions = [
            Question(text='What is the correct way to declare a variable in Python?', quiz_id=quiz1.id),
            Question(text='Which of the following is a valid variable name in Python?', quiz_id=quiz1.id),
            Question(text='How do you create a while loop in Python?', quiz_id=quiz2.id),
            Question(text='How do you create a for loop in Python?', quiz_id=quiz2.id),
            Question(text='How do you define a function in Python?', quiz_id=quiz3.id),
            Question(text='How do you call a function in Python?', quiz_id=quiz3.id),
            # New questions for quiz4
            Question(text='Which of the following is not a built-in data type in Python?', quiz_id=quiz4.id),
            Question(text='What is the correct way to create a list in Python?', quiz_id=quiz4.id),
            # New questions for quiz5
            Question(text='What keyword is used to define a class in Python?', quiz_id=quiz5.id),
            Question(text='What is the convention for naming classes in Python?', quiz_id=quiz5.id),
            # New questions for quiz6
            Question(text='Which statement is used to handle exceptions in Python?', quiz_id=quiz6.id),
            Question(text='What is the purpose of the "finally" clause in exception handling?', quiz_id=quiz6.id),
            # New questions for quiz7
            Question(text='Which function is used to open a file in Python?', quiz_id=quiz7.id),
            Question(text='What mode should be used to open a file for writing in Python?', quiz_id=quiz7.id),
        ]

        db.session.add_all(questions)
        db.session.commit()

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

            # New choices for quiz4
            Choice(text='Integer', is_correct=False, question_id=questions[6].id),
            Choice(text='Float', is_correct=False, question_id=questions[6].id),
            Choice(text='String', is_correct=False, question_id=questions[6].id),
            Choice(text='Array', is_correct=True, question_id=questions[6].id),

            Choice(text='list = [1, 2, 3]', is_correct=True, question_id=questions[7].id),
            Choice(text='list = (1, 2, 3)', is_correct=False, question_id=questions[7].id),
            Choice(text='list = {1, 2, 3}', is_correct=False, question_id=questions[7].id),
            Choice(text='list = 1, 2, 3', is_correct=False, question_id=questions[7].id),

            # New choices for quiz5
            Choice(text='class', is_correct=True, question_id=questions[8].id),
            Choice(text='def', is_correct=False, question_id=questions[8].id),
            Choice(text='function', is_correct=False, question_id=questions[8].id),
            Choice(text='object', is_correct=False, question_id=questions[8].id),

            Choice(text='PascalCase', is_correct=True, question_id=questions[9].id),
            Choice(text='camelCase', is_correct=False, question_id=questions[9].id),
            Choice(text='snake_case', is_correct=False, question_id=questions[9].id),
            Choice(text='kebab-case', is_correct=False, question_id=questions[9].id),

            # New choices for quiz6
            Choice(text='try-except', is_correct=True, question_id=questions[10].id),
            Choice(text='if-else', is_correct=False, question_id=questions[10].id),
            Choice(text='for-in', is_correct=False, question_id=questions[10].id),
            Choice(text='while-do', is_correct=False, question_id=questions[10].id),

            Choice(text='To execute code regardless of whether an exception occurred', is_correct=True, question_id=questions[11].id),
            Choice(text='To define custom exceptions', is_correct=False, question_id=questions[11].id),
            Choice(text='To raise exceptions', is_correct=False, question_id=questions[11].id),
            Choice(text='To skip exception handling', is_correct=False, question_id=questions[11].id),

            # New choices for quiz7
            Choice(text='open()', is_correct=True, question_id=questions[12].id),
            Choice(text='read()', is_correct=False, question_id=questions[12].id),
            Choice(text='file()', is_correct=False, question_id=questions[12].id),
            Choice(text='create()', is_correct=False, question_id=questions[12].id),

            Choice(text='"w"', is_correct=True, question_id=questions[13].id),
            Choice(text='"r"', is_correct=False, question_id=questions[13].id),
            Choice(text='"a"', is_correct=False, question_id=questions[13].id),
            Choice(text='"x"', is_correct=False, question_id=questions[13].id),
        ]

        db.session.add_all(choices)
        db.session.commit()

        print("Creating scores...")
        scores = [
            Score(user_id=user1.id, quiz_id=quiz1.id, score=1),
            Score(user_id=user1.id, quiz_id=quiz2.id, score=1),
            Score(user_id=user2.id, quiz_id=quiz3.id, score=1),
            Score(user_id=user3.id, quiz_id=quiz1.id, score=1),
        ]

        db.session.add_all(scores)
        db.session.commit()

        print("Seeding complete!")

if __name__ == '__main__':
    seed_data()