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
