// This code is part of a Django web application for a chat system.
// It handles the display of a popup for adding contacts.
document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    document.getElementById('addContactBtn').onclick = function () {
        document.getElementById('popup-container').style.display = 'flex';
    };
    document.getElementById('closeModalBtn').onclick = function () {
        document.getElementById('popup-container').style.display = 'none';
    };

    document.getElementById('addContactForm').onsubmit = async function (e) {
        e.preventDefault();
        document.getElementById('popup-container').style.display = 'none';
        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());
        data.user = currentUserId; // Assuming currentUserId is available in the context
        try {
            console.log('Adding contact:', data);
            const response = await fetch('http://localhost:8000/addContact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                body: JSON.stringify(data)
            });
            if (response.ok) {
                alert('Contact added!');
                const result = await response.json();
                console.log('Response JSON:', result);
                document.getElementById('popup-container').style.display = 'none';
                // Optionally reload or update user list here
                updateContactsList(result);
            } else {
                alert('Failed to add contact.');
            }
        } catch (err) {
            alert('Error occurred.');

        }
    };

    // Function to refresh the contacts list after contact is added
    function updateContactsList(contact) {
        const contactsList = document.getElementById('contactsList');
        const contactDiv = document.createElement('div');
        contactDiv.className = 'user';
        contactDiv.style.marginTop = '5px';
        contactDiv.style.borderRadius = '5px';
        contactDiv.setAttribute('data-user-id', contact.contact_id);      // Add this line
        contactDiv.setAttribute('data-username', contact.username);       // Add this line
        contactDiv.setAttribute('onclick', 'handleUserClick(this)'); // This matches your HTML
        const contactName = document.createElement('p');
        contactName.style.textAlign = 'center';
        contactName.style.paddingLeft = '10px';
        contactName.style.fontSize = '25px';
        contactName.textContent = contact.username;
        contactDiv.appendChild(contactName);
        contactsList.appendChild(contactDiv);
    }
});


// This code is used to toggle the visibility of the popup container
// when the "Add Contact" button is clicked, and to hide it when the close button
