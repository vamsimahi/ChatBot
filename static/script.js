function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    // Display user's message
    displayMessage(userInput, "user");

    // Send the message to the Flask backend
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `message=${encodeURIComponent(userInput)}`
    })
    .then(response => response.json())
    .then(data => {
        // Display chatbot's response
        displayMessage(data.response, "bot");
    })
    .catch(error => {
        console.error('Error:', error);
    });

    // Clear the input field
    document.getElementById("user-input").value = "";
}

function displayMessage(message, sender) {
    const chatBox = document.getElementById("chat-box");

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("chat-message");
    messageDiv.classList.add(sender + "-message");
    messageDiv.innerText = sender.charAt(0).toUpperCase() + sender.slice(1) + ": " + message;

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to the latest message
}
