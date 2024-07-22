document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('signUpForm');
    form.addEventListener('submit', handleSubmit);
});

function validateForm() {
    const form = document.getElementById('signUpForm');
    const username = form.username.value.trim();
    const email = form.email.value.trim();
    const password = form.password.value.trim();

    if (!username || !email || !password) {
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
    event.preventDefault(); // Prevent the form from submitting the default way

    if (!validateForm()) {
        return;
    }

    const form = document.getElementById('signUpForm');
    const username = form.username.value.trim();
    const email = form.email.value.trim();
    const password = form.password.value.trim();

    addUser(username, email, password);
}

function addUser(username, email, password) {
    const configurationObject = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password
        })
    };

    fetch('http://127.0.0.1:5000/users', configurationObject)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(json => {
            console.log(json);
            alert('Sign up successful!');
            document.getElementById('signUpForm').reset(); // Reset the form fields
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Sign up failed. Please try again.');
        });
}