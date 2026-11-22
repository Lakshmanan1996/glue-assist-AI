
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const chatContainer = document.getElementById("chatContainer");
const customerSelect = document.getElementById("customerSelect");
const welcomeScreen = document.getElementById("welcomeScreen");
const newChatBtn = document.getElementById("newChatBtn");

// Display a message in the chat window
function displayMessage(message, sender) {
    const messageElement = document.createElement("div");

    messageElement.classList.add("message");

    if (sender === "user") {
        messageElement.classList.add("user-message");
    } else {
        messageElement.classList.add("ai-message");
    }

    // Use textContent to safely display user input
    messageElement.textContent = message;

    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Send a user message
function sendMessage(message) {
    const selectedCustomer = customerSelect.value;

    if (!selectedCustomer) {
        alert("Please select a customer first.");
        return;
    }

    const question = message.trim();

    if (!question) {
        return;
    }

    // Hide the welcome screen
    if (welcomeScreen) {
        welcomeScreen.style.display = "none";
    }

    // Display the customer question
    displayMessage(question, "user");

    // Temporary response until backend integration
    displayMessage(
        "Your question has been received. Backend and AI integration is pending.",
        "ai"
    );

    messageInput.value = "";
    messageInput.focus();
}

// Handle form submission
chatForm.addEventListener("submit", function(event) {
    event.preventDefault();

    sendMessage(messageInput.value);
});

// Handle suggested questions
document.querySelectorAll(".suggestion-card").forEach(function(card) {
    card.addEventListener("click", function() {
        const question = card.dataset.question;

        sendMessage(question);
    });
});

// Start a new conversation
newChatBtn.addEventListener("click", function() {
    chatContainer.querySelectorAll(".message").forEach(function(message) {
        message.remove();
    });

    if (welcomeScreen) {
        welcomeScreen.style.display = "block";
    }

    messageInput.value = "";
    messageInput.focus();
});
