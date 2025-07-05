// Wait for the entire HTML document to be loaded before running the script
document.addEventListener('DOMContentLoaded', () => {

    // Get references to the HTML elements we'll be interacting with
    const clearButton = document.getElementById('clear-chat');

    // Listen for the form to be submitted
    clearButton.addEventListener('click', async (event) => {

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

            data = response1.json()
            if (data.full_response != ""){
                //save full_response
                const response3 = await fetch('/show/conversation-save', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json', // Tell the server we're sending JSON
                    },
                    body: JSON.stringify({
                        full_response: "",
                        prompt_type: 'init'
                    })
                });

                if (!response3.ok) {
                    // If the server responded with an error status (like 400 or 500)
                    throw new Error(`Server error: ${response3.statusText}`);
                }

                // Also clear the visual chat window
                document.getElementById('chat-window').innerHTML = '';
                alert('Chat history has been cleared.');
            }

        } catch (error) {
            console.error('Error:', error);
        }
    });
});