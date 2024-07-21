document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    form.addEventListener('submit', handleSubmit);
});

function validateForm() {
    const form = document.getElementById('loginForm');
    const username = form.username.value.trim();
    const password = form.password.value.trim();

    if (!username || !password) {
        alert('All fields are required.');
        return false;
    }

    if (password.length < 6) {
        alert('Password must be at least 6 characters long.');
        return false;
    }

    return true;
}

function handleSubmit(event) {
    event.preventDefault(); 

    if (!validateForm()) {
        return;
    }

    const form = document.getElementById('loginForm');
    const username = form.username.value.trim();
    const password = form.password.value.trim();

    Login(username, password);
}
function Login(username, password) {
    const configurationObject = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    };
    
    fetch('http://127.0.0.1:5000/login', configurationObject)
        .then(response => response.json())
        .then(json => {
            if (json.errors) {
                // Handle login failure
                alert('Login failed. Please check your credentials.');
            } else {
                // Store the JWT token in localStorage
                localStorage.setItem('access_token', json.access_token);
                window.location.href = 'home.html';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Login failed. Please try again.');
        });
}
