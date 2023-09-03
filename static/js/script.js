"use strict";

// const editCommentForm = document.querySelector(".editCommentForm");
// const exposeEdit = document.querySelector(".exposeEdit");
const commentDisplay = document.getElementById("commentDisplay");
const newComForm = document.getElementById("newComForm");
const postFormContainer = document.getElementById("postFormContainer");
const rightColHome = document.getElementById("rightColHome");
const showPostFormButton = document.getElementById("showPostFormButton");

// exposeEdit.addEventListener("click", function () {
//   editCommentForm.classList.toggle("hidden");
// });
// Create function that targets closest expose edit and performs toggle above

commentDisplay.addEventListener("click", function () {
  newComForm.classList.toggle("hidden");
});

showPostFormButton.addEventListener("click", function () {
  postFormContainer.classList.toggle("hidden");
});
