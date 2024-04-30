function toggleLoginForm() {
    var loginForm = document.getElementById("login-form");
    if (loginForm.style.display === "block") {
        loginForm.style.display = "none";
    } else {
        loginForm.style.display = "block";
    }
}

function toggleAddNoteForm() {
    var addNoteForm = document.getElementById("addNoteForm");
    if (addNoteForm.style.display === "block") {
        addNoteForm.style.display = "none";
    } else {
        addNoteForm.style.display = "block";
    }
}

function toggleEditNoteForm(blog_id) {
    var addNoteForm = document.getElementById(blog_id);
    if (addNoteForm.style.display === "block") {
        addNoteForm.style.display = "none";
    } else {
        addNoteForm.style.display = "block";
    }
}

function deleteBlog(blogId) {
    fetch("/delete", {
        method: "POST",
        body: JSON.stringify({blog_id: blogId}),
    })
    .then((respone) => {window.location.href = "/admin"})
}