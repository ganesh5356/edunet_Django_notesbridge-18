document.addEventListener('DOMContentLoaded', function () {
    const trigger = document.getElementById('chat-trigger');
    const container = document.getElementById('chat-container');
    const closeBtn = document.getElementById('close-chat');
    const sendBtn = document.getElementById('send-btn');
    const input = document.getElementById('chat-input');
    const messagesContainer = document.getElementById('chat-messages');

    if (!trigger || !container || !closeBtn || !sendBtn || !input || !messagesContainer) return;

    // Toggle Chat
    trigger.addEventListener('click', () => {
        container.classList.toggle('active');
        if (container.classList.contains('active')) {
            input.focus();
        }
    });

    closeBtn.addEventListener('click', () => {
        container.classList.remove('active');
    });

    // Send Message Logic
    function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        // Append User Message
        appendMessage(text, 'user');
        input.value = '';

        // Simulate thinking and then respond using knowledge base
        setTimeout(() => {
            const response = getChatResponse(text);
            appendMessage(response, 'bot');
        }, 300);
    }

    function appendMessage(text, side) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${side}`;
        msgDiv.textContent = text;
        messagesContainer.appendChild(msgDiv);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    sendBtn.addEventListener('click', sendMessage);

    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Initial greeting
    setTimeout(() => {
        appendMessage("Hello! I'm the NotesBridge Helper. How can I assist you with the project today?", 'bot');
    }, 1000);
});
