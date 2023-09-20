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
