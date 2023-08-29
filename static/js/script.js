"use strict";

const editCommentForm = document.querySelector(".editCommentForm");
const exposeEdit = document.querySelector(".exposeEdit");

exposeEdit.addEventListener("click", function () {
  editCommentForm.classList.toggle("hidden");
});
// Create function that targets closest expose edit and performs toggle above
