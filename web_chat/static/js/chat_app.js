// chat_app.js
// This code is part of a Django web application for a chat system.
// It handles WebSocket connections, message sending, and UI updates.
async function handleUserClick(element) {
	const userId = element.getAttribute('data-user-id');
	const username = element.getAttribute('data-username');

	// Update the top username display
	document.querySelector('.username').textContent = username;

	// Update URL
	history.pushState(null, '', '/user/' + userId);
	const start_time = performance.now();
	await connectWebSocket();
	const end_time = performance.now();
	console.log("WebSocket connection time: " + (end_time - start_time) + "ms");
	console.log("Selected user: " + username);
}

function getCSRFToken() {
	return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

async function connectWebSocket() {
	roomName = await getRoomName();
	console.log("Room name: " + roomName);
	const urlParts = window.location.href.split('/');
	websocket_url = `ws://localhost:8000/ws/chat/${roomName}/`;
	ws = new WebSocket(websocket_url);

	ws.onopen = function () {
		console.log("WebSocket is open now.");
		var toastEl = document.querySelector('.toast');
		var toast = new bootstrap.Toast(toastEl);
		toast.show();
	};

	ws.onmessage = function (event) {
		var data = JSON.parse(event.data);
		if (data && data.message) {
			console.log("Received message: " + data.message);
			console.log("Sender ID: " + data.message.sender_id);
			console.log("Current User ID: " + currentUserId);

			chat_div = document.querySelector('.chat-div');
			var chatMessage = document.createElement('div');
			chatMessage.className = 'chat-message';

			// Check if sender is current user
			if (data.message.sender_id == currentUserId) {
				// Current user's message - align right
				chatMessage.style.alignSelf = 'flex-end';
				chatMessage.style.backgroundColor = '#dcf8c6'; // Light green for sent messages
				if (data.message.file_url) {
					chatMessage.innerHTML = `
					<img src="${data.message.file_url}" style="max-width:200px;max-height:200px;display:block;margin-bottom:5px;">
					<span>${data.message.message}</span>
				`;
				}
				else {
					chatMessage.innerHTML = `<p style="text-align: right;">${data.message.message}</p>`;
				}
			} else {
				// Other user's message - align left
				chatMessage.style.alignSelf = 'flex-start';
				chatMessage.style.backgroundColor = '#7D8EE3'; // Light gray for received messages
				if (data.message.file_url) {
					chatMessage.innerHTML = `
						<img src="${data.message.file_url}" style="max-width:200px;max-height:200px;display:block;margin-bottom:5px;">
						<span>${data.message.message}</span>
					`;
				} else {
					chatMessage.innerHTML = `<p style="text-align: left;">${data.message.message}</p>`;
				}
			}

			chat_div.appendChild(chatMessage);
			chat_div.scrollTop = chat_div.scrollHeight; // Auto-scroll to bottom
		}
	};

	ws.onclose = function () {
		console.log("WebSocket is closed now.");
	};
}

async function sendMessage() {
	var chatInput = document.getElementById('chat-text-input');
	var fileInput = document.getElementById('chat-file-input');
	var chatMessage = chatInput.value;
	var file = fileInput.files[0];
	var chatUserId = ChatUserId();

	let fileUrl = null;
	let fileType = null;

	chatInput.value = '';
	fileInput.value = '';

	if (file) {
		// Upload file to S3
		const formData = new FormData();
		formData.append('file', file);

		const response = await fetch('/s3/upload', {
			method: 'POST',
			headers: {
				'X-CSRFToken': getCSRFToken()
			},
			body: formData
		});
		const result = await response.json();
		fileUrl = result.file_url;
		fileType = file.type;
	}
	console.log("File URL: " + fileUrl);
	console.log("File Type: " + fileType);

	if (ws.readyState === WebSocket.OPEN) {
		ws.send(JSON.stringify({
			'message': chatMessage,
			'sender_id': currentUserId,
			'receiver_id': chatUserId,
			'file_url': fileUrl,
			'file_type': fileType
		}));
	} else {
		console.error("WebSocket is not open. Ready state: " + ws.readyState);
	}
	// empty file preview
	const previewDiv = document.getElementById('file-preview');
	previewDiv.innerHTML = ""; // Clear previous preview
}

async function getRoomName() {
	const urlParts = window.location.href.split('/');
	const userId = urlParts[4];
	console.log("URL parts: " + urlParts);
	console.log("Chat User ID: " + userId);
	console.log("Current User ID: " + currentUserId);
	const response = await fetch(`http://localhost:8000/contactDetails?contact_id=${userId}`);
	const responseDetails = await response.json();
	console.log("Current and chat user mobiles: " + currentUserMobile + ", " + responseDetails[0].mobile);
	const usersDetails = [currentUserMobile, responseDetails[0].mobile].sort();
	roomName = usersDetails.join('_');
	console.log("Room name: " + roomName);
	return roomName;
}

function ChatUserId() {
	const urlParts = window.location.href.split('/');
	const userId = urlParts[4];
	return parseInt(userId);
}

window.onload = async function () {
	await connectWebSocket();

	// Get username from URL if user navigated directly to a chat
	const urlParts = window.location.href.split('/');
	if (urlParts[4]) {
		const userId = urlParts[4];
		// Find the contact in the list and get their username
		const contactElements = document.querySelectorAll('.user');
		contactElements.forEach(element => {
			if (element.getAttribute('data-user-id') == userId ||
				element.onclick.toString().includes(userId)) {
				const username = element.querySelector('.contact-username').textContent.trim();
				document.querySelector('.username').textContent = username;
			}
		});
	}
};

function showFileNameInInput(fileInput) {
	const chatInput = document.getElementById('chat-text-input');
	const previewDiv = document.getElementById('file-preview');
	previewDiv.innerHTML = ""; // Clear previous preview

	if (fileInput.files && fileInput.files[0]) {
		const file = fileInput.files[0];
		chatInput.value = file.name; // Show file name in input box

		// Render preview for images
		if (file.type.startsWith("image/")) {
			const img = document.createElement("img");
			img.src = URL.createObjectURL(file);
			img.style.maxWidth = "200px";
			img.style.maxHeight = "200px";
			previewDiv.appendChild(img);
		}
		// Render preview for PDFs
		else if (file.type === "application/pdf") {
			const iframe = document.createElement("iframe");
			iframe.src = URL.createObjectURL(file);
			iframe.width = "200";
			iframe.height = "200";
			previewDiv.appendChild(iframe);
		}
		// For other files, just show the file name
		else {
			previewDiv.textContent = "Selected file: " + file.name;
		}
	}
}