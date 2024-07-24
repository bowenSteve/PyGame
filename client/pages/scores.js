document.addEventListener('DOMContentLoaded', () => {
    fetchScores();
});

function fetchScores() {
    // Retrieve the token from localStorage
    const token = localStorage.getItem('access_token');
    if (!token) {
        console.error('No access token found');
        return;
    }

    // Make the fetch request with the token in the Authorization header
    fetch(`https://pygame-6.onrender.com/user_scores`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        displayScores(data);
        console.log(data);
    })
    .catch(error => {
        console.error('Error fetching scores:', error);
    });
}
function displayScores(scores) {
    const tableBody = document.getElementById('scores-table-body');
    tableBody.innerHTML = ''; // Clear existing rows

    scores.forEach(score => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${score.quiz_name}</td>
            <td>${score.score}</td>
        `;
        tableBody.appendChild(row);
    });
}
