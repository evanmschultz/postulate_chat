// Function to submit delete form
function submitDeleteForm(chatId) {
	const confirmDelete = window.confirm(
		`Are you sure you want to delete Chat #${chatId}?`
	);
	if (confirmDelete) {
		document.getElementById(`delete-chat-form-${chatId}`).submit();
	}
}

// Handling delete buttons: Now using form submission
document.addEventListener('DOMContentLoaded', function () {
	const deleteButtons = document.querySelectorAll('.delete-chat-button');
	deleteButtons.forEach((button) => {
		button.addEventListener('click', function () {
			const chatId = this.getAttribute('data-chat-id');
			submitDeleteForm(chatId);
		});
	});

	// Event listener for creating a new chat
	const createNewChatButton = document.getElementById('create-new-chat');
	createNewChatButton.addEventListener('click', function (event) {
		event.preventDefault(); // Prevent the default click behavior
		// Send a POST request to create a new chat
		fetch('/create_chat', {
			method: 'POST'
		})
			.then((response) => response.json())
			.then((data) => {
				if (data.redirect) {
					window.location.href = data.redirect;
				} else {
					alert('Failed to create new chat');
				}
			})
			.catch((error) => {
				console.error('Error:', error);
				alert('An error occurred while creating a new chat.');
			});
	});
});
