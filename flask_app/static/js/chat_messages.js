// This script is specific to the chat messages interface

// Function to format code blocks in a given string
function formatCodeBlocks(inputString) {
	let formattedString = inputString.replace(
		/```(\w+)?\n([\s\S]*?)```/gm,
		function (_, lang, code) {
			return `<pre><code class="language-${
				lang || 'none'
			}">${code}</code></pre>`;
		}
	);

	// Replace inline code wrapped in single backticks with <code> tags
	formattedString = formattedString.replace(/`([^`]+)`/gm, '<code>$1</code>');

	// Return the formatted string
	return formattedString;
}

// Function to scroll the chat messages div to the bottom
function scrollToBottom(element) {
	element.scrollTop = element.scrollHeight;
}

// Extract the form submission logic into a separate function
function performFormSubmission(event, chatInput, chatMessages) {
	// Prevent the default form submission behavior
	event.preventDefault();

	// Clear the chat input and store its value for later use
	const userInput = chatInput.value;
	chatInput.value = '';

	// Create and append the user's message immediately for a responsive UI
	const userMessage = document.createElement('p');
	userMessage.innerHTML = `<strong>You:</strong> ${userInput}`;
	userMessage.style.border = '1px solid #ccc';
	userMessage.style.padding = '10px';
	chatMessages.appendChild(userMessage);

	// Create and append a loading message
	const loadingMessage = document.createElement('p');
	loadingMessage.innerHTML = '<strong>AI:</strong> Loading...';
	loadingMessage.style.border = '1px solid #ccc';
	loadingMessage.style.padding = '10px';
	chatMessages.appendChild(loadingMessage);

	// Scroll to the top after loading message is appended
	scrollToBottom(chatMessages);

	// Create a FormData object and append the user input
	const chatId = document.getElementById('chat-id').value;
	const formData = new FormData();
	formData.append('chat-input', userInput);
	formData.append('chat_id', chatId);

	// Send an AJAX POST request to send the message
	fetch('/chat/ajax_send_message', {
		method: 'POST',
		body: formData
	})
		.then((response) => response.json()) // Parse JSON response
		.then((data) => {
			// Remove the loading message
			chatMessages.removeChild(loadingMessage);

			// Format and append the bot's message
			const formattedBotResponse = formatCodeBlocks(data.bot_response);
			const botMessage = document.createElement('p');
			botMessage.innerHTML = `<strong>Bot:</strong> ${formattedBotResponse}`;
			botMessage.style.border = '1px solid #ccc';
			botMessage.style.padding = '10px';
			chatMessages.appendChild(botMessage);

			// Trigger Prism to highlight code blocks
			Prism.highlightAll();

			// Scroll the chat messages div to the bottom again
			chatMessages.scrollTop = chatMessages.scrollHeight;

			// Send an AJAX POST request to update the session
			fetch('/chat/update_session', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					formatted_response: formattedBotResponse
				})
			});
		});
}

document.addEventListener('DOMContentLoaded', function () {
	/// Select all message blocks with the class 'message-content'
	const messageBlocks = document.querySelectorAll('.message-content');
	// Loop through each message block to format its content
	messageBlocks.forEach((block) => {
		const originalContent = block.innerHTML; // Store the original content
		const formattedContent = formatCodeBlocks(originalContent); // Apply formatting
		block.innerHTML = formattedContent; // Replace original content with formatted content
	});

	// Handling delete buttons: Now using form submission
	const deleteButtons = document.querySelectorAll('.delete-chat-button');
	deleteButtons.forEach((button) => {
		button.addEventListener('click', function () {
			const chatId = this.getAttribute('data-chat-id');
			submitDeleteForm(chatId);
		});
	});

	// Scroll the chat messages div to the bottom
	const chatMessages = document.getElementById('chat-messages');
	scrollToBottom(chatMessages);

	// Get chat input and chat messages elements by their IDs
	const chatInput = document.getElementById('chat-input');

	// Add an event listener for input events on chat input
	chatInput.addEventListener('input', function () {
		// Dynamically adjust the height based on the scrollHeight
		this.style.height = 'auto';
		this.style.height = this.scrollHeight + 'px';
	});

	// Add a keydown event listener
	chatInput.addEventListener('keydown', function (event) {
		if (event.key === 'Enter' && (event.metaKey || event.ctrlKey)) {
			performFormSubmission(event, chatInput, chatMessages);
		}
	});

	// Add a submit event listener
	document
		.querySelector('.input-form')
		.addEventListener('submit', function (event) {
			performFormSubmission(event, chatInput, chatMessages);
		});
});
