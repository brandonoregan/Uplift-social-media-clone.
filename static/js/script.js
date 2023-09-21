"use strict";

const commentDisplayButtons = document.querySelectorAll(
  ".commentDisplayButtons"
);

// Toggle hidden on all new com buttons
commentDisplayButtons.forEach(function (button) {
  button.addEventListener("click", function () {
    // Find the closest parent element with the class "postCards"
    const postCard = button.closest(".postCards");

    // Find the child element with the class "newComForm" within the postCard
    const newComForm = postCard.querySelector(".newComForm");

    // Toggle the "hidden" class for the found newComForm element
    newComForm.classList.toggle("hidden");

    // newComFormClass.classList.toggle("hidden");
  });
});

// // Prevent forms submitting multiple times with multiple clicks
// document.addEventListener("DOMContentLoaded", function () {
//   console.log("JavaScript executed");
//   const submitButton = document.getElementById("submitButton");

//   // Get isSubmitting from local storage
//   let isSubmitting = localStorage.getItem("isSubmitting") === "true";

//   if (isSubmitting) {
//     submitButton.disabled = true;
//   }

//   submitButton.addEventListener("click", function (e) {
//     if (isSubmitting) {
//       e.preventDefault(); // Prevent multiple form submissions
//     } else {
//       isSubmitting = true;
//       submitButton.disabled = true; // Disable the button

//       localStorage.setItem("isSubmitting", "true");
//     }
//   });
// });

// Ensure model stays open after page refresh
// Ensure model stays open after page refresh
// Check if a modal open state is stored in local storage
// const modalOpen = localStorage.getItem("modalOpen");

// // If a modal open state exists and it's 'true', open the modal
// if (modalOpen === "true") {
//   const modal = new bootstrap.Modal(document.getElementById("exampleModal"));
//   modal.show();
// }

// // Listen for modal show/hide events and update local storage accordingly
// document
//   .getElementById("exampleModal")
//   .addEventListener("show.bs.modal", function () {
//     localStorage.setItem("modalOpen", "true");
//   });

// document
//   .getElementById("exampleModal")
//   .addEventListener("hide.bs.modal", function () {
//     localStorage.setItem("modalOpen", "false");
//   });
