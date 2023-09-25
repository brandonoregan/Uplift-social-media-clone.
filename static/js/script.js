"use strict";

const commentDisplayButtons = document.querySelectorAll(
  ".commentDisplayButtons"
);
const backToTop = document.querySelector(".backToTop");

backToTop.addEventListener("click", function () {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
});

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

// Prevent forms submitting multiple times with multiple clicks
document.addEventListener("DOMContentLoaded", function () {
  // select all elemts with the class submitButton
  const submitButtons = document.querySelectorAll(".submitButton");

  // Get isSubmitting from local storage
  let isSubmitting = localStorage.getItem("isSubmitting") === "true";

  // Flag to indicate whether the form is currently loading
  let isFormLoading = false;

  if (isSubmitting) {
    console.log("Top:", isSubmitting);
    disableSubmitButton(submitButtons);
  }

  // loop through all submitButtons instances
  submitButtons.forEach(function (submitButton) {
    // attach an event listener to each button and capture the event
    submitButton.addEventListener("click", function (e) {
      // identify the form where the submitButton was clicked
      const form = submitButton.closest("form");
      // check is the form is loading
      if (isFormLoading) {
        console.log("isFormLoading:", isFormLoading);
        e.preventDefault(); // Prevent multiple form submissions
        disableSubmitButton(submitButtons);
      } else {
        console.log("Second", "isFormLoading:", isFormLoading);
        form.addEventListener("load", function () {
          enableSubmitButton(submitButtons);
        });
        isFormLoading = true;
      }
    });
  });

  function disableSubmitButton(submitButtons) {
    isSubmitting = true;
    submitButtons.disabled = true;
    localStorage.setItem("isSubmitting", "true");
    console.log("Disabled");
  }

  function enableSubmitButton(submitButtons) {
    isSubmitting = false;
    submitButtons.disabled = false;
    localStorage.setItem("isSubmitting", "false");
    console.log("Enabled");
  }

  console.log("Bottom:", isSubmitting);
});

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

if (window.location.pathname === "/home") {
  // Event listener for form submissions
  document.addEventListener("DOMContentLoaded", function () {
    const postFormOne = document.querySelector(".postFormOne");
    const postFormTwo = document.querySelector(".postFormTwo");

    // Event listener for form 1 submission
    postFormOne.addEventListener("submit", function () {
      localStorage.setItem("scrollPosition", "form1");
    });

    // Event listener for form 2 submission
    postFormTwo.addEventListener("submit", function () {
      localStorage.setItem("scrollPosition", "form2");
    });
  });

  // Get the scroll position when the page loads or is refreshed
  window.addEventListener("beforeunload", function () {
    // Check if the scrollPosition was set by a form submission
    const scrollPosition = localStorage.getItem("scrollPosition");
    if (scrollPosition !== "form1" && scrollPosition !== "form2") {
      localStorage.setItem("scrollPosition", window.scrollY);
    }
  });

  // Set the scroll position or scroll to the top based on the scrollPosition flag
  window.addEventListener("load", function () {
    const scrollPosition = localStorage.getItem("scrollPosition");

    if (scrollPosition === "form1" || scrollPosition === "form2") {
      // Scroll to the top if a form was submitted
      window.scrollTo(0, 0);
      localStorage.setItem("scrollPosition", "");
    } else {
      // Restore the scroll position if no form was submitted
      window.scrollTo(0, parseInt(scrollPosition));
      localStorage.setItem("scrollPosition", "");
    }
  });
} else {
  // Reset the scrollPosition when the home page is left
  window.addEventListener("beforeunload", function (e) {
    // Set the local storage variable here
    localStorage.setItem("scrollPosition", "form1");
  });
}

// const hideComments = document.getElementById("hideComments");
// const viewComments = document.getElementById("viewComments");

// document.addEventListener("DOMContentLoaded", function () {
//   const viewCommentButtons = document.querySelectorAll(".viewComments");
//   const hideCommentButtons = document.querySelectorAll(".hideComments");
//   const commentThreadLongs = document.querySelectorAll(".commentThreadLong");
//   const commentThreadShorts = document.querySelectorAll(".commentThreadShort");

//   viewCommentButtons.forEach(function (viewButton) {
//     viewButton.addEventListener("click", function (e) {
//       commentThreadLongs.forEach(function (button) {
//         button.classList.toggle("hidden");
//       });
//       console.log("View Clicked ");
//     });
//   });

//   hideCommentButtons.forEach(function (hideButton) {
//     hideButton.addEventListener("click", function (e) {
//       commentThreadShorts.forEach(function (button) {
//         button.classList.toggle("hidden");
//       });
//       console.log("Hide Clicked");
//     });
//   });
// });

// const postCards = document.querySelectorAll(".postCards");
// const commentThreadLong = document.querySelector(".commentThreadLong");

// document.addEventListener("DOMContentLoaded", function () {
//   commentThreadLong.classList.add("hidden");
// });

// postCards.forEach(function (post) {
//   post.addEventListener("click", function (e) {
//     const closestViewButton = e.target.closest(".viewComments");
//     const closestHideButton = e.target.closest(".hideComments");
//     const closestShortThread = e.target.closest(".commentThreadShort");
//     const closestLongThread = e.target.closest(".commentThreadLong");

//     if (closestViewButton) {
//       closestShortThread.classList.toggle("hidden");
//       commentThreadLong.classList.toggle("hidden");
//       console.log("Bingo");
//     } else if (closestHideButton) {
//       closestShortThread.classList.toggle("hidden");
//       commentThreadLong.classList.toggle("hidden");
//     } else {
//       console.log("WHOOOPS");
//     }
//   });
// });
