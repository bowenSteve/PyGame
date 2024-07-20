document.getElementById('menuButton').addEventListener('click', function() {
    var sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('expanded');
});

document.addEventListener('DOMContentLoaded', () => {
    fetchData();
});

function fetchData() {
    fetch('http://127.0.0.1:5000/quizzes')
        .then(response => response.json())
        .then(data => {
            displayQuizzes(data);
        });
}

function displayQuizzes(quizzes) {
    const quizContainer = document.getElementById('quizContainer');
    quizContainer.innerHTML = '';

    quizzes.forEach(quiz => {
        const quizDiv = document.createElement('div');
        quizDiv.className = 'quiz';
        quizDiv.dataset.quizId = quiz.id;

        const quizTitle = document.createElement('h3');
        quizTitle.textContent = quiz.name;
        quizDiv.appendChild(quizTitle);

        // Add an event listener to navigate to the quiz page on click
        quizDiv.addEventListener('click', () => {
            // Redirect to quiz.html with the quiz ID as a query parameter
            window.location.href = `quiz.html?quizId=${quiz.id}`;
        });

        quizContainer.appendChild(quizDiv);
    });
}

function fetchQuestions(quizId, container) {
    fetch(`http://127.0.0.1:5000/quizzes/${quizId}/questions`)
        .then(response => response.json())
        .then(data => {
            displayQuestions(data, container);
        });
}

function displayQuestions(questions, container) {

    container.innerHTML = '';

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

        
            const choiceText = document.createElement('p');
            choiceText.textContent = choice.text;
            choiceDiv.appendChild(choiceText);

  
            if (choice.is_correct) {
                choiceDiv.classList.add('correct');
            }

            choicesContainer.appendChild(choiceDiv);
        });

        container.appendChild(questionDiv);
    });


    container.style.display = 'block';
}
