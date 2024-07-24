document.getElementById('menuButton').addEventListener('click', function() {
    var sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('expanded');
});

const userId = document.getElementById('user');

document.addEventListener('DOMContentLoaded', () => {
    fetchData();
    getCurrentUser();
});

function fetchData() {
    fetch('https://pygame-6.onrender.com/quizzes')
        .then(response => response.json())
        .then(data => {
            displayQuizzes(data);
        })
        .catch(error => {
            console.error('Error fetching quizzes:', error);
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

        quizDiv.addEventListener('click', () => {
            window.location.href = `quiz.html?quizId=${quiz.id}`;
        });

        quizContainer.appendChild(quizDiv);
    });
}

function fetchQuestions(quizId, container) {
    fetch(`https://pygame-6.onrender.com/quizzes/${quizId}/questions`)
        .then(response => response.json())
        .then(data => {
            displayQuestions(data, container);
        })
        .catch(error => {
            console.error('Error fetching questions:', error);
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

function getCurrentUser() {
    const token = localStorage.getItem('access_token'); // or however you store the token

    if (!token) {
        throw new Error('No access token found');
    }

    fetch('https://pygame-6.onrender.com/check_session', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then((res) => {
        if (res.ok) {
            return res.json();
        } else {
            throw new Error('User not logged in');
        }
    })
    .then((user) => {
        console.log(user);
        userId.innerText = `${user.user.name}`;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

const button = document.getElementById('logout');
button.addEventListener('click', () => {
    logOut();
});

function logOut() {
    fetch('https://pygame-6.onrender.com/logout', {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            localStorage.removeItem('access_token'); // Clear the token from localStorage
            window.location.href = 'login.html'; // Redirect to login page
        } else {
            console.error('Failed to log out');
        }
    })
    .catch(error => {
        console.error('Error logging out:', error);
    });
}
