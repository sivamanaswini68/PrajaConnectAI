// PrajaConnectAI Chatbot Script

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const providerSelect = document.getElementById('providerSelect');
    const languageSelect = document.getElementById('languageSelect');
    const clearBtn = document.getElementById('clearChatBtn');

    if (!chatForm || !chatInput || !chatMessages) return;

    // Check if initial query parameter exists
    const urlParams = new URLSearchParams(window.location.search);
    const initialQuery = urlParams.get('q');
    if (initialQuery) {
        chatInput.value = initialQuery;
        sendMessage(initialQuery);
    }

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const msg = chatInput.value.trim();
        if (msg) {
            sendMessage(msg);
            chatInput.value = '';
        }
    });

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            fetch('/assistant/clear', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                chatMessages.innerHTML = `
                    <div class="message-bubble msg-ai">
                        Hello! I am your <strong>PrajaConnectAI Assistant</strong>.<br>
                        Ask me about government schemes, eligibility, required documents, or health camps.
                    </div>
                `;
            });
        });
    }

    function sendMessage(messageText) {
        // Append user message
        appendMessage(messageText, 'user');

        // Show typing indicator
        const typingId = appendTypingIndicator();

        const provider = providerSelect ? providerSelect.value : 'local';
        const language = languageSelect ? languageSelect.value : 'English';

        fetch('/assistant/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: messageText,
                provider: provider,
                language: language
            })
        })
        .then(res => res.json())
        .then(data => {
            removeTypingIndicator(typingId);
            if (data.response) {
                appendMessage(data.response, 'ai');
            } else {
                appendMessage("AI service is temporarily unavailable. Please try again.", 'ai');
            }
        })
        .catch(err => {
            removeTypingIndicator(typingId);
            console.error('Chat API Error:', err);
            appendMessage("Unable to connect to AI server. Please check your internet connection.", 'ai');
        });
    }

    function appendMessage(text, sender) {
        const bubble = document.createElement('div');
        bubble.className = `message-bubble msg-${sender}`;
        
        // Simple Markdown-like formatting (bold, newlines, bullet points)
        let formatted = text
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`([^`]+)`/g, '<code>$1</code>');
            
        bubble.innerHTML = formatted;
        chatMessages.appendChild(bubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function appendTypingIndicator() {
        const id = 'typing_' + Date.now();
        const indicator = document.createElement('div');
        indicator.id = id;
        indicator.className = 'message-bubble msg-ai';
        indicator.innerHTML = `<em>PrajaConnectAI is thinking...</em>`;
        chatMessages.appendChild(indicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    function removeTypingIndicator(id) {
        const elem = document.getElementById(id);
        if (elem) elem.remove();
    }
});
