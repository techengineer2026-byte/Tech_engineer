// =======================================================
// THE MASTER URL (Handles BOTH Sheet 1 and Sheet 2)
// =======================================================
const MASTER_URL =
  "https://script.google.com/macros/s/AKfycbxdSLbUgQQcB5xm3C6QM8lOrLBYym17AzAhNDIobq-YUbyWp0-H3xit3wRXR-AJ6GG3/exec";

// =======================================================
// 1. GENERAL INQUIRY MODAL LOGIC (Goes to Sheet 1)
// =======================================================

function openModal(serviceName) {
  document.getElementById("modalTitle").innerText = "Inquire: " + serviceName;
  document.getElementById("serviceInput").value = serviceName;
  var myModal = new bootstrap.Modal(document.getElementById("inquiryModal"));
  myModal.show();
}

const inquiryForm = document.forms["contactForm"];
const inquiryBtn = document.getElementById("submitBtn");

// Only run this if the Inquiry Form exists on the page
if (inquiryForm) {
  inquiryForm.addEventListener("submit", (e) => {
    e.preventDefault();
    inquiryBtn.disabled = true;
    inquiryBtn.innerHTML =
      'Sending... <i class="fas fa-spinner fa-spin ms-2"></i>';

    fetch(MASTER_URL, { method: "POST", body: new FormData(inquiryForm) })
      .then((response) => {
        alert("Thank you! Your message was sent successfully.");
        inquiryBtn.disabled = false;
        inquiryBtn.innerHTML =
          'Send Request <i class="fas fa-rocket ms-2"></i>';
        inquiryForm.reset();

        var modalEl = document.getElementById("inquiryModal");
        var modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
      })
      .catch((error) => {
        alert("Error! " + error.message);
        inquiryBtn.disabled = false;
        inquiryBtn.innerHTML =
          'Send Request <i class="fas fa-rocket ms-2"></i>';
      });
  });
}

// =======================================================
// 2. SYLLABUS DOWNLOAD LOGIC (Goes to Sheet 2 & Sends Auto-Email)
// =======================================================

const pdfForm = document.getElementById("pdfForm");
const pdfBtn = document.getElementById("pdfSubmitBtn");

// Only run this if the Syllabus PDF Form exists on the page
if (pdfForm) {
  pdfForm.addEventListener("submit", (e) => {
    e.preventDefault();

    // Change button state
    pdfBtn.disabled = true;
    pdfBtn.innerHTML = 'Sending... <i class="fas fa-spinner fa-spin ms-2"></i>';

    // Send to Sheet 2
    fetch(MASTER_URL, { method: "POST", body: new FormData(pdfForm) })
      .then((response) => response.json()) // <-- ADDED THIS TO READ THE JSON
      .then((data) => {
        if (data.result === "success") {
          // It actually worked!
          alert(
            "Success! We have received your request. The syllabus will be sent to your email.",
          );
          pdfBtn.disabled = false;
          pdfBtn.innerHTML =
            'Get Syllabus Now <i class="fas fa-download ms-2"></i>';
          pdfForm.reset();
          var modalEl = document.getElementById("pdfModal");
          var modal = bootstrap.Modal.getInstance(modalEl);
          if (modal) modal.hide();
        } else {
          // The script crashed, show the REAL error!
          alert("Google Script Error: " + data.error);
          pdfBtn.disabled = false;
          pdfBtn.innerHTML =
            'Get Syllabus Now <i class="fas fa-download ms-2"></i>';
        }
      })
      .catch((error) => {
        alert("Network Error! " + error.message);
        pdfBtn.disabled = false;
        pdfBtn.innerHTML =
          'Get Syllabus Now <i class="fas fa-download ms-2"></i>';
      });
  });
}
