// Initialize Socket.IO connection
const socket = io.connect('http://127.0.0.1:5000');

// Unique identifier for the current AI message content box
let currentAiMessageContentId = null;

// Place this near the top of your script, or in a location where it will be run
console.log('Running regex test...');
const regexTestString = '```python\ncode here\n```';
const regex = /```(\w+)?\n([\s\S]*?)```/gm;
const match = regex.exec(regexTestString);
console.log('Regex test match:', match);

// function formatCodeBlocks(inputString) {
// 	console.log('Input to formatCodeBlocks:', inputString); // Log the input string
// 	let formattedString = inputString.replace(
// 		/```(\w+)?\n([\s\S]*?)```/gm,
// 		function (_, lang, code) {
// 			return `<pre><code class="language-${
// 				lang || 'none'
// 			}">${code}</code></pre>`;
// 		}
// 	);
// 	formattedString = formattedString.replace(/`([^`]+)`/gm, '<code>$1</code>');
// 	console.log('Output from formatCodeBlocks:', formattedString); // Log the output string
// 	return formattedString;
// }

// Function to format code blocks in a given string
function formatCodeBlocks(inputString) {
	console.log('Input to formatCodeBlocks:', inputString);
	let formattedString = inputString.replace(
		/```(\w+)?\n([\s\S]*?)```/gm,
		function (_, lang, code) {
			return `<pre><code class="language-${
				lang || 'none'
			}">${code}</code></pre>`;
		}
	);
	formattedString = formattedString.replace(/`([^`]+)`/gm, '<code>$1</code>');
	console.log('Output from formatCodeBlocks:', formattedString);
	return formattedString;
}

// Function to scroll the chat messages div to the bottom
function scrollToBottom(element) {
	console.log('Scrolling to bottom.');
	element.scrollTop = element.scrollHeight;
}

// Function to append received tokens to the chat
function appendTokenToChat(token, aiMessageContentId) {
	console.log('Appending token: ', token);
	// Use the existing unique ID for appending tokens
	const aiMessageElement = document.getElementById(aiMessageContentId);
	if (aiMessageElement) {
		aiMessageElement.textContent += token + ' ';
	}
}

// Temporary storage for accumulating tokens
let accumulatedTokens = '';

// Listen for new_token event
socket.on('new_token', function (data) {
	console.log('Received new token from server.');
	const token = data.token;
	accumulatedTokens += token; // Directly append tokens
	console.log('Current state of accumulatedTokens:', accumulatedTokens);

	// Use the existing unique identifier for appending tokens
	appendTokenToChat(token, currentAiMessageContentId);
});

// Listen for stream_end event
socket.on('stream_end', function (data) {
	console.log('Stream has ended from server.');
	console.log('Final state of accumulatedTokens:', accumulatedTokens);

	// Format the accumulated tokens
	const formattedContent = formatCodeBlocks(accumulatedTokens);
	console.log('Formatted content:', formattedContent);

	// Append the formatted content to chat
	const aiMessageElement = document.getElementById(currentAiMessageContentId);
	if (aiMessageElement) {
		aiMessageElement.innerHTML = formattedContent;
		aiMessageElement.innerHTML = formattedContent;
		Prism.highlightAll();
	}

	console.log('HTML encoded formattedContent:', escape(formattedContent));

	// Clear the accumulatedTokens string for the next stream
	accumulatedTokens = '';
	scrollToBottom(chatMessages);
});

// Perform form submission
function performFormSubmission(event, chatInput, chatMessages) {
	console.log('Form submission triggered.');
	event.preventDefault();

	const userInput = chatInput.value;
	chatInput.value = '';

	const userMessage = document.createElement('p');
	userMessage.innerHTML = `<strong>You:</strong> ${userInput}`;
	userMessage.style.border = '1px solid #ccc';
	userMessage.style.padding = '10px';
	chatMessages.appendChild(userMessage);

	// Create a new unique identifier for the AI message content box
	currentAiMessageContentId = 'ai-message-content-' + new Date().getTime();

	const aiMessage = document.createElement('p');
	aiMessage.style.border = '1px solid #ccc';
	aiMessage.style.padding = '10px';

	const aiLabel = document.createElement('strong');
	aiLabel.textContent = 'AI:';
	aiMessage.appendChild(aiLabel);

	const aiSpace = document.createElement('span');
	aiSpace.textContent = ' ';
	aiMessage.appendChild(aiSpace);

	const aiMessageContent = document.createElement('span');
	aiMessageContent.id = currentAiMessageContentId; // Set the unique ID
	aiMessage.appendChild(aiMessageContent);

	chatMessages.appendChild(aiMessage);

	scrollToBottom(chatMessages);

	const chatId = document.getElementById('chat-id').value;
	const formData = new FormData();
	formData.append('chat-input', userInput);
	formData.append('chat_id', chatId);

	fetch('/chat/ajax_send_message', {
		method: 'POST',
		body: formData
	})
		.then((response) => response.json())
		.then((data) => {
			if (data.status === 'streaming_started') {
				// You can show a loading indicator here if you want
			}
		});
}

document.addEventListener('DOMContentLoaded', function () {
	const messageBlocks = document.querySelectorAll('.message-content');
	messageBlocks.forEach((block) => {
		const originalContent = block.innerHTML;
		const formattedContent = formatCodeBlocks(originalContent);
		block.innerHTML = formattedContent;
	});

	const deleteButtons = document.querySelectorAll('.delete-chat-button');
	deleteButtons.forEach((button) => {
		button.addEventListener('click', function () {
			const chatId = this.getAttribute('data-chat-id');
			submitDeleteForm(chatId);
		});
	});

	const chatMessages = document.getElementById('chat-messages');
	scrollToBottom(chatMessages);

	const chatInput = document.getElementById('chat-input');

	chatInput.addEventListener('input', function () {
		this.style.height = 'auto';
		this.style.height = this.scrollHeight + 'px';
	});

	chatInput.addEventListener('keydown', function (event) {
		if (event.key === 'Enter' && (event.metaKey || event.ctrlKey)) {
			performFormSubmission(event, chatInput, chatMessages);
		}
	});

	document
		.querySelector('.input-form')
		.addEventListener('submit', function (event) {
			performFormSubmission(event, chatInput, chatMessages);
		});
});
