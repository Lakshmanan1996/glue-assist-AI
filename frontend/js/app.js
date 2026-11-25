
// =====================================
// GLUE ASSIST AI - FRONTEND APPLICATION
// =====================================

const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const chatContainer = document.getElementById("chatContainer");
const welcomeScreen = document.getElementById("welcomeScreen");
const newChatBtn = document.getElementById("newChatBtn");
const sendBtn = document.getElementById("sendBtn");
const customerSelect = document.getElementById("customerSelect");

const API_URL = "/chat";

// =====================================
// CUSTOMER SELECTION
// =====================================

function getSelectedCustomer() {
    return {
        id: customerSelect.value,
        name: customerSelect.options[
            customerSelect.selectedIndex
        ].text
    };
}

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

    messageElement.textContent = message;

    chatContainer.appendChild(messageElement);

    chatContainer.scrollTop = chatContainer.scrollHeight;

    return messageElement;
}

// =====================================
// SEND MESSAGE TO BACKEND
// =====================================

async function sendMessage(message, documentType=null) {

    const question = message.trim();
    const customer = getSelectedCustomer();

    if (!customer.id) {
        alert("Please select a customer before asking a question.");
        customerSelect.focus();
        return;
    }

    if (!question) {
        return;
    }

    if (welcomeScreen) {
        welcomeScreen.style.display = "none";
    }

    displayMessage(question, "user");

    messageInput.value = "";

    sendBtn.disabled = true;
    messageInput.disabled = true;
    customerSelect.disabled = true;

    const loadingMessage = displayMessage(
        "Glue Assist AI is processing your question...",
        "ai"
    );

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question,
                customer_id: customer.id,
                document_type: documentType

            })

        });

        if (!response.ok) {

            const errorData = await response.json().catch(() => ({}));

            throw new Error(
                errorData.detail || `Server error: ${response.status}`
            );

        }

        const data = await response.json();

        loadingMessage.remove();

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

        sendBtn.disabled = false;
        messageInput.disabled = false;
        customerSelect.disabled = false;

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
// KNOWLEDGE CARDS
// =====================================

document.querySelectorAll(".suggestion-card").forEach(function(card) {

    card.addEventListener("click", function() {

        const customer = getSelectedCustomer();

        if (!customer.id) {
            alert("Please select a customer first.");
            customerSelect.focus();
            return;
        }

        const topic = card.dataset.topic;

        let question = "";

	let documentType= null;

        if (topic === "ticketing") {
		question = `What is the ticketing process for ${customer.name}?`;

		documentType = "ticket_process";

        } else if (topic === "patch") {

		question = `What is the patch process and patch window for ${customer.name}?`;

		documentType = "patch_process";
        }

        if (question) {

		sendMessage(question, documentType);

	}

    });

});

// =====================================
// CUSTOMER CHANGE
// =====================================

customerSelect.addEventListener("change", function() {

    const existingMessages = chatContainer.querySelectorAll(".message");

    if (existingMessages.length > 0) {

        resetChat();

        displayMessage(
            "Customer changed to " + getSelectedCustomer().name +
            ". A new conversation has started.",
            "ai"
        );

    }

});

// =====================================
// RESET CHAT
// =====================================

function resetChat() {

    chatContainer.querySelectorAll(".message").forEach(function(message) {
        message.remove();
    });

    if (welcomeScreen) {
        welcomeScreen.style.display = "block";
    }

    messageInput.value = "";

    messageInput.disabled = false;
    sendBtn.disabled = false;
    customerSelect.disabled = false;

}

// =====================================
// NEW CHAT
// =====================================

newChatBtn.addEventListener("click", function() {

    resetChat();

    messageInput.focus();

});

