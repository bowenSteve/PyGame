document.addEventListener('DOMContentLoaded', () => {
    const quizId = new URLSearchParams(window.location.search).get('quizId');
    if (quizId) {
        fetchQuestions(quizId);
        startTimer();
    }
});

function fetchQuestions(quizId) {
    fetch(`http://127.0.0.1:5000/quizzes/${quizId}/questions`)
        .then(response => response.json())
        .then(data => {
            displayQuestions(data);
        });
}

function displayQuestions(questions) {
    const quizContainer = document.getElementById('quizContainer');
    quizContainer.innerHTML = '';

    questions.forEach(question => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question';
        
        const questionText = document.createElement('p');
        questionText.textContent = question.text;
        questionDiv.appendChild(questionText);

        const choicesContainer = document.createElement('div');
        choicesContainer.className = 'choices';
        questionDiv.appendChild(choicesContainer);

        question.choices.forEach(choice => {
            const choiceDiv = document.createElement('div');
            choiceDiv.className = 'choice';

            const choiceInput = document.createElement('input');
            choiceInput.type = 'radio';
            choiceInput.name = `question-${question.id}`;
            choiceInput.value = choice.id;
            choiceDiv.appendChild(choiceInput);

            const choiceText = document.createElement('label');
            choiceText.textContent = choice.text;
            choiceDiv.appendChild(choiceText);

            if (choice.is_correct) {
                choiceDiv.classList.add('correct');
            }

            choicesContainer.appendChild(choiceDiv);
        });

        quizContainer.appendChild(questionDiv);
    });
}

function startTimer() {
    let timeLeft = 30;
    const timerElement = document.getElementById('timer');
    const timerInterval = setInterval(() => {
        timeLeft--;
        timerElement.textContent = `Time left: ${timeLeft}s`;

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            timerElement.textContent = 'Time is up!';
            document.getElementById('submitQuiz').disabled = true;
        }
    }, 1000);
}

document.getElementById('submitQuiz').addEventListener('click', () => {
    const questions = document.querySelectorAll('.question');
    let score = 0;

    questions.forEach(question => {
        const selectedChoice = question.querySelector('input[type="radio"]:checked');
        if (selectedChoice) {
            const choiceId = selectedChoice.value;
            fetch(`http://127.0.0.1:5000/choices/${choiceId}`)
                .then(response => response.json())
                .then(choice => {
                    if (choice.is_correct) {
                        score++;
                    }
                    document.getElementById('scoreCounter').textContent = score;
                });
        }
    });
});


