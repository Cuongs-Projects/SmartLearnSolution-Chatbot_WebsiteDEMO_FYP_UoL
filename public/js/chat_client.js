// Wait for the entire HTML document to be loaded before running the script
document.addEventListener('DOMContentLoaded', () => {
    const converter = new showdown.Converter();

    // Get references to the HTML elements we'll be interacting with
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatWindow = document.getElementById('chat-window');

    // This is the identifier for the course. You would set this dynamically.
    // For now, we'll hardcode it. In a real app, this might come from the URL
    // or be embedded in the page by your EJS template.
    // const currentCourse = "PADBRC";
    // const currentCourse = document.body.dataset.course;

    // Listen for the form to be submitted
    chatForm.addEventListener('submit', async (event) => {
        // 1. PREVENT THE DEFAULT PAGE REFRESH
        event.preventDefault();

        // 2. Get the user's message from the input field
        const userMessage = chatInput.value.trim();
        if (userMessage === '') {
            return; // Don't send empty messages
        }

        // 3. Immediately display the user's message in the chat window
        addMessageToChat('You', userMessage);
        
        // Clear the input field and show a "thinking" message
        chatInput.value = '';
        addMessageToChat('AI', 'Thinking...', true); // 'true' for a temporary message

        try {
            //get full resposne
            const response1 = await fetch('/show/conversation-get', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json', // Tell the server we're sending JSON
                }
            });

            if (!response1.ok) {
                // If the server responded with an error status (like 400 or 500)
                throw new Error(`Server error: ${response1.statusText}`);
            }

            const data1 = await response1.json();

            // 4. Send the message to your Node.js backend using Fetch API
            const response2 = await fetch('/show/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Tell the server we're sending JSON
                },
                // The body of the request, as a JSON string
                body: JSON.stringify({
                    question: userMessage,
                    // course: currentCourse, // Pass the dynamic course identifier
                    prompt_type: data1.prompt_type,
                    full_response: data1.full_response
                }),
            });

            if (!response2.ok) {
                // If the server responded with an error status (like 400 or 500)
                throw new Error(`Server error: ${response2.statusText}`);
            }

            // 5. Get the JSON data from the server's response
            const data2 = await response2.json();
            const aiMessage = data2.answer;

            //save full_response
            const response3 = await fetch('/show/conversation-save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Tell the server we're sending JSON
                },
                body: JSON.stringify({
                    full_response: data2.full_response,
                    prompt_type: data2.prompt_type
                })
            });

            if (!response3.ok) {
                // If the server responded with an error status (like 400 or 500)
                throw new Error(`Server error: ${response3.statusText}`);
            }

            // Remove the "Thinking..." message
            removeTemporaryMessage();

            // 6. Display the AI's response in the chat window
            addMessageToChat('AI', aiMessage);

        } catch (error) {
            console.error('Error:', error);
            removeTemporaryMessage();
            addMessageToChat('Error', 'Sorry, something went wrong. Please try again.');
        }
    });

    /**
     * Helper function to add a message to the chat window
     * @param {string} sender - Who sent the message ('You' or 'AI')
     * @param {string} text - The content of the message
     * @param {boolean} isTemporary - If true, adds a special class for removal
     */
    function addMessageToChat(sender, text, isTemporary = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        
        if (isTemporary) {
            messageElement.classList.add('temporary-message');
        }

        if (sender === 'You') {
            messageElement.classList.add('user-message');
            messageElement.innerHTML = `<strong style="color:Tomato;"><u>${sender}</u>:</strong> ${text}`;
        } else {
            messageElement.classList.add('ai-message');
            const htmlText = converter.makeHtml(text);
            messageElement.innerHTML = `<strong style="color:DodgerBlue;"><u>${sender}</u>:</strong> ${htmlText}`;
        }
        
        chatWindow.appendChild(messageElement);
        // Automatically scroll to the bottom to see the new message
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    /**
     * Helper function to remove the "Thinking..." message
     */
    function removeTemporaryMessage() {
        const tempMessage = chatWindow.querySelector('.temporary-message');
        if (tempMessage) {
            tempMessage.remove();
        }
    }
});