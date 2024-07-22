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
        })
        .catch(error => {
            console.error('Error fetching questions:', error);
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

            const choiceLabel = document.createElement('label');
            choiceLabel.textContent = choice.text;
            choiceDiv.appendChild(choiceLabel);

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
            submitQuiz(); // Automatically submit when time is up
        }
    }, 1000);
}

document.getElementById('submitQuiz').addEventListener('click', () => {
    submitQuiz();
});
function submitQuiz() {
    const questions = document.querySelectorAll('.question');
    let score = 0;
    const quizId = new URLSearchParams(window.location.search).get('quizId');

    if (!quizId) {
        console.error('Quiz ID not found');
        return;
    }

    questions.forEach(question => {
        const selectedChoice = question.querySelector('input[type="radio"]:checked');
        if (selectedChoice) {
            const choiceId = selectedChoice.value;
            const choiceElement = Array.from(question.querySelectorAll('.choice')).find(choice => choice.querySelector('input').value === choiceId);
            if (choiceElement && choiceElement.classList.contains('correct')) {
                score++;
            }
        }
    });

    document.getElementById('scoreCounter').textContent = score;

    // Send the score to the server
    fetch('https://pygame-5.onrender.com/scores', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Replace with actual token retrieval
    },
    body: JSON.stringify({ quiz_id: quizId, score: score })
})
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
})
.then(data => {
    console.log('Score submitted successfully:', data);
})
.catch(error => {
    console.error('Error submitting score:', error);
});

}
