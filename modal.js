// 1. Function to Open Modal and Set Service Name
function openModal(serviceName) {
    // Set the visible title
    document.getElementById('modalTitle').innerText = 'Inquire: ' + serviceName;
    // Set the hidden input value so it goes to Google Sheet
    document.getElementById('serviceInput').value = serviceName;
    // Open the modal using Bootstrap API
    var myModal = new bootstrap.Modal(document.getElementById('inquiryModal'));
    myModal.show();
}

// 2. Script to Send Data to Google Sheet
const scriptURL = 'https://script.google.com/macros/s/AKfycbyEXg2yuWTR7DrwdjZcdlVoz_95kgiySTah7EEohI2aQ6uhMvOPcj68Q9RTotSkcNg/exec'; // <--- YOU WILL PASTE URL HERE LATER
const form = document.forms['contactForm'];
const btn = document.getElementById('submitBtn');

form.addEventListener('submit', e => {
    e.preventDefault();
    btn.disabled = true;
    btn.innerText = "Sending...";

    fetch(scriptURL, { method: 'POST', body: new FormData(form) })
        .then(response => {
            alert("Thank you! Your message sent successfully.");
            btn.disabled = false;
            btn.innerText = "Send Inquiry";
            form.reset();
            // Close modal
            var modalEl = document.getElementById('inquiryModal');
            var modal = bootstrap.Modal.getInstance(modalEl);
            modal.hide();
        })
        .catch(error => {
            alert('Error!', error.message);
            btn.disabled = false;
            btn.innerText = "Send Inquiry";
        });
});
