"use strict";

// const editCommentForm = document.querySelector(".editCommentForm");
// const exposeEdit = document.querySelector(".exposeEdit");
const commentDisplay = document.getElementById("commentDisplay");
const newComForm = document.getElementById("newComForm");

// exposeEdit.addEventListener("click", function () {
//   editCommentForm.classList.toggle("hidden");
// });
// Create function that targets closest expose edit and performs toggle above

commentDisplay.addEventListener("click", function () {
  newComForm.classList.toggle("hidden");
});
