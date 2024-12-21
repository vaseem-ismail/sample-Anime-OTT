const BASE_URL = "https://backend-50024021027.development.catalystappsail.in";

async function registerUser() {
    const username = document.getElementById("register-username").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const messageElement = document.getElementById("register-message");

    try {
        const response = await fetch(`${BASE_URL}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, email, password }),
        });

        const data = await response.json();
        if (response.ok) {
            messageElement.style.color = "green";
            messageElement.textContent = data.message;
        } else {
            messageElement.style.color = "red";
            messageElement.textContent = data.message;
        }
    } catch (error) {
        messageElement.style.color = "red";
        messageElement.textContent = "Error registering user.";
    }
}

async function loginUser() {
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;
    const messageElement = document.getElementById("login-message");

    try {
        const response = await fetch(`${BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();
        if (response.ok) {
            messageElement.style.color = "green";
            messageElement.textContent = `${data.message}. Token: ${data.token}`;
        } else {
            messageElement.style.color = "red";
            messageElement.textContent = data.message;
        }
    } catch (error) {
        messageElement.style.color = "red";
        messageElement.textContent = "Error logging in.";
    }
}
