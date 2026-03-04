document.getElementById("loginForm").addEventListener("submit", function(e){
    e.preventDefault();

    // Temporarily bypass validation
    window.location.href = "admin.html";
});