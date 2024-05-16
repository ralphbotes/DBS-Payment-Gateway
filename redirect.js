function redirectToPage(a_data) {
    // Create a hidden form element
    const form = document.createElement('form');
    form.style.display = 'none'; // Hide the form

    // Set form attributes
    form.method = 'POST';
    form.action = a_data["submitUrl"];

    // Add form fields
    const requestIdInput = document.createElement('input');
    requestIdInput.type = 'hidden';
    requestIdInput.name = 'requestId';
    requestIdInput.value = a_data["form_request_payload"]["requestId"];
    form.appendChild(requestIdInput);

    const encryptedPayloadInput = document.createElement('input');
    encryptedPayloadInput.type = 'hidden';
    encryptedPayloadInput.name = 'encryptedPayload';
    encryptedPayloadInput.value = a_data["form_request_payload"]["encryptedPayload"];
    form.appendChild(encryptedPayloadInput);

    // Append the form to the document body
    document.body.appendChild(form);

    // Submit the form
    form.submit();
}