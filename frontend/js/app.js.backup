
// =====================================
// GLUE ASSIST AI - FRONTEND APPLICATION
// =====================================

const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const chatContainer = document.getElementById("chatContainer");
const welcomeScreen = document.getElementById("welcomeScreen");
const newChatBtn = document.getElementById("newChatBtn");
const sendBtn = document.getElementById("sendBtn");

const API_URL = "/chat";

// =====================================
// DISPLAY CHAT MESSAGE
// =====================================

function displayMessage(message, sender) {
    const messageElement = document.createElement("div");

    messageElement.classList.add("message");

    if (sender === "user") {
        messageElement.classList.add("user-message");
    } else {
        messageElement.classList.add("ai-message");
    }

    // Safely display message content
    messageElement.textContent = message;

    chatContainer.appendChild(messageElement);

    chatContainer.scrollTop = chatContainer.scrollHeight;

    return messageElement;
}

// =====================================
// SEND MESSAGE TO BACKEND
// =====================================

async function sendMessage(message) {

    const question = message.trim();

    if (!question) {
        return;
    }

    // Hide welcome screen
    if (welcomeScreen) {
        welcomeScreen.style.display = "none";
    }

    // Display user question
    displayMessage(question, "user");

    // Clear input
    messageInput.value = "";

    // Prevent duplicate submissions
    sendBtn.disabled = true;
    messageInput.disabled = true;

    // Display loading message
    const loadingMessage = displayMessage(
        "Glue Assist AI is processing your question...",
        "ai"
    );

    try {

        // Send question to FastAPI
        const response = await fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })
        });

        // Check HTTP response
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));

            throw new Error(
                errorData.detail || `Server error: ${response.status}`
            );
        }

        // Read backend response
        const data = await response.json();

        // Remove loading message
        loadingMessage.remove();

        // Display AI response
        displayMessage(
            data.message || "The backend returned an empty response.",
            "ai"
        );

    } catch (error) {

        loadingMessage.remove();

        console.error("Chat API Error:", error);

        displayMessage(
            "Unable to process your question. " + error.message,
            "ai"
        );

    } finally {

        // Re-enable input
        sendBtn.disabled = false;
        messageInput.disabled = false;

        messageInput.focus();
    }
}

// =====================================
// CHAT FORM SUBMISSION
// =====================================

chatForm.addEventListener("submit", function(event) {

    event.preventDefault();

    sendMessage(messageInput.value);

});

// =====================================
// SUGGESTED QUESTIONS
// =====================================

document.querySelectorAll(".suggestion-card").forEach(function(card) {

    card.addEventListener("click", function() {

        const question = card.dataset.question;

        sendMessage(question);

    });

});

// =====================================
// NEW CHAT
// =====================================

newChatBtn.addEventListener("click", function() {

    // Remove previous messages
    chatContainer.querySelectorAll(".message").forEach(function(message) {
        message.remove();
    });

    // Show welcome screen
    if (welcomeScreen) {
        welcomeScreen.style.display = "block";
    }

    // Clear input
    messageInput.value = "";

    messageInput.disabled = false;
    sendBtn.disabled = false;

    messageInput.focus();

});

