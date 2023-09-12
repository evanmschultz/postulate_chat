// This script is specific to the settings menu

document.addEventListener('DOMContentLoaded', function () {
	const singleUrlForm = document.getElementById('single-url-ingest-form');
	const multipleUrlsForm = document.getElementById('url-ingest-form');

	// This event listener will handle the submission of the Single URL form.
	singleUrlForm.addEventListener('submit', function (event) {
		event.preventDefault(); // Prevent the default form submission behavior

		// Get the URL entered by the user in the input field
		const singleUrl = document.getElementById('single-url').value;

		// Send a POST request to the '/ingest_single_url' route on the Flask backend
		fetch('/ingest_single_url', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ url: singleUrl })
		})
			// Handle Server Response for Single URL
			.then((response) => response.json())
			.then((data) => {
				if (data.message) {
					alert(data.message);
				} else {
					alert(data.error);
				}
			})
			.catch((error) => console.error('Error:', error));
	});

	// This event listener will handle the submission of the Multiple URLs form.
	multipleUrlsForm.addEventListener('submit', function (event) {
		event.preventDefault(); // Prevent the default form submission behavior

		// Get the URLs entered by the user, split by commas
		const multipleUrls = document.getElementById('urls').value.split(',');

		// Send a POST request to the '/ingest_urls' route on the Flask backend
		fetch('/ingest_urls', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ urls: multipleUrls })
		})
			// 5. Handle Server Response for Multiple URLs
			.then((response) => response.json())
			.then((data) => {
				if (data.message) {
					alert(data.message);
				} else {
					alert(data.error);
				}
			})
			.catch((error) => console.error('Error:', error));
	});
});
